from models import CAMPOS_ESTUDIANTE
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota, obtener_promedio, estudiantes_en_comun, estadisticas
)


def pausa():
    input("\nPresione Enter para continuar...")


def mostrar_tabla(estudiantes):
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}{'NOTAS':<12}{'MATERIAS':<20}")
    print("-" * 85)
    for estudiante in estudiantes:
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.carnet:<15}{str(estudiante.notas):<12}{str(estudiante.materias):<20}")
    print("-" * 85)
    imprimir_info(f"Total: {len(estudiantes)} cliente(s)")


# ---------- C · CREAR ----------
def opcion_crear():
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    # Recorro la TUPLA de campos: si mañana agrego un campo al Modelo,
    # este formulario se actualiza solo.
    datos = {}
    for campo in ("nombre", "apellido", "email", "carnet"):
        datos[campo] = input(f"{campo.capitalize()}: ")

    exito, mensaje = crear_estudiante(datos)          # desempaqueto la TUPLA que devuelve
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- R · LEER TODOS ----------
def opcion_ver_todos():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    estudiantes = obtener_todos()
    if not estudiantes:
        imprimir_info("Todavía no hay estudiantes. Use la opción 1 para crear el primero.")
    else:
        mostrar_tabla(estudiantes)
    pausa()


# ---------- S · BUSCAR ----------
def opcion_buscar():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, email o carnet: ")
    encontrados = buscar_estudiantes(termino)

    if not encontrados:
        imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
    else:
        mostrar_tabla(encontrados)
    pausa()


# ---------- R · LEER UNO ----------
def opcion_ver_por_id():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        # Recorro el DICCIONARIO del cliente: clave y valor a la vez
        for clave, valor in estudiante.a_diccionario().items():
            print(f"  {clave.capitalize():<12}: {valor}")
    pausa()


# ---------- U · ACTUALIZAR ----------
def opcion_actualizar():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un cliente con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Editando a {estudiante.obtener_nombre_completo()}")
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Armo un DICCIONARIO solo con lo que el usuario escribió
    cambios = {}
    campos_excluidos = ["notas", "materias"]
    for campo in CAMPOS_ESTUDIANTE:
        if campo not in campos_excluidos:
            actual = getattr(estudiante, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()


# ---------- D · ELIMINAR ----------
def opcion_eliminar():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()

    estudiante = obtener_por_id(id_estudiante)
    if not estudiante:
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        return pausa()

    imprimir_info(f"Se eliminará: {estudiante}")
    if confirmar("¿Confirma la eliminación?"):
        exito, mensaje = eliminar_estudiante(id_estudiante)
        if exito:
            imprimir_exito(mensaje)
        else:
            imprimir_error(mensaje)
    else:
        imprimir_info("Operación cancelada")
    pausa()

def agregar_nota_menu():
    imprimir_titulo("AGREGAR NOTA")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()
    materia = input("Ingrese la materia: ")
    try:
        nota = float(input("Ingrese la nota (0-20): "))
    except ValueError:
        imprimir_error("La nota debe ser un número.")
        pausa()
        return
    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    if exito:
        imprimir_exito(mensaje)
    else:
        imprimir_error(mensaje)
    pausa()

def ver_promedio():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_estudiante = int(input("Id del estudiante: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return pausa()
    exito, resultado = obtener_promedio(id_estudiante)
    if exito:
        imprimir_exito(f"El promedio del estudiante es: {resultado}")
    else:
        imprimir_error(resultado)
    pausa()
        
def materias_en_comun():
    imprimir_titulo("VER PROMEDIO")
    try:
        id_a = int(input("Id del primer estudiante: "))
        id_b = int(input("Id del segundo estudiante: "))
    except ValueError:
        imprimir_error("Los id deben ser números entero")
        return pausa()
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    if not exito:
        imprimir_error(resultado)
    elif resultado:
        imprimir_exito("Materias en común: " + ", ".join(sorted(resultado)))
    else:
        imprimir_info( "Los estudiantes no tienen materias en común." ) 
    pausa()

# ---------- EXTRA · ESTADÍSTICAS ----------
def opcion_estadisticas():
    imprimir_titulo("ESTADÍSTICAS")
    datos = estadisticas()
    print(f"  Estudiantes registrados : {datos['total']}")
    print(f"  Materias distintas   : {len(datos['materias'])} -> {', '.join(datos['materias'])}")
    print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
    print(f"  Sin notas         : {len(datos['sin_notas'])}")
    pausa()


def salir():
    imprimir_info("¡Hasta luego! 👋")
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "8": ("Agregar nota", agregar_nota_menu),
    "9": ("Ver promedio", ver_promedio),
    "10": ("Estadísticas", opcion_estadisticas),
    "11": ("Materias en comun", materias_en_comun),
    "0": ("Salir", salir),
}


def mostrar_menu():
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    for tecla, (texto, _funcion) in OPCIONES.items():
        print(f"  {tecla}. {texto}")
    print()


def main():
    while True:
        mostrar_menu()
        tecla = input("Seleccione una opción: ").strip()

        if tecla not in OPCIONES:          # búsqueda instantánea por clave
            imprimir_error("Opción no válida")
            pausa()
            continue

        _texto, funcion = OPCIONES[tecla]
        if funcion() == "salir":
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")