# Sistema de Búsqueda de Estudiantes - Comparación de Estructuras de Datos

Este repositorio contiene el código fuente para comparar el rendimiento de tres estructuras de datos en la búsqueda de estudiantes por ID. Las estructuras implementadas son:

- **Listas** (búsqueda lineal)
- **Árbol Binario de Búsqueda (ABB)** 
- **Árbol B+** 

El objetivo es medir el tiempo de búsqueda para diferentes cantidades de consultas (100, 1000, 2000, 4000 y 10000) cuando los IDs se insertan en **orden ascendente** y en **orden aleatorio**.

## 📁 Archivos

- `sistemasdebusqueda.py` — Código principal en Python que genera los datos, implementa las estructuras, ejecuta los experimentos y muestra los resultados.
- `README.md` — Este archivo de documentación.

## 🚀 Requisitos y ejecución

### Requisitos

- Python 3.6 o superior.
- No se requieren librerías externas (usa solo `random` y `time` de la biblioteca estándar).

### Ejecución

1. Clona este repositorio o descarga el archivo `sistemasdebusqueda.py`.
2. Abre una terminal en la carpeta donde se encuentra el archivo.
3. Ejecuta el script con:

   ```bash
   python sistemasdebusqueda.py
4. La salida mostrará el progreso de construcción de las estructuras y, para cada lote de búsquedas, los tiempos parciales. Al final de cada experimento se presenta una tabla resumen.

### Personalización

Puedes modificar los siguientes parámetros directamente en el bloque `if __name__ == "__main__":`:

- `total:` número total de estudiantes (por defecto 10000).

- `random.seed():` cambiar la semilla para obtener diferentes conjuntos de datos.

- `cantidades:` lista de tamaños de lote (modificable dentro de la función `experimento`).
  

## 📊 Resultados esperados

Al ejecutar el código se obtendrán dos tablas comparativas:

- IDs insertados en ORDEN: El ABB se comporta como una lista enlazada (búsqueda lineal) porque la inserción secuencial lo desbalancea por completo. El árbol B+, al estar siempre balanceado, mantiene búsquedas rápidas.

- IDs insertados en ALEATORIO: El ABB se mantiene aproximadamente balanceado y ofrece tiempos similares al B+.

En todos los casos, la lista desordenada es la estructura más lenta, con tiempos que crecen linealmente con el número de búsquedas.

Ejemplo de salida (valores ilustrativos, pueden variar según la máquina):

=== IDs insertados en ORDEN ===

Construyendo estructuras...

  Búsquedas: 100
  
    Lista: 0.045678 s
    ABB:   0.041234 s
    B+:    0.001234 s
...

Resumen de tiempos (segundos):

Cantidad  |   Lista   |    ABB    |    B+
----------|-----------|-----------|---------
     100  | 0.045678  | 0.041234  | 0.001234
...

## 📝 Notas importantes

- Este proyecto fue desarrollado con asistencia de IA bajo supervisión.

Nombre: Jefferson Lizarazo Arias

Curso: Estructura de Datos

Institución: UdeA
