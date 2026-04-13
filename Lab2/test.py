import unittest
import random
import matplotlib.pyplot as plt
from Lab2.KDtree import KDTree, BruteForce

def generate_points(n, k=2, min_val=0, max_val=10000):
    """Genera n coordenadas aleatorias que representan puntos en metros"""
    return [tuple(random.uniform(min_val, max_val) for _ in range(k)) for _ in range(n)]

class TestKDTree(unittest.TestCase):
    def setUp(self):
        # 1,000 puntos para una prueba rápida de correctitud en k=2
        self.points = generate_points(1000, 2)
        self.kdtree = KDTree(self.points)
        self.brute_force = BruteForce(self.points)

    def test_range_search(self):
        target = (5000, 5000)
        radius = 500
        
        kd_res = self.kdtree.range_search(target, radius)
        bf_res = self.brute_force.range_search(target, radius)
        
        # Deben devolver la misma cantidad de puntos y elementos
        self.assertEqual(len(kd_res), len(bf_res))
        self.assertEqual(set(kd_res), set(bf_res))

    def test_nearest_neighbor(self):
        target = (5000, 5000)
        kd_point, kd_dist = self.kdtree.nearest_neighbor(target)
        bf_point, bf_dist = self.brute_force.nearest_neighbor(target)
        
        self.assertAlmostEqual(kd_dist, bf_dist)
        
    def test_edge_cases(self):
        target = (-1000, -1000)  # Objetivo lejos de la nube
        kd_point, _ = self.kdtree.nearest_neighbor(target)
        self.assertIsNotNone(kd_point)

def visualize_range_search():
    # 10,000 puntos como dice el problema
    points = generate_points(10000, 2)
    kdtree = KDTree(points)
    
    target = (5000, 5000)
    radius = 500
    found_points = kdtree.range_search(target, radius)
    
    plt.figure(figsize=(8, 8))
    # Puntos globales (gris)
    px = [p[0] for p in points]
    py = [p[1] for p in points]
    plt.scatter(px, py, s=2, c='lightgray', alpha=0.6, label='Puntos de Entrega (Ciudad)')
    
    # Puntos encontrados (azul)
    if found_points:
        fx = [p[0] for p in found_points]
        fy = [p[1] for p in found_points]
        plt.scatter(fx, fy, s=15, c='blue', alpha=0.8, label='Entregas viables')
        
    # Ubicación objetivo (rojo)
    plt.scatter([target[0]], [target[1]], s=100, c='red', marker='X', label='Ubicación Origen')
    
    # Dibujar radio de búsqueda
    circle = plt.Circle(target, radius, color='red', fill=False, linestyle='--', linewidth=1.5)
    plt.gca().add_patch(circle)
    
    plt.title(f"Range Search KD-Tree: {len(found_points)} puntos encontrados en un radio de {radius}m")
    plt.xlabel('Eje X (metros)')
    plt.ylabel('Eje Y (metros)')
    plt.axis('equal')
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.show()

def visualize_nearest_neighbor():
    points = generate_points(10000, 2)
    kdtree = KDTree(points)
    
    target = (4500, 5500)
    best_point, best_dist = kdtree.nearest_neighbor(target)
    
    plt.figure(figsize=(8, 8))
    px = [p[0] for p in points]
    py = [p[1] for p in points]
    plt.scatter(px, py, s=2, c='lightgray', alpha=0.6, label='Puntos de Entrega')
    
    # Origen y Vecino
    plt.scatter([target[0]], [target[1]], s=100, c='red', marker='X', label='Ubicación Origen')
    plt.scatter([best_point[0]], [best_point[1]], s=50, c='green', marker='o', label='Vecino más cercano')
    
    # Línea
    plt.plot([target[0], best_point[0]], [target[1], best_point[1]], 'k--', label=f'Distancia: {best_dist:.2f}m')
    
    # Zoom estético centrado en la zona (no mostrar los 10k fijos a no ser necesario)
    plt.xlim(target[0] - 1500, target[0] + 1500)
    plt.ylim(target[1] - 1500, target[1] + 1500)
    
    plt.title(f"Nearest Neighbor KD-Tree: Mejor distancia = {best_dist:.2f}m")
    plt.xlabel('Eje X (metros)')
    plt.ylabel('Eje Y (metros)')
    plt.legend()
    plt.grid(True, linestyle=':')
    plt.show()

if __name__ == '__main__':
    print("Ejecutando pruebas")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestKDTree)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    print("\nAbriendo ventana para visualizar el Range Search...")
    visualize_range_search()
    
    print("\nAbriendo ventana para visualizar el Nearest Neighbor...")
    visualize_nearest_neighbor()
    print("Fin de las pruebas.")
