import ply.lex as lex
import ply.yacc as yacc
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

ruta_json_global = None

# Variable global para marcar si hay errores
has_errors = False

# Tokens
tokens = (
    'A_STRING', 'EQUIPOS', 'DIRECCION', 'ESTADO', 'VERSION', 'FIRMA_DIGITAL', 'LINK', 'EDAD', 'FOTO', 'EMAIL',
    'HABILIDADES', 'SALARIO', 'ACTIVO', 'TAREAS', 'FECHA_INICIO', 'FECHA_FIN', 'VIDEO',
    'LLAVE_ABRE', 'LLAVE_CIERRA', 'CORCHETE_ABRE', 'CORCHETE_CIERRA', 'DOS_PUNTOS', 'COMA',
    'NUMBER', 'TRUE', 'FALSE', 'NULL', 'CONCLUSION', 'RESUMEN', 'CALLE', 'CIUDAD', 'PAIS', 'DATE',
    'NOMBRE', 'NOMBRE_EQUIPO', 'IDENTIDAD_EQUIPO', 'CARRERA', 'ASIGNATURA', 'UNIVERSIDAD_REGIONAL',
    'ALIANZA_EQUIPO', 'INTEGRANTES', 'PROYECTOS', 'CARGO'
)

# Definición de tokens simples
t_LLAVE_ABRE = r'\{'
t_LLAVE_CIERRA = r'\}'
t_CORCHETE_ABRE = r'\['
t_CORCHETE_CIERRA = r'\]'
t_DOS_PUNTOS = r':'
t_COMA = r','
t_TRUE = r'true'
t_FALSE = r'false'
t_NULL = r'null'


# Tokens con funciones (MÁS ESPECÍFICOS PRIMERO)

def t_LINK(t):
    r'"https?://[^"\s]+"'
    return t


def t_DATE(t):
    r'"\d{4}-\d{2}-\d{2}"'  # Fechas entre comillas
    t.value = t.value.strip('"')  # Quitar las comillas
    return t


def t_UNIVERSIDAD_REGIONAL(t):
    r'"universidad_regional"'
    return t


def t_IDENTIDAD_EQUIPO(t):
    r'"identidad_equipo"'
    return t


def t_NOMBRE_EQUIPO(t):
    r'"nombre_equipo"'
    return t


def t_ALIANZA_EQUIPO(t):
    r'"alianza_equipo"'
    return t


def t_FECHA_INICIO(t):
    r'"fecha_inicio"'
    return t


def t_FECHA_FIN(t):
    r'"fecha_fin"'
    return t


def t_FIRMA_DIGITAL(t):
    r'"firma_digital"'
    return t


def t_VERSION(t):
    r'"version"'
    return t


def t_DIRECCION(t):
    r'"direccion"'
    return t


def t_INTEGRANTES(t):
    r'"integrantes"'
    return t


def t_PROYECTOS(t):
    r'"proyectos"'
    return t


def t_HABILIDADES(t):
    r'"habilidades"'
    return t


def t_ASIGNATURA(t):
    r'"asignatura"'
    return t


def t_CARRERA(t):
    r'"carrera"'
    return t


def t_EQUIPOS(t):
    r'"equipos"'
    return t


def t_CALLE(t):
    r'"calle"'
    return t


def t_CIUDAD(t):
    r'"ciudad"'
    return t


def t_PAIS(t):
    r'"pais"'
    return t


def t_TAREAS(t):
    r'"tareas"'
    return t


def t_VIDEO(t):
    r'"video"'
    return t


def t_CONCLUSION(t):
    r'"conclusion"'
    return t


def t_RESUMEN(t):
    r'"resumen"'
    return t


def t_ESTADO(t):
    r'"estado"'
    return t


def t_NOMBRE(t):
    r'"nombre"'
    return t


def t_EDAD(t):
    r'"edad"'
    return t


def t_CARGO(t):
    r'"cargo"'
    return t


def t_FOTO(t):
    r'"foto"'
    return t


def t_EMAIL(t):
    r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}"'
    return t


def t_SALARIO(t):
    r'"salario"'
    return t


