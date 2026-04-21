# Quad-Tree
**Autor:** Jefferson Lizarazo Arias (Algunas partes del código fueron desarrolladas con ayuda de IA)

Este proyecto implementa el árbol `QuadTree` para el uso en sistemas de logística de entregas. 

## Estructura del Proyecto

- `Quadtreetree.py`: Módulo principal del sistema. Contiene las clases `Point`, `Rectangle`, la estructura `QuadTree` para búsquedas en $\mathcal{O}(\log N)$, y la clase `FuerzaBruta` para las búsquedas tradicionales exhaustivas por medio de listas.
- `test.py`: Contiene las pruebas modulares y visualizaciones usando matplotlib. Comprueba rigurosamente que las búsquedas (`Range Search` y `Nearest Neighbor`) producen el mismo resultado que fuerza bruta. Genera imágenes (png) de validación manual.
- `analisis.py`: Herramienta de profiling métrico. Compara empirícamente el tiempo de los métodos sobre los diferentes tamaños de datos $N$ para comprobar dónde se cruzan las volatilidades.
- `README.md`: Este archivo.

## Instalación y Ejecución

*Requisitos:* Python 3.8+ y `matplotlib` instalado en el entorno (`pip install matplotlib`).

1. Para generar las gráficas de validación espacial de la búsqueda y correr las aserciones:
   ```bash
   python test.py
   ```
   **Output**: Imágenes de visualización `visualizacion_range_search.png` y `visualizacion_nearest_neighbor.png`.

2. Para efectuar el análisis comparativo del costo de rendimiento:
   ```bash
   python analisis.py
   ```
   **Output**: Generará un archivo `analisis_rendimiento.png` mostrando las curvas tiempo vs total de puntos.

## Análisis Comparativo & Resultados

### ¿Para qué tamaño de datos el árbol Quadtree comienza a ser más rápido que "Fuerza Bruta" (listas)?

Basado en las simulaciones corridas a través de `analisis.py` con 50 consultas promedio aleatorias:

- **Búsqueda por Radio (Range Search)**: El algoritmo QuadTree suele ser consistentemente más rápido que iterar todos los datos (Fuerza bruta sobre Listas) para tamaños de lista superiores a **N = 100 - 500 puntos** (dependiendo del computador y los tiempos microscópicos de instanciación). Esto se debe a que la complejidad en Fuerza Bruta es lineal $\mathcal{O}(N)$ ya que se evalúa la distancia euclidiana de *todos los clientes del mundo real*, mientras que en el Quadtree solo procesamos las ramas/rectángulos cuyo área logra intersectar el radio de búsqueda (búsqueda localizada o *pruning*), teniendo un rendimiento tendiente a $\mathcal{O}(\log N + k)$ donde k son los elementos retornados.

- **Vecino más Cercano (Nearest Neighbor)**: Sigue la misma directiva, a partir de **N = 100 - 500**, el QuadTree logra sobrepasar la velocidad de la matriz de recorrido simple. Esto surge gracias al *pruning* inteligente, donde si una rama del Quadtree tiene una distancia frontal más alta que nuestra "mejor distancia" encontrada, podemos podarla y evitar explorar miles de puntos en el interior de esa rama, reduciendo abismalmente los recuentos euclidianos.

Si la solución es superior a *N=10000* como en este proyecto, el Quadtree se vuelve matemáticamente una absoluta necesidad; con una lista, una docena de miles de consultas hundirían el procesador en pocos segundos.
