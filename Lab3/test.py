import random
import matplotlib.pyplot as plt
from Quadtree import Point, Rectangle, QuadTree, FuerzaBruta

def draw_quadtree(ax, node):
    if node is None:
        return
    rect = plt.Rectangle((node.boundary.west, node.boundary.south), 
                         node.boundary.w * 2, node.boundary.h * 2,
                         edgecolor='gray', fill=False, lw=0.5, alpha=0.5)
    ax.add_patch(rect)
    
    if node.divided:
        draw_quadtree(ax, node.nw)
        draw_quadtree(ax, node.ne)
        draw_quadtree(ax, node.sw)
        draw_quadtree(ax, node.se)

def generate_random_points(n, min_val, max_val):
    return [Point(random.uniform(min_val, max_val), random.uniform(min_val, max_val), i) for i in range(n)]

def test_system():
    print("Iniciando Pruebas Unitarias...")
    N_POINTS = 10000
    MIN_VAL = 0
    MAX_VAL = 10000 # 10km x 10km area
    
    points = generate_random_points(N_POINTS, MIN_VAL, MAX_VAL)
    
    # Boundary que cubra todos los puntos
    boundary = Rectangle(MAX_VAL/2, MAX_VAL/2, MAX_VAL/2, MAX_VAL/2)
    qt = QuadTree(boundary, capacity=4)
    bf = FuerzaBruta()
    
    for p in points:
        qt.insert(p)
        bf.insert(p)
        
    print(f"Insertados {N_POINTS} puntos en QuadTree y BruteForce.")
    
    # --- Test Range Search ---
    target_point = Point(5000, 5000)
    radius = 500
    
    qt_range_result = qt.query_radius(target_point, radius)
    bf_range_result = bf.query_radius(target_point, radius)
    
    assert len(qt_range_result) == len(bf_range_result), "Falló la prueba: Longitud de resultados distinto en Range Search."
    qt_set = set([p.point_id for p in qt_range_result])
    bf_set = set([p.point_id for p in bf_range_result])
    assert qt_set == bf_set, "Falló la prueba: Elementos encontrados distintos en Range Search."
    
    print(f"Prueba de Range Search (Radio={radius}m): EXITOSA. {len(qt_range_result)} puntos encontrados.")
    
    # --- Test Nearest Neighbor ---
    target_nn = Point(2500, 2500)
    
    qt_nn_point, qt_nn_dist = qt.nearest_neighbor(target_nn)
    bf_nn_point, bf_nn_dist = bf.nearest_neighbor(target_nn)
     
    # Podrían ser distintos puntos si hay un empate exacto, pero la distancia debe ser la misma.
    assert abs(qt_nn_dist - bf_nn_dist) < 1e-9, "Falló la prueba: Diferente distancia mínima en Nearest Neighbor."
    print("Prueba de Nearest Neighbor: EXITOSA.")

def visualize_range_search():
    print("Generando visualización de Range Search...")
    N_POINTS = 500 # Menos puntos para que la visualización sea limpia
    MIN_VAL = 0
    MAX_VAL = 10000 
    random.seed(42) # Mismos puntos para ambas visualizaciones
    points = generate_random_points(N_POINTS, MIN_VAL, MAX_VAL)
    boundary = Rectangle(MAX_VAL/2, MAX_VAL/2, MAX_VAL/2, MAX_VAL/2)
    qt = QuadTree(boundary, capacity=4)
    for p in points:
        qt.insert(p)
        
    target_point = Point(5000, 5000)
    radius = 1500
    found = qt.query_radius(target_point, radius)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Todos los puntos (gris)
    ax.scatter([p.x for p in points], [p.y for p in points], c='lightgray', s=10, label='Puntos')
    
    # Puntos encontrados (verde)
    if found:
        ax.scatter([p.x for p in found], [p.y for p in found], c='green', s=30, label='Encontrados')
        
    # Objetivo (rojo)
    ax.scatter([target_point.x], [target_point.y], c='red', s=50, marker='x', label='Centro')
    
    # Dibujar radio
    circle = plt.Circle((target_point.x, target_point.y), radius, color='blue', fill=False, linestyle='--', label='Área de Búsqueda')
    ax.add_patch(circle)
    
    ax.set_xlim(0, MAX_VAL)
    ax.set_ylim(0, MAX_VAL)
    ax.set_aspect('equal')
    ax.set_title('Visualización Quadtree - Range Search')
    ax.legend()
    
    draw_quadtree(ax, qt)
    
    # plt.savefig('visualizacion_range_search.png')
    print("Mostrando visualización Range Search en ventana interactiva...")
    plt.show()

def visualize_nearest_neighbor():
    print("Generando visualización de Nearest Neighbor...")
    N_POINTS = 500
    MIN_VAL = 0
    MAX_VAL = 10000 
    random.seed(42) # Mismos puntos que en range_search
    points = generate_random_points(N_POINTS, MIN_VAL, MAX_VAL)
    boundary = Rectangle(MAX_VAL/2, MAX_VAL/2, MAX_VAL/2, MAX_VAL/2)
    qt = QuadTree(boundary, capacity=4)
    for p in points:
        qt.insert(p)
        
    target_point = Point(5000, 5000) # Mismo punto de objetivo
    nn_point, nn_dist = qt.nearest_neighbor(target_point)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter([p.x for p in points], [p.y for p in points], c='lightgray', s=10, label='Puntos')
    
    ax.scatter([target_point.x], [target_point.y], c='red', s=50, marker='x', label='Objetivo')
    
    if nn_point:
        ax.scatter([nn_point.x], [nn_point.y], c='blue', s=40, label='Vecino más cercano')
        ax.plot([target_point.x, nn_point.x], [target_point.y, nn_point.y], 'k--', label=f'Distancia: {nn_dist:.2f}')
        
    ax.set_xlim(0, MAX_VAL)
    ax.set_ylim(0, MAX_VAL)
    ax.set_aspect('equal')
    ax.set_title('Visualización Quadtree - Nearest Neighbor')
    ax.legend()
    
    draw_quadtree(ax, qt)
    
    # plt.savefig('visualizacion_nearest_neighbor.png')
    print("Mostrando visualización Nearest Neighbor en ventana interactiva...")
    plt.show()

if __name__ == '__main__':
    test_system()
    visualize_range_search()
    visualize_nearest_neighbor()