def t_ACTIVO(t):
    r'"activo"'
    return t


def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t


def t_A_STRING(t):
    r'"[^"]*"'
    return t


# Ignorar espacios y tabs
t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Carácter ilegal: {t.value[0]}")
    t.lexer.skip(1)


# Construir el lexer
lexer = lex.lex()


# Función para validar claves (modificada)
def validar_clave(clave_cruda):
    """Valida si una clave es válida según las reglas del parser"""
    global has_errors

    # Lista de claves válidas
    claves_validas = [
        'nombre_equipo', 'identidad_equipo', 'carrera', 'asignatura', 'universidad_regional',
        'alianza_equipo', 'direccion', 'integrantes', 'proyectos', 'calle', 'ciudad', 'pais',
        'nombre', 'edad', 'cargo', 'foto', 'email', 'habilidades', 'salario', 'activo',
        'estado', 'resumen', 'fecha_inicio', 'fecha_fin', 'video', 'conclusion', 'tareas',
        'version', 'firma_digital', 'equipos', 'link'
    ]

    clave = clave_cruda.strip('"')

    if clave not in claves_validas:
        mostrar_error(f"❌ Clave inválida detectada: {clave}")
        has_errors = True
        return False

    return True

# Función para validar links (modificada)
def validar_link(link_crudo):
    """Valida si un link tiene formato válido"""
    global has_errors

    link = link_crudo.strip('"')

    # Verificar que comience con http:// o https://
    if not (link.startswith('http://') or link.startswith('https://')):
        mostrar_error(f"❌ Link inválido detectado: {link}")
        has_errors = True
        return False

    # Verificar que tenga al menos un dominio básico
    if '.' not in link or len(link) < 10:
        mostrar_error(f"❌ Link inválido detectado: {link}")
        has_errors = True
        return False

    # Verificar que no contenga caracteres inválidos en la URL
    if ';' in link:
        mostrar_error(f"❌ Link inválido detectado (contiene ';'): {link}")
        has_errors = True
        return False

    # Verificar estructura básica del dominio
    partes = link.split('/')
    if len(partes) < 3:
        mostrar_error(f"❌ Link inválido detectado: {link}")
        has_errors = True
        return False

    dominio = partes[2]

    # Verificar que el dominio no termine con caracteres extraños
    if dominio.endswith('an') or dominio.endswith('coman'):
        mostrar_error(f"❌ Link inválido detectado (dominio malformado): {link}")
        has_errors = True
        return False

    # Verificar que el dominio tenga al menos un punto y una extensión válida
    if '.' not in dominio:
        mostrar_error(f"❌ Link inválido detectado (dominio sin extensión): {link}")
        has_errors = True
        return False

    return True


def validar_numero_segun_contexto(clave, valor):
    """Valida números según el contexto del campo"""
    global has_errors

    # Campos que requieren enteros
    campos_enteros = ['edad']

    # Campos que pueden ser float
    campos_float = ['salario', 'version']

    if clave in campos_enteros:
        if isinstance(valor, float):
            mostrar_error(f"❌ {clave.capitalize()} inválida: {valor} (debe ser un número entero)")
            has_errors = True
            return None
        elif isinstance(valor, int):
            if clave == 'edad' and (valor < 0 or valor > 150):
                mostrar_error(f"❌ Edad inválida: {valor} (debe estar entre 0 y 150)")
                has_errors = True
                return None

    elif clave in campos_float:
        if isinstance(valor, (int, float)):
            if clave == 'salario' and valor < 0:
                mostrar_error(f"❌ Salario inválido: {valor} (debe ser mayor o igual a 0)")
                has_errors = True
                return None

    return valor

# Reglas de gramática
def p_json(p):
    '''json : LLAVE_ABRE contenido_json LLAVE_CIERRA'''
    p[0] = p[2]


