import random
import time


# Generación de datos

def generar_estudiantes(ids):
    """Crea una lista de diccionarios con id, nombre y promedio."""
    nombres_base = ["Ana", "Carlos", "María", "Juan", "Pedro", "Luis", "Sofía", "Elena", "Diego", "Valentina"]
    estudiantes = []
    for id_val in ids:
        nombre = random.choice(nombres_base) + str(random.randint(1, 999))
        promedio = round(random.uniform(5.0, 10.0), 2)
        estudiantes.append({"id": id_val, "nombre": nombre, "promedio": promedio})
    return estudiantes

# Estructura 1: Lista desordenada (búsqueda lineal)
class ListaEstudiantes:
    """Implementa una estructura de lista simple para almacenar estudiantes y permite búsqueda lineal."""
    def __init__(self, estudiantes):
        """Inicializa la lista de estudiantes.

        Args:
            estudiantes (list): Una lista de diccionarios de estudiantes.
        """
        self.lista = estudiantes  # lista de diccionarios

    def buscar(self, id_buscar):
        """Busca un estudiante por su ID utilizando búsqueda lineal.

        Args:
            id_buscar (int): El ID del estudiante a buscar.

        Returns:
            dict or None: El diccionario del estudiante si se encuentra, de lo contrario None.
        """
        for est in self.lista:
            if est["id"] == id_buscar:
                return est
        return None

# Estructura 2: Árbol Binario de Búsqueda (ABB) - VERSIÓN ITERATIVA
class NodoABB:
    """Representa un nodo en el Árbol Binario de Búsqueda."""
    def __init__(self, estudiante):
        """Inicializa un nodo con un estudiante y punteros a hijos izquierdo y derecho.

        Args:
            estudiante (dict): El diccionario del estudiante a almacenar en el nodo.
        """
        self.est = estudiante
        self.izq = None
        self.der = None

class ABB:
    """Implementa un Árbol Binario de Búsqueda (ABB) con inserción y búsqueda iterativas."""
    def __init__(self):
        """Inicializa un ABB vacío."""
        self.raiz = None

    def insertar(self, estudiante):
        """Inserta un estudiante en el ABB de forma iterativa.

        Args:
            estudiante (dict): El diccionario del estudiante a insertar.
        """
        nuevo = NodoABB(estudiante)
        if self.raiz is None:
            self.raiz = nuevo
            return
        actual = self.raiz
        while True:
            if estudiante["id"] < actual.est["id"]:
                if actual.izq is None:
                    actual.izq = nuevo
                    break
                else:
                    actual = actual.izq
            else:
                if actual.der is None:
                    actual.der = nuevo
                    break
                else:
                    actual = actual.der

    def buscar(self, id_buscar):
        """Busca un estudiante por su ID en el ABB de forma iterativa.

        Args:
            id_buscar (int): El ID del estudiante a buscar.

        Returns:
            dict or None: El diccionario del estudiante si se encuentra, de lo contrario None.
        """
        actual = self.raiz
        while actual is not None:
            if id_buscar == actual.est["id"]:
                return actual.est
            elif id_buscar < actual.est["id"]:
                actual = actual.izq
            else:
                actual = actual.der
        return None


# Estructura 3: Árbol B+ (simplificado, orden=4)

class BPlusNode:
    """Representa un nodo genérico en un Árbol B+."""
    def __init__(self, leaf=False):
        """Inicializa un nodo B+.

        Args:
            leaf (bool): True si el nodo es una hoja, False si es un nodo interno.
        """
        self.leaf = leaf
        self.keys = []          # claves (ids)
        self.children = []       # para hoja: valores (diccionarios); para interno: nodos hijos
        self.next = None         # solo para hojas (siguiente hoja)

class BPlusTree:
    """Implementa una versión simplificada de un Árbol B+."""
    def __init__(self, order=4):
        """Inicializa un Árbol B+.

        Args:
            order (int): El orden máximo de claves por nodo.
        """
        self.root = BPlusNode(leaf=True)
        self.order = order       # máximo de claves por nodo

    def buscar(self, id_buscar):
        """Busca un estudiante por su ID en el Árbol B+.

        Args:
            id_buscar (int): El ID del estudiante a buscar.

        Returns:
            dict or None: El diccionario del estudiante si se encuentra, de lo contrario None.
        """
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys) and id_buscar >= node.keys[i]:
                i += 1
            node = node.children[i]
        # Buscar en la hoja
        for i, key in enumerate(node.keys):
            if key == id_buscar:
                return node.children[i]   # el valor asociado
        return None

    def insertar(self, id_val, estudiante):
        """Inserta un estudiante en el Árbol B+.

        Args:
            id_val (int): El ID del estudiante a insertar.
            estudiante (dict): El diccionario del estudiante a insertar.
        """
        root = self.root
        if len(root.keys) == self.order:   # raíz llena
            new_root = BPlusNode(leaf=False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, id_val, estudiante)

    def _insert_non_full(self, node, id_val, estudiante):
        """Método auxiliar para insertar en un nodo no lleno, manejando divisiones si es necesario.

        Args:
            node (BPlusNode): El nodo actual donde intentar la inserción.
            id_val (int): El ID del estudiante a insertar.
            estudiante (dict): El diccionario del estudiante a insertar.
        """
        if node.leaf:
            # Insertar en hoja manteniendo orden
            i = 0
            while i < len(node.keys) and id_val > node.keys[i]:
                i += 1
            node.keys.insert(i, id_val)
            node.children.insert(i, estudiante)
        else:
            i = 0
            while i < len(node.keys) and id_val > node.keys[i]:
                i += 1
            child = node.children[i]
            if len(child.keys) == self.order:
                self._split_child(node, i)
                if id_val > node.keys[i]:
                    i += 1
                child = node.children[i]
            self._insert_non_full(child, id_val, estudiante)

    def _split_child(self, parent, i):
        """Método auxiliar para dividir un nodo hijo cuando está lleno.

        Args:
            parent (BPlusNode): El nodo padre del hijo a dividir.
            i (int): El índice del hijo a dividir en la lista de hijos del padre.
        """
        order = self.order
        child = parent.children[i]
        if child.leaf:
            new_node = BPlusNode(leaf=True)
            mid = order // 2
            new_node.keys = child.keys[mid:]
            new_node.children = child.children[mid:]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid]
            # Enlazar hojas para recorrido secuencial
            new_node.next = child.next
            child.next = new_node
            # Insertar clave en el padre (la primera clave del nuevo nodo)
            parent.keys.insert(i, new_node.keys[0])
            parent.children.insert(i+1, new_node)
        else:
            new_node = BPlusNode(leaf=False)
            mid = order // 2
            new_node.keys = child.keys[mid+1:]
            new_node.children = child.children[mid+1:]
            mid_key = child.keys[mid]
            child.keys = child.keys[:mid]
            child.children = child.children[:mid+1]
            parent.keys.insert(i, mid_key)
            parent.children.insert(i+1, new_node)


