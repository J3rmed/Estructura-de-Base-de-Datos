import math

def euclidean_distance(p1, p2):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))

class Node:
    def __init__(self, point, left=None, right=None):
        self.point = point
        self.left = left
        self.right = right

class KDTree:
    def __init__(self, points):
        self.k = len(points[0]) if points else 0
        self.root = self._build(list(points), depth=0)

    def _build(self, points, depth):
        if not points:
            return None
        
        axis = depth % self.k
        # Ordenar los puntos a lo largo del eje actual
        points.sort(key=lambda x: x[axis])
        
        median_idx = len(points) // 2
        
        # Determinar la mediana y dividir
        return Node(
            point=points[median_idx],
            left=self._build(points[:median_idx], depth + 1),
            right=self._build(points[median_idx + 1:], depth + 1)
        )

    def range_search(self, target, radius):
        """
        Encuentra todos los puntos dentro de una distancia 'radius' desde 'target'.
        """
        results = []
        self._range_search(self.root, target, radius, 0, results)
        return results

    def _range_search(self, node, target, radius, depth, results):
        if node is None:
            return
        
        # Si la distancia al punto es <= al radio, lo añadimos
        if euclidean_distance(node.point, target) <= radius:
            results.append(node.point)
            
        axis = depth % self.k
        
        # Decidir si necesitamos explorar subárbol izquierdo y/o derecho
        # Si la distancia del target al plano es menor al radio, puede haber intersectos en ambos
        if target[axis] - radius <= node.point[axis]:
            self._range_search(node.left, target, radius, depth + 1, results)
        if target[axis] + radius >= node.point[axis]:
            self._range_search(node.right, target, radius, depth + 1, results)

    def nearest_neighbor(self, target):
        """
        Encuentra el vecino más cercano a 'target'.
        """
        self.best_point = None
        self.best_dist = float('inf')
        self._nearest_neighbor(self.root, target, 0)
        return self.best_point, self.best_dist

    def _nearest_neighbor(self, node, target, depth):
        if node is None:
            return
        
        dist = euclidean_distance(node.point, target)
        if dist < self.best_dist:
            self.best_dist = dist
            self.best_point = node.point
            
        axis = depth % self.k
        
        # Determinar qué subárbol explorar primero (el más probable)
        if target[axis] < node.point[axis]:
            good_side = node.left
            bad_side = node.right
        else:
            good_side = node.right
            bad_side = node.left
            
        # Explorar el lado "bueno"
        self._nearest_neighbor(good_side, target, depth + 1)
        
        # Ver si hay chances de que un punto mejor esté en el lado "malo"
        if abs(target[axis] - node.point[axis]) < self.best_dist:
            self._nearest_neighbor(bad_side, target, depth + 1)


class FuerzaBruta:
    """Implementación basada en listas para evaluar el rendimiento esperado y verificar validaciones."""
    def __init__(self, points):
        self.points = list(points)
        
    def range_search(self, target, radius):
        results = []
        for p in self.points:
            if euclidean_distance(p, target) <= radius:
                results.append(p)
        return results

    def nearest_neighbor(self, target):
        if not self.points:
            return None, float('inf')
            
        best_point = None
        best_dist = float('inf')
        
        for p in self.points:
            dist = euclidean_distance(p, target)
            if dist < best_dist:
                best_dist = dist
                best_point = p
                
        return best_point, best_dist
