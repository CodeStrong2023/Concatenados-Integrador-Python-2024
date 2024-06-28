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
    ('hola|ayuda|buenos días|buenas tardes|buenas noches', [
        'Hola, bienvenido a TorneosARG. ¿En qué puedo ayudarte?\n',
        '¡Hola! ¿Cómo puedo asistirte hoy?\n',
        'Bienvenido a TorneosARG. ¿Necesitas ayuda con algo?\n'
    ]),

    ('menu', [
        'MENU:\n'
        '1. Torneos\n'
        '2. Horarios\n'
        '3. Reglas\n'
        '4. Inscripción\n'
        '5. Mi Perfil\n'
        '6. Chat en Vivo\n'
        '7. Premios',
        'Aquí tienes el menú:\n'
        '1. Torneos\n'
        '2. Horarios\n'
        '3. Reglas\n'
        '4. Inscripción\n'
        '5. Mi Perfil\n'
        '6. Chat en Vivo\n'
        '7. Premios'
    ]),

    ('1|torneos', [
        'Los torneos disponibles son:\n' + '\n✅'.join(get_tournament_data()),
        'Estos son los torneos que tenemos actualmente:\n' + '\n✅'.join(get_tournament_data())
    ]),

    ('2|horarios', [
        'Los horarios son:\n'
        'Lunes 9:00PM a 12:00AM\n'
        'Martes 8:00PM a 10:00PM\n'
        'Miércoles 7:00PM a 9:00PM',
        'Nuestros horarios son los siguientes:\n'
        'Lunes 9:00PM a 12:00AM\n'
        'Martes 8:00PM a 10:00PM\n'
        'Miércoles 7:00PM a 9:00PM'
    ]),

    ('3|reglas|normas', [
        'Las reglas son:\n'
        '1. No usar hacks\n'
        '2. Queda prohibido cualquier clase de insulto\n'
        '3. Respetar los horarios',
        'Estas son las normas del torneo:\n'
        '1. No usar hacks\n'
        '2. No se permiten insultos\n'
        '3. Cumplir con los horarios establecidos'
    ]),

    ('4|inscripción|inscripcion|inscribirme|registrar|registrarme|registro|torneo', [
        'Para inscribirte en un torneo, debes registrarte e iniciar sesión y luego podrás acceder al torneo de tu interés.',
        'Primero, regístrate e inicia sesión para poder inscribirte en un torneo de tu elección.'
    ]),

    ('5|perfil|mi perfil|cuenta', [
        'Para ver tu perfil y torneos inscritos, visita tu perfil en nuestra página web.',
        'Accede a tu perfil en nuestra web para ver tus torneos inscritos y más detalles.'
    ]),

    ('6|chat en vivo|soporte', [
        'Para acceder al chat en vivo, haz clic en el botón de chat en la parte inferior derecha de la pantalla.',
        'Puedes acceder al chat en vivo desde el botón en la esquina inferior derecha de tu pantalla.'
    ]),

    ('7|premios', ['Los premios para los ganadores incluyen:\n'
                   '1. Dinero en efectivo\n'
                   '2. Hardware de última generación\n'
                   '3. Merchandising exclusivo\n'
                   '4. Entradas para eventos']),

    ('adiós|adios|gracias|chau|bye|hasta luego', [
        '¡Hasta luego!',
        '¡Adiós! Nos vemos pronto.',
        'Gracias por visitar TorneosARG. ¡Hasta la próxima!'
    ]),

    ('(.*)', [
        'Lo siento, no entiendo esa pregunta.\n'
        'Prueba usar "Menu" o pregunta sobre torneos, horarios, reglas, inscripción, perfil o chat en vivo.',
        'No estoy seguro de entender tu pregunta. Por favor, usa "Menu" para ver las opciones disponibles.'
    ])
]


def chatbot_response(user_input):
    for pattern, responses in pares:
        if re.match(pattern, user_input.lower()):
            return random.choice(responses)
    return "Lo siento, no entiendo esa pregunta."