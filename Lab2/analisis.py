import time
import random
import matplotlib.pyplot as plt
from KDtree import KDTree, FuerzaBruta

def generate_points(n, k=2):
    return [tuple(random.uniform(0, 10000) for _ in range(k)) for _ in range(n)]

def run_benchmark():
    # Diferentes tamaños a evaluar
    sizes = [10, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    kd_times = []
    bf_times = []
    
    num_queries = 100  # Cantidad de búsquedas por cada N para sacar un promedio estable
    
    print("\nIniciando Benchmark de Búsqueda (Nearest Neighbor)")
    print("Promedios calculados sobre 100 consultas por tamaño de N.\n")
    print(f"{'N Puntos':<10} | {'KD-Tree (s)':<15} | {'Fuerza Bruta (s)':<18} | {'Ganador':<10}")
    print("-" * 65)
    
    crossover_point = None
    
    for n in sizes:
        points = generate_points(n)
        
        # Construcción de estructuras 
        kdtree = KDTree(points)
        brute_force = FuerzaBruta(points)
        
        queries = generate_points(num_queries)
        
        # Benchmark KD-Tree
        start_kd = time.perf_counter()
        for q in queries:
            kdtree.nearest_neighbor(q)
        end_kd = time.perf_counter()
        
        # Benchmark Fuerza Bruta
        start_bf = time.perf_counter()
        for q in queries:
            brute_force.nearest_neighbor(q)
        end_bf = time.perf_counter()
        
        # Tiempo promedio por query
        avg_kd = (end_kd - start_kd) / num_queries
        avg_bf = (end_bf - start_bf) / num_queries
        
        kd_times.append(avg_kd)
        bf_times.append(avg_bf)
        
        faster = "KD-Tree" if avg_kd < avg_bf else "Fuerza Bruta"
        
        # Detectamos dónde el KD-tree empieza a bajar su tiempo por debajo del brute force
        if avg_kd < avg_bf and crossover_point is None:
            crossover_point = n
            
        print(f"{n:<10} | {avg_kd:.8f}      | {avg_bf:.8f}         | {faster:<10}")

    print("\n" + "="*65)
    if crossover_point:
        print(f"CONCLUSIÓN: El Árbol KD comienza a ser consistentemente más rápido")
        print(f"en la búsqueda que la Fuerza Bruta alrededor de N = {crossover_point} puntos.")
    else:
        print("No se encontró punto de cruce. Raro, revisar implementaciones.")
    print("="*65 + "\n")

    # Gráfica
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, kd_times, marker='o', linewidth=2, color='green', label='KD-Tree  ~ O(log N)')
    plt.plot(sizes, bf_times, marker='x', linewidth=2, color='red', label='Fuerza Bruta ~ O(N)')
    
    # Crossover point
    if crossover_point:
        idx = sizes.index(crossover_point)
        plt.axvline(x=crossover_point, color='gray', linestyle='--', alpha=0.5, label=f'Cruce en N={crossover_point}')
        plt.scatter([crossover_point], [kd_times[idx]], color='black', s=80, zorder=5)

    plt.title('Comparativa de Tiempo de Búsqueda (Nearest Neighbor)')
    plt.xlabel('Cantidad de Puntos en la Ciudad (N)')
    plt.ylabel('Tiempo Promedio por Búsqueda (segundos)')
    plt.legend()
    plt.grid(True, linestyle=":")
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    run_benchmark()
