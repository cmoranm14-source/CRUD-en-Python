# Importa el módulo estándar 'json', que sirve para convertir datos de Python
# (diccionarios, listas, textos, números) a texto JSON y viceversa.
import json

CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet", "notas", "materias")
# Define la clase Estudiante. Además de datos personales, usa dos estructuras
# de datos: un DICCIONARIO DE LISTAS (notas) y un CONJUNTO (materias).
class Estudiante:
    """Representa a un estudiante, sus materias y sus calificaciones.

    La clase usa un diccionario de listas para almacenar notas por materia y
    un conjunto para evitar materias duplicadas.
    """

    # Constructor. 'notas' y 'materias' tienen valor por defecto None, así que
    # son OPCIONALES: se puede crear Estudiante(1, "Ana", "Pérez", "a@x.com", "EST1").
    # Se usa None (y no {} o set()) porque un valor por defecto mutable se
    # COMPARTIRÍA entre todos los estudiantes creados: un error clásico de Python.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        """Crea un estudiante con sus datos académicos iniciales.

        Args:
            id_estudiante: Identificador único del estudiante.
            nombre: Nombres del estudiante.
            apellido: Apellidos del estudiante.
            email: Dirección de correo electrónico del estudiante.
            carnet: Código o carnet académico del estudiante.
            notas: Diccionario opcional con materias y listas de notas.
            materias: Colección opcional de materias inscritas.
        """
        # Guarda el identificador único del estudiante.
        self.id = id_estudiante
        # Guarda los nombres.
        self.nombre = nombre
        # Guarda los apellidos.
        self.apellido = apellido
        # Guarda el correo electrónico.
        self.email = email
        # Guarda el carnet (código académico).
        self.carnet = carnet                      # ej: EST2026001
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        # Expresión condicional: si llegaron notas se usan; si no (None o
        # vacío) se crea un diccionario vacío NUEVO para este estudiante.
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito, sin repetidos
        # set(materias) convierte cualquier colección (lista, tupla, set) en
        # conjunto, eliminando duplicados. Si no llegó nada, set() vacío.
        self.materias = set(materias) if materias else set()

    # Igual que en Cliente: une nombre y apellido en un solo texto.
    def obtener_nombre_completo(self):
        """Une el nombre y el apellido del estudiante.

        Returns:
            El nombre completo formado por el nombre y el apellido.
        """
        # Ej: "Ana Pérez"
        return f"{self.nombre} {self.apellido}"

    # Agrega una materia al conjunto de materias del estudiante.
    def inscribir_materia(self, materia):
        """Inscribe al estudiante en una materia.

        Args:
            materia: Nombre de la materia que se desea agregar.

        La materia se guarda en un conjunto, por lo que agregarla varias veces
        no crea registros repetidos.
        """
        # add() no duplica: si ya estaba inscrito, no pasa nada
        self.materias.add(materia)

    # Registra una calificación en una materia.
    def agregar_nota(self, materia, nota):
        """Registra una nota y asegura la inscripción en la materia.

        Args:
            materia: Nombre de la materia asociada a la nota.
            nota: Calificación que se agregará a la lista de notas.
        """
        # Primero se asegura de que el estudiante esté inscrito en la materia
        # (reutiliza el método anterior; si ya estaba, no pasa nada).
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        # Paso a paso:
        #   1) self.notas.setdefault(materia, []) -> devuelve la lista de esa
        #      materia; si no existía, crea la clave con [] y devuelve esa lista.
        #   2) .append(nota) -> agrega la nota al final de esa lista.
        # Ej: {} -> {"Matemática": [18]} -> {"Matemática": [18, 19]}
        self.notas.setdefault(materia, []).append(nota)

    # Calcula el promedio general juntando las notas de TODAS las materias.
    def obtener_promedio(self):
        """Calcula el promedio de todas las notas del estudiante.

        Returns:
            Promedio de todas las calificaciones redondeado a dos decimales.
            Devuelve `0` si todavía no existen notas registradas.
        """
        # Lista donde se juntarán todas las notas, sin importar la materia.
        # Al final queda una lista plana de números, ej: [18, 19, 17]
        todas = []
        # self.notas.values() recorre solo las LISTAS de notas del diccionario.
        # Si self.notas = {"Matemática": [18, 19], "Inglés": [17]}
        # entonces lista_notas vale [18, 19] y luego [17].
        for lista_notas in self.notas.values():
            # extend() agrega CADA elemento de la lista (no la lista entera,
            # eso haría append). [] -> [18, 19] -> [18, 19, 17]
            todas.extend(lista_notas)
        # Una lista vacía se evalúa como False: si no hay notas, se devuelve 0
        # y así se evita dividir entre cero (len(todas) sería 0).
        if not todas:
            return 0
        # sum() suma todas las notas, len() cuenta cuántas hay; su división es
        # el promedio. round(..., 2) lo redondea a 2 decimales.
        # ¡OJO! 'return todas, round(...)' devuelve una TUPLA:
        #   ([18, 19, 17], 18.0)  y no solo el promedio 18.0 como dice el docstring.
        # Para devolver solo el promedio sería: return round(sum(todas) / len(todas), 2)
        return todas, round(sum(todas) / len(todas), 2)

    # Compara este estudiante con otro y devuelve las materias que comparten.
    def materias_en_comun(self, otro_estudiante):
        """Obtiene las materias que comparten dos estudiantes.

        Args:
            otro_estudiante: Segundo estudiante con quien se compararán las
                materias inscritas.

        Returns:
            Conjunto con las materias presentes en ambos estudiantes.
        """
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        # El operador & equivale a self.materias.intersection(otro_estudiante.materias).
        # Ej: {"Física", "Matemática"} & {"Matemática", "Programación"} -> {"Matemática"}
        return self.materias & otro_estudiante.materias

    # Convierte el estudiante en un diccionario listo para guardarse en JSON.
    def a_diccionario(self):
        """Convierte el estudiante a un diccionario compatible con JSON.

        Returns:
            Diccionario con los datos personales, notas y materias. Las
            materias se convierten en una lista ordenada porque JSON no admite
            conjuntos.
        """
        return {
            "id": self.id,              # identificador
            "nombre": self.nombre,      # nombres
            "apellido": self.apellido,  # apellidos
            "email": self.email,        # correo
            "carnet": self.carnet,      # código académico
            "notas": self.notas,        # el diccionario de listas SÍ es compatible con JSON
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            # sorted() recibe el conjunto y devuelve una LISTA en orden alfabético,
            # así el archivo siempre queda igual y es fácil de leer.
            "materias": sorted(self.materias),
        }

    # Constructor alternativo: reconstruye un Estudiante desde un diccionario
    # (por ejemplo, uno leído desde un archivo JSON).
    @classmethod
    def desde_diccionario(cls, datos):
        """Crea un estudiante a partir de un diccionario guardado.

        Args:
            datos: Diccionario con los datos del estudiante. Las notas y
                materias pueden faltar y, en ese caso, se usan valores vacíos.

        Returns:
            Una instancia de `Estudiante` reconstruida desde el diccionario.
        """
        # cls(...) equivale a Estudiante(...).
        return cls(
            # Campos obligatorios: se leen con [] (si faltan, lanza KeyError).
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            # Argumento por NOMBRE (keyword). Si no hay "notas", usa {}.
            notas=datos.get("notas", {}),
            # y al leer lo volvemos a convertir en set
            # En el JSON las materias están como lista; set() las regresa a conjunto.
            materias=set(datos.get("materias", [])),
        )

    def a_json(self):
            """Convierte los datos del cliente a una cadena de texto JSON.
    
            Returns:
                Texto JSON con la información del cliente.
            """
            # json.dumps ("dump string") convierte el diccionario a texto JSON.
            # ensure_ascii=False permite que tildes y ñ se vean tal cual
            # ("Pérez") en lugar de códigos como "Pérez".
            return json.dumps(self.a_diccionario(), ensure_ascii=False)
    
    # Se ejecuta automáticamente con print(estudiante) o str(estudiante).
    def __str__(self):
        """Devuelve una representación breve y legible del estudiante.

        Returns:
            Texto con el carnet, nombre completo y promedio del estudiante.
        """
        # Ej: "[EST2026001] Ana Pérez - Promedio: 18.0"
        # (Con el return actual de obtener_promedio se mostraría la tupla completa.)
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"
