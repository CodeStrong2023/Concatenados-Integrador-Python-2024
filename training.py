import re
import random
import psycopg2

# Conexión a la base de datos
def get_tournament_data():
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
                cursor.execute('SELECT nombre FROM torneos')
                torneos = cursor.fetchall()
        return [torneo[0] for torneo in torneos]
    except psycopg2.Error as e:
        return []
    finally:
        if 'conexion' in locals() and conexion is not None:
            conexion.close()

# Patrones y respuestas mejorados
pares = [
    ('hola|ayuda', ['Hola, bienvenido a TorneosARG. ¿En qué puedo ayudarte?']),
    
    ('menu', ['MENU:\n'
              '1. Torneos\n'
              '2. Horarios\n'
              '3. Reglas\n'
              '4. Inscripción\n'
              '5. Mi Perfil\n'
              '6. Chat en Vivo']),

    ('1|torneos', ['Los torneos disponibles son:\n' '\n✅' + '\n\n✅'.join(get_tournament_data())]),
    
    ('2|horarios', ['Los horarios son:\n'
                    'Lunes 9:00PM a 12:00AM\n'
                    'Martes 8:00PM a 10:00PM\n'
                    'Miércoles 7:00PM a 9:00PM']),
    
    ('3|reglas', ['Las reglas son:\n'
                  '1. No usar hacks\n'
                  '2. Queda prohibido cualquier clase de insulto\n'
                  '3. Respetar los horarios']),
    
    ('4|inscripción|inscripcion|inscribirme', ['Para inscribirte en un torneo, debes registrarte e iniciar sesión y luego podrás acceder a el torneo de tu interés.']),
    
    ('5|perfil', ['Para ver tu perfil y torneos inscritos, visita tu perfil en nuestra página web.']),
    
    ('6|chat en vivo', ['Para acceder al chat en vivo, haz clic en el botón de chat en la parte inferior derecha de la pantalla.']),
    
    ('adiós|adios|gracias|chau|bye', ['¡Hasta luego!']),
    
    ('(.*)', ['Lo siento, no entiendo esa pregunta.\n'
              'Prueba usar "Menu" o pregunta sobre torneos, horarios, reglas, inscripción, perfil o chat en vivo.'])
]

def chatbot_response(user_input):
    for pattern, responses in pares:
        if re.match(pattern, user_input.lower()):
            return random.choice(responses)
    return "Lo siento, no entiendo esa pregunta."