# Medición de tiempos

def medir_busquedas(estructura, ids_buscar):
    """Ejecuta búsquedas para cada id en ids_buscar y retorna el tiempo total.

    Args:
        estructura: Una instancia de ListaEstudiantes, ABB o BPlusTree.
        ids_buscar (list): Una lista de IDs de estudiantes a buscar.

    Returns:
        float: El tiempo total transcurrido para todas las búsquedas en segundos.
    """
    inicio = time.perf_counter()
    for id_val in ids_buscar:
        _ = estructura.buscar(id_val)
    fin = time.perf_counter()
    return fin - inicio

def experimento(estudiantes, titulo):
    """Construye las tres estructuras con los estudiantes dados y mide tiempos para distintos lotes de búsqueda.

    Args:
        estudiantes (list): Una lista de diccionarios de estudiantes para construir las estructuras.
        titulo (str): Un título para el experimento (ej. "IDs insertados en ORDEN").
    """
    print(f"\n=== {titulo} ===")
    ids_todos = [e["id"] for e in estudiantes]

    # Construir estructuras (sin medir tiempo de construcción, solo de búsqueda)
    print("Construyendo estructuras...")
    # Lista
    lista_est = ListaEstudiantes(estudiantes)
    # ABB
    abb = ABB()
    for e in estudiantes:
        abb.insertar(e)
    # B+
    bplus = BPlusTree(order=4)
    for e in estudiantes:
        bplus.insertar(e["id"], e)

    # Cantidades de búsqueda a probar
    cantidades = [100, 1000, 2000, 4000, 10000]
    resultados = {"Lista": [], "ABB": [], "B+": []}

    for n in cantidades:
        # Seleccionar n ids aleatorios del conjunto total para las búsquedas
        ids_muestra = random.sample(ids_todos, n)
        print(f"  Búsquedas: {n}")

        # Medir tiempo para Lista
        t = medir_busquedas(lista_est, ids_muestra)
        resultados["Lista"].append(t)
        print(f"    Lista: {t:.6f} s")

        # Medir tiempo para ABB
        t = medir_busquedas(abb, ids_muestra)
        resultados["ABB"].append(t)
        print(f"    ABB:   {t:.6f} s")

        # Medir tiempo para B+
        t = medir_busquedas(bplus, ids_muestra)
        resultados["B+"].append(t)
        print(f"    B+:    {t:.6f} s")

    # Mostrar tabla resumen de tiempos
    print("\nResumen de tiempos (segundos):")
    print("Cantidad  |   Lista   |    ABB    |    B+")
    print("----------|-----------|-----------|---------")
    for i, n in enumerate(cantidades):
        print(f"{n:8d}  | {resultados['Lista'][i]:.6f} | {resultados['ABB'][i]:.6f} | {resultados['B+'][i]:.6f}")


# Main execution block

if __name__ == "__main__":
    random.seed(42)  # Establece la semilla para reproducibilidad de los resultados aleatorios

    # Define el número total de estudiantes a generar
    total = 10000

    # --- Escenario 1: IDs en orden --- #
    # Genera IDs ordenados secuencialmente
    ids_ordenados = list(range(total))
    # Crea estudiantes usando los IDs ordenados
    estudiantes_orden = generar_estudiantes(ids_ordenados)

    # --- Escenario 2: IDs aleatorios --- #
    # Genera una permutación aleatoria de IDs
    ids_aleatorios = random.sample(range(total), total)
    # Crea estudiantes usando los IDs aleatorios
    estudiantes_aleatorios = generar_estudiantes(ids_aleatorios)

    # Ejecutar experimentos para ambos escenarios de inserción
    experimento(estudiantes_orden, "IDs insertados en ORDEN")
    experimento(estudiantes_aleatorios, "IDs insertados en ALEATORIO")