def p_contenido_json(p):
    '''contenido_json : equipos
                      | equipos COMA version
                      | equipos COMA firma_digital
                      | equipos COMA version COMA firma_digital
                      | equipos COMA firma_digital COMA version
                      | version COMA equipos
                      | version COMA equipos COMA firma_digital
                      | firma_digital COMA equipos
                      | firma_digital COMA equipos COMA version
                      | version COMA firma_digital COMA equipos
                      | firma_digital COMA version COMA equipos'''
    if len(p) == 2:
        p[0] = {"equipos": p[1]}
    elif len(p) == 4:
        if isinstance(p[1], list):
            p[0] = {"equipos": p[1]}
            p[0].update(p[3])
        else:
            p[0] = p[1]
            p[0]["equipos"] = p[3]
    else:
        result = {}
        for item in [p[1], p[3], p[5]]:
            if isinstance(item, list):
                result["equipos"] = item
            else:
                result.update(item)
        p[0] = result


def p_equipos(p):
    '''equipos : EQUIPOS DOS_PUNTOS CORCHETE_ABRE lista_equipos CORCHETE_CIERRA'''
    p[0] = p[4]


def p_lista_equipos(p):
    '''lista_equipos : equipo
                     | lista_equipos COMA equipo'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_equipo(p):
    '''equipo : LLAVE_ABRE campos_equipo LLAVE_CIERRA'''
    p[0] = p[2]


def p_campos_equipo(p):
    '''campos_equipo : campo_equipo
                     | campos_equipo COMA campo_equipo'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}


def p_campo_equipo(p):
    '''campo_equipo : NOMBRE_EQUIPO DOS_PUNTOS valor_simple
                    | IDENTIDAD_EQUIPO DOS_PUNTOS valor_simple
                    | CARRERA DOS_PUNTOS valor_simple
                    | ASIGNATURA DOS_PUNTOS valor_simple
                    | UNIVERSIDAD_REGIONAL DOS_PUNTOS valor_simple
                    | ALIANZA_EQUIPO DOS_PUNTOS valor_simple
                    | A_STRING DOS_PUNTOS valor_simple
                    | DIRECCION DOS_PUNTOS LLAVE_ABRE campos_direccion LLAVE_CIERRA
                    | INTEGRANTES DOS_PUNTOS CORCHETE_ABRE lista_integrantes CORCHETE_CIERRA
                    | PROYECTOS DOS_PUNTOS CORCHETE_ABRE lista_proyectos CORCHETE_CIERRA'''
    if len(p) == 4:
        # Validar clave si es A_STRING
        if p[1].startswith('"') and p[1].endswith('"'):
            if not validar_clave(p[1]):
                p[0] = {}
                return

        key = p[1].strip('"')
        value = p[3]

        # Validación de números según contexto
        if isinstance(value, (int, float)):
            validated_value = validar_numero_segun_contexto(key, value)
            if validated_value is None:
                p[0] = {}
                return
            value = validated_value

        # Validar link si el valor es LINK
        if hasattr(value, 'startswith') and value.startswith('"http'):
            if not validar_link(value):
                p[0] = {}
                return

        p[0] = {key: value}
    elif len(p) == 6:
        if p[1] == '"direccion"':
            p[0] = {"direccion": p[4]}
        elif p[1] == '"integrantes"':
            p[0] = {"integrantes": p[4]}
        elif p[1] == '"proyectos"':
            p[0] = {"proyectos": p[4]}


def p_valor_simple(p):
    '''valor_simple : A_STRING
                    | LINK
                    | EMAIL
                    | NUMBER
                    | TRUE
                    | FALSE
                    | NULL
                    | DATE'''
    if p[1] == 'true':
        p[0] = True
    elif p[1] == 'false':
        p[0] = False
    elif p[1] == 'null':
        p[0] = None
    elif isinstance(p[1], str) and p[1].startswith('"'):
        # Validar si es un link
        if p[1].startswith('"http'):
            if not validar_link(p[1]):
                p[0] = None
                return
        p[0] = p[1].strip('"')
    else:
        p[0] = p[1]


