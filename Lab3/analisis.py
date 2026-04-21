import time
import random
import matplotlib.pyplot as plt
from Quadtree import Point, Rectangle, QuadTree, FuerzaBruta

def generate_random_points(n, min_val, max_val):
    return [Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val), i) for i in range(n)]

def test_performance():
    print("Iniciando análisis de rendimiento...")
    
    # nnúmero de puntos a evaluar
    tamaños_N = [100, 500, 1000, 2000, 4000, 6000, 8000, 10000]
    
    tiempos_qt_range = []
    tiempos_bf_range = []
    
    tiempos_qt_nn = []
    tiempos_bf_nn = []
    
    MIN_VAL = 0
    MAX_VAL = 10000
    
    for n in tamaños_N:
        print(f"Probando para N = {n}...")
        points = generate_random_points(n, MIN_VAL, MAX_VAL)
        
        boundary = Rectangle(MAX_VAL/2, MAX_VAL/2, MAX_VAL/2, MAX_VAL/2)
        qt = QuadTree(boundary, capacity=4)
        bf = FuerzaBruta()
        
        for p in points:
            qt.insert(p)
            bf.insert(p)
            
        # Generar varias queries para sacar un promedio y que el tiempo sea representativo
        NUM_QUERIES = 50
        queries = generate_random_points(NUM_QUERIES, MIN_VAL, MAX_VAL)
        
        # --- Evaluar Range Search ---
        radio = 500
        
        t0 = time.time()
        for q in queries:
            bf.query_radius(q, radio)
        t1 = time.time()
        tiempos_bf_range.append((t1 - t0) / NUM_QUERIES)
        
        t0 = time.time()
        for q in queries:
            qt.query_radius(q, radio)
        t1 = time.time()
        tiempos_qt_range.append((t1 - t0) / NUM_QUERIES)

        # --- Evaluar Nearest Neighbor ---
        t0 = time.time()
        for q in queries:
            bf.nearest_neighbor(q)
        t1 = time.time()
        tiempos_bf_nn.append((t1 - t0) / NUM_QUERIES)
        
        t0 = time.time()
        for q in queries:
            qt.nearest_neighbor(q)
        t1 = time.time()
        tiempos_qt_nn.append((t1 - t0) / NUM_QUERIES)
        
    # --- Visualización del rendimiento ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.plot(tamaños_N, tiempos_bf_range, marker='o', label='Fuerza Bruta')
    ax1.plot(tamaños_N, tiempos_qt_range, marker='s', label='QuadTree')
    ax1.set_title("Range Search: Tiempo vs N")
    ax1.set_xlabel("Número de Puntos (N)")
    ax1.set_ylabel("Tiempo Promedio de Búsqueda (s)")
    ax1.legend()
    ax1.grid(True)
    
    ax2.plot(tamaños_N, tiempos_bf_nn, marker='o', label='Fuerza Bruta')
    ax2.plot(tamaños_N, tiempos_qt_nn, marker='s', label='QuadTree')
    ax2.set_title("Nearest Neighbor: Tiempo vs N")
    ax2.set_xlabel("Número de Puntos (N)")
    ax2.set_ylabel("Tiempo Promedio de Búsqueda (s)")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig('analisis_rendimiento.png')
    # plt.show()
    print("\nGráfico de rendimiento guardado en 'analisis_rendimiento.png'.")
    
    # Análisis del cruce
    print("\n--- Discusión de Resultados ---")
    cruce_encontrado_range = None
    for i in range(len(tamaños_N)):
        if tiempos_qt_range[i] < tiempos_bf_range[i]:
            cruce_encontrado_range = tamaños_N[i]
            break
            
    if cruce_encontrado_range:
        print(f"Para Búsqueda por Radio, QuadTree comienza a ser más rápido que Fuerza Bruta alrededor de N = {cruce_encontrado_range}.")
    else:
        print("Para Búsqueda por Radio, QuadTree no logró superar a Fuerza Bruta en los tamaños probados (posible sobrecarga del árbol).")

    cruce_encontrado_nn = None
    for i in range(len(tamaños_N)):
        if tiempos_qt_nn[i] < tiempos_bf_nn[i]:
            cruce_encontrado_nn = tamaños_N[i]
            break
            
    if cruce_encontrado_nn:
        print(f"Para Búsqueda Vecino Cercano, QuadTree comienza a ser más rápido que Fuerza Bruta alrededor de N = {cruce_encontrado_nn}.")
    else:
        print("Para Búsqueda Vecino Cercano, QuadTree no logró superar a Fuerza Bruta en los tamaños probados.")

if __name__ == '__main__':
    test_performance()
