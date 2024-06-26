import json
import urllib
from http.cookies import SimpleCookie

import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import os

from chatbot import chatbot_response

class ServerHandler(BaseHTTPRequestHandler):
    """
    Clase que maneja las peticiones HTTP para un servidor simple.
    """

    def do_GET(self):
        """
        Maneja las peticiones GET.
        """
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        query = urllib.parse.parse_qs(parsed_url.query)

        # Manejo de rutas estáticas
        if path == '/index.html' or path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/registro.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('registro.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/login.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/home.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('home.html', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/styles.css':
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open('styles.css', 'rb') as f:
                self.wfile.write(f.read())
        elif path == '/script.js':
            self.send_response(200)
            self.send_header('Content-type', 'application/javascript')
            self.end_headers()
            with open('script.js', 'rb') as f:
                self.wfile.write(f.read())
        elif path.startswith('/img/'):
            self.serve_static_file(path, 'image')  # Servir archivos de imagen
        elif path == '/mis-torneos':
            self.get_user_tournaments()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def serve_static_file(self, path, content_type):
        """
        Método para servir archivos estáticos como imágenes.
        """
        try:
            with open(path[1:], 'rb') as f:  # Eliminar '/' inicial de la ruta
                self.send_response(200)
                if content_type == 'image':
                    # Determinar el tipo de imagen basado en la extensión del archivo
                    if path.endswith('.jpg'):
                        self.send_header('Content-type', 'image/jpeg')
                    elif path.endswith('.png'):
                        self.send_header('Content-type', 'image/png')
                    elif path.endswith('.webp'):
                        self.send_header('Content-type', 'image/webp')
                self.end_headers()
                self.wfile.write(f.read())
        except IOError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"File not found")

    def do_POST(self):
        """
        Maneja las peticiones POST para registro y login.
        """
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/registro':
            self.handle_register()  # Manejar registro de usuarios
        elif path == '/login':
            self.handle_login()  # Manejar inicio de sesión
        elif path == '/logout':
            self.handle_logout()  # Manejar cierre de sesión
        elif path == '/inscribir':
            self.register_tournament()
        elif path == '/chat':
            self.handle_chat()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def handle_register(self):
        """
        Maneja la creación de nuevos usuarios.
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        username = form.getvalue('username')
        email = form.getvalue('email')
        password = form.getvalue('password')
        confirm_password = form.getvalue('confirm-password')

        # Validar que todos los campos obligatorios estén presentes
        if not username or not email or not password or not confirm_password:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Todos los campos son obligatorios.'}).encode())
            return

        # Validar que las contraseñas coincidan
        if password != confirm_password:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Las contraseñas no coinciden.'}).encode())
            return

        try:
            # Conectar a la base de datos PostgreSQL
            conexion = psycopg2.connect(
                user='postgres',
                password='admin',
                host='127.0.0.1',
                port='5432',
                database='Integrador'
            )

            with conexion:
                with conexion.cursor() as cursor:
                    # Ejecutar la sentencia SQL para insertar el usuario
                    sentencia = 'INSERT INTO users (username, email, password) VALUES (%s, %s, %s)'
                    valores = (username, email, password)
                    cursor.execute(sentencia, valores)
                    conexion.commit()
                    registros_insertados = cursor.rowcount
                    print(f'Los registros insertados son: {registros_insertados}')

            # Respuesta exitosa si todo fue correcto
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Cuenta creada exitosamente'}).encode())
        except psycopg2.Error as e:
            # Manejo de errores si hay un problema con la base de datos
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': f'Error: {e}'}).encode())
        finally:
            # Cerrar la conexión a la base de datos de manera segura
            if 'conexion' in locals() and conexion is not None:
                conexion.close()

    def handle_login(self):
        """
        Maneja el proceso de inicio de sesión de usuarios.
        """
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        username = form.getvalue('username')
        password = form.getvalue('password')

        # Validar que todos los campos obligatorios estén presentes
        if not username or not password:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Todos los campos son obligatorios.'}).encode())
            return

        try:
            # Conectar a la base de datos PostgreSQL
            conexion = psycopg2.connect(
                user='postgres',
                password='admin',
                host='127.0.0.1',
                port='5432',
                database='Integrador'
            )

            with conexion:
                with conexion.cursor() as cursor:
                    # Consultar si existe un usuario con el nombre de usuario y contraseña proporcionados
                    sentencia = 'SELECT username FROM users WHERE username = %s AND password = %s'
                    valores = (username, password)
                    cursor.execute(sentencia, valores)
                    usuario = cursor.fetchone()
                    sentencia = 'SELECT id FROM users WHERE username = %s AND password = %s'
                    cursor.execute(sentencia, valores)
                    id_usuario = cursor.fetchone()


            if usuario:
                # Respuesta exitosa si el usuario existe
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Set-Cookie', f'user_id={id_usuario[0]}; Path=/; HttpOnly')
                self.send_header('Access-Control-Allow-Origin', '*')  # Permitir acceso CORS
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps({'success': True, 'message': 'Inicio de sesión exitoso', 'username': usuario[0], 'id': id_usuario[0]}).encode())
                print(id_usuario[0])
            else:
                # Respuesta de credenciales incorrectas si no se encuentra el usuario
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')  # Permitir acceso CORS
                self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'message': 'Credenciales incorrectas'}).encode())

        except psycopg2.Error as e:
            # Manejo de errores si hay un problema con la base de datos
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # Permitir acceso CORS
            self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': f'Error: {e}'}).encode())
        finally:
            # Cerrar la conexión a la base de datos de manera segura
            if 'conexion' in locals() and conexion is not None:
                conexion.close()

    def handle_logout(self):
        """
        Maneja la operación de logout del usuario.
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'success': True, 'message': 'Sesión cerrada exitosamente'}).encode())

        # Aquí podrías añadir más lógica si necesitas limpiar variables de sesión específicas.


    def register_tournament(self):
        cookie = SimpleCookie(self.headers.get('Cookie'))
        user_id = cookie.get('user_id').value if cookie.get('user_id') else None


        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )

        tournament_id = form.getvalue('tournament_id')

        if not user_id or not tournament_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Todos los campos son obligatorios.'}).encode())
            return

        try:
            conexion = psycopg2.connect(
                user='postgres',
                password='admin',
                host='127.0.0.1',
                port='5432',
                database='Integrador'
            )

            with conexion:
                with conexion.cursor() as cursor:
                    # Verificar si el usuario ya está inscrito en el torneo
                    cursor.execute('SELECT * FROM user_tournaments WHERE user_id = %s AND torneos_id = %s',
                                   (user_id, tournament_id))
                    existing_registration = cursor.fetchone()

                    if existing_registration:
                        # Si el usuario ya está inscrito, enviar respuesta de error
                        self.send_response(400)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(
                            json.dumps({'success': False, 'message': 'Ya estás inscrito en este torneo.'}).encode())
                        return
                    sentencia = 'INSERT INTO user_tournaments (user_id, torneos_id) VALUES (%s, %s)'
                    valores = (user_id, tournament_id)
                    cursor.execute(sentencia, valores)
                    conexion.commit()

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'message': 'Inscripción exitosa'}).encode())
        except psycopg2.Error as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': f'Error: {e}'}).encode())
        finally:
            if 'conexion' in locals() and conexion is not None:
                conexion.close()

    def get_user_tournaments(self):
        """
        Maneja la solicitud de obtener los torneos inscritos por un usuario.
        """
        cookie = SimpleCookie(self.headers.get('Cookie'))
        user_id = cookie.get('user_id').value if cookie.get('user_id') else None

        if not user_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': 'Usuario no autenticado.'}).encode())
            return

        try:
            conexion = psycopg2.connect(
                user='postgres',
                password='admin',
                host='127.0.0.1',
                port='5432',
                database='Integrador'
            )

            with conexion:
                with conexion.cursor() as cursor:
                    # Consultar los nombres de los torneos inscritos por el usuario
                    cursor.execute('''
                        SELECT t.nombre
                        FROM torneos t
                        INNER JOIN user_tournaments ut ON t.id = ut.torneos_id
                        WHERE ut.user_id = %s
                    ''', (user_id,))
                    torneos = cursor.fetchall()

            # Crear una lista de nombres de torneos
            nombres_torneos = [torneo[0] for torneo in torneos]

            # Enviar una respuesta con los nombres de los torneos
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True, 'torneos': nombres_torneos}).encode())

        except psycopg2.Error as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': False, 'message': f'Error: {e}'}).encode())

        finally:
            if 'conexion' in locals() and conexion is not None:
                conexion.close()

    def handle_logout(self):

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Set-Cookie', 'session=; expires=Thu, 01 Jan 1970 00:00:00 GMT')  # Expira la cookie de sesión
        self.end_headers()
        response = {'success': True, 'message': 'Sesión cerrada exitosamente'}
        self.wfile.write(json.dumps(response).encode())

    def handle_chat(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        message = json.loads(post_data)['message']
        response = chatbot_response(message)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'response': response}).encode())

def run_server():
    """
    Función para iniciar el servidor HTTP.
    """
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, ServerHandler)
    print("Servidor iniciado en http://localhost:8080/")
    httpd.serve_forever()

run_server()
