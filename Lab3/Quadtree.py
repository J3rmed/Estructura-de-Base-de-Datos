import math

class Point:
    def __init__(self, x, y, point_id=None):
        self.x = x
        self.y = y
        self.point_id = point_id

    def distance_to(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def __repr__(self):
        return f"Point({self.x:.2f}, {self.y:.2f})"

class Rectangle:
    """
    Rectangle represented by its center (x, y) and half-dimension (w, h).
    """
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.west = x - w
        self.east = x + w
        self.north = y + h
        self.south = y - h

    def contains(self, point):
        return (self.west <= point.x < self.east and
                self.south <= point.y < self.north)

    def intersects(self, other_range):
        return not (other_range.west > self.east or
                    other_range.east < self.west or
                    other_range.south > self.north or
                    other_range.north < self.south)
    
    def distance_from_point(self, point):
        """
        Minimum Euclidean distance from a point to this rectangle.
        If the point is inside the rectangle, the distance is 0.
        """
        dx = max(self.west - point.x, 0, point.x - self.east)
        dy = max(self.south - point.y, 0, point.y - self.north)
        return math.sqrt(dx*dx + dy*dy)

class QuadTree:
    def __init__(self, boundary, capacity=4):
        self.boundary = boundary
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w / 2
        h = self.boundary.h / 2

        self.ne = QuadTree(Rectangle(x + w, y + h, w, h), self.capacity)
        self.nw = QuadTree(Rectangle(x - w, y + h, w, h), self.capacity)
        self.se = QuadTree(Rectangle(x + w, y - h, w, h), self.capacity)
        self.sw = QuadTree(Rectangle(x - w, y - h, w, h), self.capacity)
        
        self.divided = True
        
        # Opcional: bajar los puntos existentes a los nuevos hijos
        # para implementaciones estrictas, no es estrictamente necesario,
        # pero es bueno para la limpieza del árbol y que sólo las hojas contengan puntos (poda).
        for p in self.points:
            self.ne.insert(p) or self.nw.insert(p) or self.se.insert(p) or self.sw.insert(p)
        self.points = []

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if not self.divided:
            if len(self.points) < self.capacity:
                self.points.append(point)
                return True
            else:
                self.subdivide()

        if self.ne.insert(point): return True
        if self.nw.insert(point): return True
        if self.se.insert(point): return True
        if self.sw.insert(point): return True
        
        return False

    def query_radius(self, center_point, radius, found=None):
        if found is None:
            found = []

        # Representamos el rango círcular con un bounding box aproximado
        range_rect = Rectangle(center_point.x, center_point.y, radius, radius)

        # Si el rango ni siquiera intersecta el cuadrante actual, cancelamos la búsqueda en esta rama
        if not self.boundary.intersects(range_rect):
            return found

        # Verificamos puntos en el nodo actual (si no ha sido dividido, los puntos están aquí)
        if not self.divided:
            for p in self.points:
                if p.distance_to(center_point) <= radius:
                    found.append(p)
        else:
            self.nw.query_radius(center_point, radius, found)
            self.ne.query_radius(center_point, radius, found)
            self.sw.query_radius(center_point, radius, found)
            self.se.query_radius(center_point, radius, found)

        return found

    def nearest_neighbor(self, target_point, best_point=None, best_dist=float('inf')):
        # Si la distancia al límite de este cuadrante ya es peor que nuestra mejor distancia, podamos esta rama.
        if self.boundary.distance_from_point(target_point) >= best_dist:
            return best_point, best_dist

        # Revisar puntos en el nodo actual
        if not self.divided:
            for p in self.points:
                dist = p.distance_to(target_point)
                if dist < best_dist:
                    best_dist = dist
                    best_point = p
            return best_point, best_dist

        # Heurística: buscar primero en el cuadrante donde se ubica el target_point (o el más cercano)
        children = [self.nw, self.ne, self.sw, self.se]
        children.sort(key=lambda child: child.boundary.distance_from_point(target_point))

        for child in children:
            best_point, best_dist = child.nearest_neighbor(target_point, best_point, best_dist)

        return best_point, best_dist


class FuerzaBruta:
    def __init__(self):
        self.points = []

    def insert(self, point):
        self.points.append(point)

    def query_radius(self, center_point, radius):
        found = []
        for p in self.points:
            if p.distance_to(center_point) <= radius:
                found.append(p)
        return found
    
    def nearest_neighbor(self, target_point):
        best_point = None
        best_dist = float('inf')
        for p in self.points:
            dist = p.distance_to(target_point)
            if dist < best_dist:
                best_dist = dist
                best_point = p
        return best_point, best_dist