def p_campos_direccion(p):
    '''campos_direccion : campo_direccion
                        | campos_direccion COMA campo_direccion'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}


def p_campo_direccion(p):
    '''campo_direccion : CALLE DOS_PUNTOS valor_simple
                       | CIUDAD DOS_PUNTOS valor_simple
                       | PAIS DOS_PUNTOS valor_simple'''
    key = p[1].strip('"')
    p[0] = {key: p[3]}


def p_lista_integrantes(p):
    '''lista_integrantes : integrante
                         | lista_integrantes COMA integrante'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_integrante(p):
    '''integrante : LLAVE_ABRE campos_integrante LLAVE_CIERRA'''
    p[0] = p[2]


def p_campos_integrante(p):
    '''campos_integrante : campo_integrante
                         | campos_integrante COMA campo_integrante'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}


def p_campo_integrante(p):
    '''campo_integrante : NOMBRE DOS_PUNTOS valor_simple
                        | EDAD DOS_PUNTOS valor_simple
                        | CARGO DOS_PUNTOS valor_simple
                        | FOTO DOS_PUNTOS valor_simple
                        | EMAIL DOS_PUNTOS campo_email
                        | HABILIDADES DOS_PUNTOS valor_simple
                        | SALARIO DOS_PUNTOS valor_simple
                        | ACTIVO DOS_PUNTOS valor_simple
                        | A_STRING DOS_PUNTOS valor_simple'''

    # Validar clave si es A_STRING
    if p[1].startswith('"') and p[1].endswith('"'):
        if not validar_clave(p[1]):
            p[0] = {}
            return

    key = p[1].strip('"')
    value = p[3]

    # Validación de números según contexto
    if isinstance(value, (int, float)):
        validated_value = validar_numero_segun_contexto(key, value)
        if validated_value is None:
            p[0] = {}
            return
        value = validated_value

    # Validación de email si la clave es "email"
    if key == "email":
        import re
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
        if not re.match(patron, value.strip('"')):
            mostrar_error(f"❌ Email inválido detectado: {value}")
            global has_errors
            has_errors = True
            value = None

    # Validar si el valor es un link
    if hasattr(value, 'startswith') and value.startswith('"http'):
        if not validar_link(value):
            value = None

    p[0] = {key: value}


def p_campo_email(p):
    '''campo_email : EMAIL DOS_PUNTOS A_STRING'''
    email_val = p[3].strip('"')

    import re
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'

    if re.match(patron, email_val):
        p[0] = ("email", email_val)
    else:
        mostrar_error(f"❌ Email inválido: {email_val}")
        global has_errors
        has_errors = True
        p[0] = ("email", None)

def p_lista_proyectos(p):
    '''lista_proyectos : proyecto
                       | lista_proyectos COMA proyecto'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_proyecto(p):
    '''proyecto : LLAVE_ABRE campos_proyecto LLAVE_CIERRA'''
    p[0] = p[2]


def p_campos_proyecto(p):
    '''campos_proyecto : campo_proyecto
                       | campos_proyecto COMA campo_proyecto'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}


def p_campo_proyecto(p):
    '''campo_proyecto : NOMBRE DOS_PUNTOS valor_simple
                      | ESTADO DOS_PUNTOS valor_simple
                      | RESUMEN DOS_PUNTOS valor_simple
                      | FECHA_INICIO DOS_PUNTOS valor_simple
                      | FECHA_FIN DOS_PUNTOS valor_simple
                      | VIDEO DOS_PUNTOS valor_simple
                      | CONCLUSION DOS_PUNTOS valor_simple
                      | A_STRING DOS_PUNTOS valor_simple
                      | TAREAS DOS_PUNTOS CORCHETE_ABRE lista_tareas CORCHETE_CIERRA'''

    if len(p) == 4:
        # Validar clave si es A_STRING
        if p[1].startswith('"') and p[1].endswith('"'):
            if not validar_clave(p[1]):
                p[0] = {}
                return

        key = p[1].strip('"')
        value = p[3]

        # Validar link si el valor es LINK
        if hasattr(value, 'startswith') and value.startswith('"http'):
            if not validar_link(value):
                print(f"❌ Link inválido detectado: {value}")
                global has_errors
                has_errors = True
                value = None

        # Validación de estado si corresponde
        if key == "estado":
            estados_validos = {
                "to do", "in progress", "canceled", "done", "on hold"
            }
            if value.lower() not in estados_validos:
                print(f"❌ Estado inválido detectado: {value}")
                has_errors = True
                value = None

        p[0] = {key: value}
    else:
        p[0] = {"tareas": p[4]}


def p_lista_tareas(p):
    '''lista_tareas : tarea
                    | lista_tareas COMA tarea'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_tarea(p):
    '''tarea : LLAVE_ABRE campos_tarea LLAVE_CIERRA'''
    p[0] = p[2]


