# Quad-Tree
**Autor:** Jefferson Lizarazo Arias (Algunas partes del código fueron desarrolladas con ayuda de IA)

Este proyecto implementa el árbol `QuadTree` para el uso en sistemas de logística de entregas. 

## Descripción del Problema

Eres parte de un equipo que desarrolla un sistema de logística de entregas en una ciudad.  
Se tienen coordenadas (x, y) de 10.000 puntos de entrega (estáticos, no cambian).  
Se necesita implementar un sistema que responda eficientemente preguntas como:

- ¿Qué puntos de entrega están a un radio de 500 metros de un punto dado?
- ¿Cuál es el punto de entrega más cercano a una ubicación dada?

**Objetivo:** Implementar un Árbol Quadtree desde cero y comparar su rendimiento con fuerza bruta (lista simple).

## Requisitos

Se requiere el uso de `matplotlib` para que funcionen las comprobaciones visuales y las métricas en diagramas:

```bash
pip install matplotlib
```
## Ejecución

1. **Para pruebas unitarias y visualizaciones:**
   ```bash
   python test.py
   ```
   *Nota: Las figuras son bloqueantes, para que aparezca la siguiente comprobación visual necesitas cerrar la ventana actual de matplotlib.*

2. **Análisis de rendimiento:**
   ```bash
   python analisis.py

## Análisis y Resultados
Se evaluaron tamaños de datos: N = [100, 500, 1000, 2000, 4000, 6000, 8000, 10000]
Para cada N se realizaron 50 consultas de búsqueda por radio y 50 consultas de vecino más cercano, promediando los tiempos.

Respuesta a las preguntas del análisis:
### ¿Para qué tamaño de datos el árbol Quadtree comienza a ser más rápido que fuerza bruta en búsqueda por radio?

A partir de N = 500 puntos, el QuadTree supera consistentemente a la fuerza bruta en búsqueda por radio (radio = 500 unidades).

### ¿Para qué tamaño de datos el árbol Quadtree comienza a ser más rápido que fuerza bruta en búsqueda del vecino más cercano?

A partir de N = 500 puntos, el QuadTree comienza a ser más rápido que la fuerza bruta en nearest neighbor.
La poda por distancia mínima al rectángulo y el orden de exploración reducen drásticamente las comparaciones, pero el overhead es mayor que en range search, por lo que el cruce ocurre más tarde.
