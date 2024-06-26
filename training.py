# Pares de patrones y respuestas para el chatbot
pares = [
    ('hola|ayuda', ['Hola, bienvenido a TorneosARG en que puedo ayudarte?']),

    ('menu', ['MENU:\n'
              '1. Torneos\n'
              '2. Horarios\n'
              '3. Reglas']),

    ('1|torneos', ['Los torneos disponibles son:\n'
                   'T.Mundial Fortnite\n'
                   'T.Arg CS2']),

    ('2|horarios', ['Los horarios son:\n'
                    'Lunes 9:00PM a 12:00AM\n'
                    'Martes 8:00PM a 10:00PM']),

    ('3|reglas', ['Las reglas son:\n'
                  '1. No usar hacks\n'
                  '2. Queda prohibido cualquier clase de insulto']),

    ('adiós|adios|gracias|chau|bye', ['¡Hasta luego!']),

    ('(.*)', ['Lo siento, no entiendo esa pregunta.\n'
              'Pruebe usar "Menu"']),
]