def p_campos_tarea(p):
    '''campos_tarea : campo_tarea
                    | campos_tarea COMA campo_tarea'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}


def p_campo_tarea(p):
    '''campo_tarea : NOMBRE DOS_PUNTOS valor_simple
                   | ESTADO DOS_PUNTOS valor_simple
                   | RESUMEN DOS_PUNTOS valor_simple
                   | FECHA_INICIO DOS_PUNTOS valor_simple
                   | FECHA_FIN DOS_PUNTOS valor_simple
                   | A_STRING DOS_PUNTOS valor_simple'''

    if p[1].startswith('"') and p[1].endswith('"'):
        if not validar_clave(p[1]):
            p[0] = {}
            return

    key = p[1].strip('"')
    value = p[3]

    # Validar link si el valor es un link
    if hasattr(value, 'startswith') and value.startswith('"http'):
        if not validar_link(value):
            print(f"❌ Link inválido detectado: {value}")
            global has_errors
            has_errors = True
            value = None

    # Validar estado si la clave es "estado"
    if key == "estado":
        estados_validos = {
            "to do", "in progress", "canceled", "done", "on hold"
        }
        if value.lower() not in estados_validos:
            print(f"❌ Estado inválido detectado: {value}")
            has_errors = True
            value = None
    p[0] = {key: value}


def p_version(p):
    '''version : VERSION DOS_PUNTOS valor_simple'''
    value = p[3]

    # Validar que version sea un número válido
    if isinstance(value, (int, float)):
        validated_value = validar_numero_segun_contexto('version', value)
        if validated_value is None:
            p[0] = {"version": None}
            return
        value = validated_value

    p[0] = {"version": value}


def p_firma_digital(p):
    '''firma_digital : FIRMA_DIGITAL DOS_PUNTOS valor_simple'''
    p[0] = {"firma_digital": p[3]}


def p_error(p):
    global has_errors
    has_errors = True
    error_msg = ""

    if p:
        error_msg = f"❌ Error de sintaxis en token {p.type} (valor: {p.value}) línea {p.lineno}\n"
        print(error_msg.strip())  # Mantener print para consola
    else:
        error_msg = "❌ Error de sintaxis: Fin inesperado del archivo\n"
        print(error_msg.strip())  # Mantener print para consola

    # Mostrar error en el widget analisislex si existe
    try:
        analisislex.insert(tk.END, error_msg)
        analisislex.see(tk.END)  # Scroll automático al final
    except NameError:
        # Si analisislex no está definido (ejecución por línea de comandos)
        pass

def mostrar_error(mensaje):
    """Función auxiliar para mostrar errores tanto en consola como en el widget tkinter"""
    print(mensaje)
    try:
        analisislex.insert(tk.END, mensaje + "\n")
        analisislex.see(tk.END)  # Scroll automático al final
    except NameError:
        # Si analisislex no está definido (ejecución por línea de comandos)
        pass


# Construir el parser
parser = yacc.yacc(debug=False)


# Función para imprimir JSON sin usar librería json
def imprimir_json(obj, indent=0):
    """Función para imprimir JSON sin usar la librería json"""
    espacios = "  " * indent

    if isinstance(obj, dict):
        print(f"{espacios}{{")
        items = list(obj.items())
        for i, (key, value) in enumerate(items):
            print(f"{espacios}  \"{key}\": ", end="")
            if isinstance(value, (dict, list)):
                print()
                imprimir_json(value, indent + 1)
            else:
                if isinstance(value, str):
                    print(f"\"{value}\"", end="")
                elif isinstance(value, bool):
                    print("true" if value else "false", end="")
                elif value is None:
                    print("null", end="")
                else:
                    print(value, end="")

            if i < len(items) - 1:
                print(",")
            else:
                print()
        print(f"{espacios}}}")

    elif isinstance(obj, list):
        print(f"{espacios}[")
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                imprimir_json(item, indent + 1)
            else:
                if isinstance(item, str):
                    print(f"{espacios}  \"{item}\"", end="")
                elif isinstance(item, bool):
                    print(f"{espacios}  {'true' if item else 'false'}", end="")
                elif item is None:
                    print(f"{espacios}  null", end="")
                else:
                    print(f"{espacios}  {item}", end="")

            if i < len(obj) - 1:
                print(",")
            else:
                print()
        print(f"{espacios}]")


# Función para imprimir JSON en el widget analisislex sin usar json
def imprimir_json_en_tk(obj, indent=0):
    espacios = "  " * indent
    if isinstance(obj, dict):
        analisislex.insert(tk.INSERT, f"{espacios}{{\n")
        items = list(obj.items())
        for i, (key, value) in enumerate(items):
            analisislex.insert(tk.INSERT, f"{espacios}  \"{key}\": ")
            if isinstance(value, (dict, list)):
                analisislex.insert(tk.INSERT, "\n")
                imprimir_json_en_tk(value, indent + 1)
            else:
                if isinstance(value, str):
                    analisislex.insert(tk.INSERT, f'"{value}"')
                elif isinstance(value, bool):
                    analisislex.insert(tk.INSERT, "true" if value else "false")
                elif value is None:
                    analisislex.insert(tk.INSERT, "null")
                else:
                    analisislex.insert(tk.INSERT, str(value))
            if i < len(items) - 1:
                analisislex.insert(tk.INSERT, ",\n")
            else:
                analisislex.insert(tk.INSERT, "\n")
        analisislex.insert(tk.INSERT, f"{espacios}}}\n")
    elif isinstance(obj, list):
        analisislex.insert(tk.INSERT, f"{espacios}[\n")
        for i, item in enumerate(obj):
            if isinstance(item, (dict, list)):
                imprimir_json_en_tk(item, indent + 1)
            else:
                if isinstance(item, str):
                    analisislex.insert(tk.INSERT, f'{espacios}  "{item}"')
                elif isinstance(item, bool):
                    analisislex.insert(tk.INSERT, f"{espacios}  {'true' if item else 'false'}")
                elif item is None:
                    analisislex.insert(tk.INSERT, f"{espacios}  null")
                else:
                    analisislex.insert(tk.INSERT, f"{espacios}  {item}")
            if i < len(obj) - 1:
                analisislex.insert(tk.INSERT, ",\n")
            else:
                analisislex.insert(tk.INSERT, "\n")
        analisislex.insert(tk.INSERT, f"{espacios}]\n")


# Función para generar HTML
def generar_html_y_mostrar_codigo(data, nombre_archivo):
    """Genera un archivo HTML y muestra el código HTML en el widget analisislex"""

    # Generar el código HTML
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Equipos y Proyectos</title>
    <style>
        .equipo {
            border: 1px solid gray;
            padding: 20px;
            margin: 10px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
"""

    if "equipos" in data:
        for equipo in data["equipos"]:
            html += f'<div class="equipo">\n'
            html += f'<h1>{equipo.get("nombre_equipo", "")}</h1>\n'

            # Datos del equipo
            if "asignatura" in equipo:
                html += f'<p><strong>Asignatura:</strong> {equipo["asignatura"]}</p>\n'
            if "carrera" in equipo:
                html += f'<p><strong>Carrera:</strong> {equipo["carrera"]}</p>\n'
            if "universidad_regional" in equipo:
                html += f'<p><strong>Universidad:</strong> {equipo["universidad_regional"]}</p>\n'
            if "link" in equipo and equipo["link"]:
                html += f'<p><strong>Link:</strong> <a href="{equipo["link"]}">{equipo["link"]}</a></p>\n'
            if "alianza_equipo" in equipo:
                html += f'<p><strong>Alianza:</strong> {equipo["alianza_equipo"]}</p>\n'

            # Integrantes
            if "integrantes" in equipo:
                html += '<h2>Integrantes</h2>\n<ul>\n'
                for integrante in equipo["integrantes"]:
                    html += f'<li><strong>{integrante.get("nombre", "")}</strong>\n'
                    html += '<ul>\n'
                    if "edad" in integrante:
                        html += f'<li>Edad: {integrante["edad"]}</li>\n'
                    if "cargo" in integrante:
                        html += f'<li>Cargo: {integrante["cargo"]}</li>\n'
                    if "email" in integrante:
                        html += f'<li>Email: {integrante["email"]}</li>\n'
                    if "foto" in integrante:
                        html += f'<li>Foto: <a href="{integrante["foto"]}">{integrante["foto"]}</a></li>\n'
                    if "habilidades" in integrante:
                        html += f'<li>Habilidades: {integrante["habilidades"]}</li>\n'
                    if "salario" in integrante:
                        html += f'<li>Salario: {integrante["salario"]}</li>\n'
                    if "activo" in integrante:
                        html += f'<li>Activo: {integrante["activo"]}</li>\n'
                    html += '</ul>\n'
                    html += '</li>\n'
                html += '</ul>\n'

            # Proyectos
            if "proyectos" in equipo:
                for proyecto in equipo["proyectos"]:
                    html += f'<h3>{proyecto.get("nombre", "")}</h3>\n'
                    html += '<ul>\n'
                    if "estado" in proyecto:
                        html += f'<li>Estado: {proyecto["estado"]}</li>\n'
                    if "resumen" in proyecto:
                        html += f'<li>Resumen: {proyecto["resumen"]}</li>\n'
                    if "fecha_inicio" in proyecto:
                        html += f'<li>Fecha Inicio: {proyecto["fecha_inicio"]}</li>\n'
                    if "fecha_fin" in proyecto:
                        html += f'<li>Fecha Fin: {proyecto["fecha_fin"]}</li>\n'
                    if "video" in proyecto:
                        html += f'<li>Video: <a href="{proyecto["video"]}">{proyecto["video"]}</a></li>\n'
                    if "conclusion" in proyecto:
                        html += f'<li>Conclusión: {proyecto["conclusion"]}</li>\n'
                    html += '</ul>\n'

                    # Tareas como tabla
                    if "tareas" in proyecto:
                        html += '<table>\n'
                        html += '<tr><th>Nombre</th><th>Estado</th><th>Resumen</th><th>Fecha Inicio</th><th>Fecha Fin</th></tr>\n'
                        for tarea in proyecto["tareas"]:
                            html += '<tr>\n'
                            html += f'<td>{tarea.get("nombre", "")}</td>\n'
                            html += f'<td>{tarea.get("estado", "")}</td>\n'
                            html += f'<td>{tarea.get("resumen", "")}</td>\n'
                            html += f'<td>{tarea.get("fecha_inicio", "")}</td>\n'
                            html += f'<td>{tarea.get("fecha_fin", "")}</td>\n'
                            html += '</tr>\n'
                        html += '</table>\n'

            html += '</div>\n'

    html += """
</body>
</html>
"""

    # Guardar archivo HTML
    nombre_html = nombre_archivo.replace('.json', '.html')
    with open(nombre_html, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Archivo HTML generado: {nombre_html}")

    # Mostrar el código HTML en el widget analisislex
    analisislex.delete(1.0, tk.END)
    analisislex.insert(tk.END, html)

# Función modificada para seleccionar JSON que muestre el HTML
def seleccionarjson_con_html():
    global ruta_json_global, has_errors
    ruta_json_global = tk.filedialog.askopenfilename(
        filetypes=[('Archivos JSON', '*.json'), ('Todos los archivos', '*.*')])
    if ruta_json_global:
        # Limpiar widget de análisis
        analisislex.delete(1.0, tk.END)

        # Resetear flag de errores
        has_errors = False

        with open(ruta_json_global, 'r', encoding='utf-8') as file_obj:
            data = file_obj.read()
            textojson.delete(1.0, tk.END)
            textojson.insert(tk.INSERT, data)

        try:
            # Analizar con el parser
            result = parser.parse(data, lexer=lexer)

            if result and not has_errors:
                print("✅ Análisis exitoso!")
                # Generar HTML y mostrar código en widget
                generar_html_y_mostrar_codigo(result, ruta_json_global)
            else:
                if not has_errors:
                    analisislex.insert(tk.END, "❌ Error en el análisis del JSON\n")
                analisislex.insert(tk.END, "❌ No se pudo generar el HTML\n")
                analisislex.see(tk.END)  # Scroll automático al final

        except Exception as e:
            analisislex.insert(tk.END, f"❌ Error: {e}\n")
            analisislex.insert(tk.END, "❌ No se pudo procesar el archivo\n")
            analisislex.see(tk.END)  # Scroll automático al final

        # Alimento el lexer con el contenido extraído (solo si no hay errores críticos)
        if not has_errors:
            lexer.input(data)

            # contador de tokens generados
            token_count = 0

            # Procesamiento de tokens generados
            file = open("LexAnalysis.txt", "w")
            while True:
                tok = lexer.token()
                if not tok:
                    break
                file.write(tok.type), file.write(" ")  # ESCRIBO EN TXT EXTERNO
                file.write(str(tok.value)), file.write(" ")
                file.write(str(tok.lineno)), file.write(" ")
                file.write(str(tok.lexpos)), file.write("\n")

                token_count += 1  # Incrementar contador de tokens procesados

            if token_count > 0:
                token_msg = f"\n¡Procesamiento exitoso! Se generaron {token_count} tokens."
                file.write(token_msg)
                analisislex.insert(tk.END, token_msg)
            else:
                error_msg = "\nError: No se generaron tokens. Verifica el formato del JSON."
                file.write(error_msg)
                analisislex.insert(tk.END, error_msg)

            # Mensaje final
            if token_count > 0:
                print(f"\n✅¡Procesamiento exitoso! Se generaron {token_count} tokens.")
                print("\n✅Se generó el archivo LexAnalysis.txt en la carpeta para el análisis léxico.")
            else:
                print("\nError: No se generaron tokens. Verifica el formato del JSON.")
            file.close()
        else:
            analisislex.insert(tk.END, "\n❌ Se encontraron errores. No se generaron tokens.\n")
            analisislex.see(tk.END)


# Crear ventana con Tkinter

ventana = tk.Tk()  # VENTANA PRINCIPAL
ventana.title("Lexer - Los Semánticos")
ventana.geometry("1280x650+30+20")
ventana.configure(bg="oldlace")
ventana.iconbitmap("semanticoslogov2.ico")

imagenfondo = Image.open("fondolexer.jpg")
fondo = ImageTk.PhotoImage(imagenfondo)

labelfondo = tk.Label(ventana, image=fondo)  # LABEL FONDO
labelfondo.place(x=0, y=0, relwidth=1, relheight=1)

button = tk.Button(ventana, text="Seleccionar JSON")  # BOTON SELECCIONAR ARCHIVO
button.config(fg="black", bg="lightblue", font=("Arial", 12))
button.pack(side="top", padx=10, pady=50)

label1 = tk.LabelFrame(ventana, text="Contenido JSON", bg="white", labelanchor="n")  # LABEL CONTENIDO JSON
label1.configure(width=600, height=570)
label1.pack(side="left", padx=10)

analisislabel2 = tk.LabelFrame(ventana, text="Código HTML", bg="white", labelanchor="n")  # LABEL ANALISIS LEXICO
analisislabel2.configure(width=600, height=570)
analisislabel2.pack(side="right", padx=10)

textojson = tk.Text(label1, wrap='word')
textojson.pack(expand=True, fill='both')

analisislex = tk.Text(analisislabel2, wrap='word')
analisislex.pack(expand=True, fill='both')

button.config(command=seleccionarjson_con_html)

ventana.mainloop()
