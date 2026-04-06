# Solución de dos problemas criptográficos en Python

**Autor:** Jefferson Lizarazo Arias (Parte del código fue desarrollada con ayuda de inteligencia artificial (IA).)

Este notebook contiene la implementación de dos algoritmos de búsqueda inversa sobre funciones hash, utilizando fuerza bruta optimizada y árboles de Merkle.

## Problema 1: Revertir un hash SHA256 a su secuencia original

**Descripción:**  
Dado un hash SHA256 (en hexadecimal) que fue generado a partir de una secuencia de **10 dígitos** (cada dígito en el rango `[0,9]`), se debe encontrar dicha secuencia.

**Enfoque:**  
- El espacio de búsqueda es de `10^10` combinaciones (10 mil millones).  
- Se implementa una búsqueda exhaustiva con **multiprocesamiento** para aprovechar múltiples núcleos de CPU.  
- La búsqueda comienza desde `"0000000000"` hasta `"9999999999"`.  
- Para acelerar la comparación, se trabaja directamente con bytes (`digest()`) en lugar de cadenas hexadecimales.

**Uso:**  
Ejecutar la celda correspondiente, ingresar el hash objetivo y esperar el resultado. El tiempo de ejecución puede ser de varios minutos u horas según la posición de la secuencia.

---

## Problema 2: Encontrar el orden de transacciones que genera una raíz de Merkle

**Descripción:**  
Dadas una lista de transacciones (strings) y la raíz de Merkle (en hexadecimal) de un árbol construido con esas transacciones, se debe determinar una permutación de las transacciones que produzca exactamente esa raíz.

**Reglas:**  
- El árbol de Merkle se construye con SHA256.  
- En niveles impares, el último nodo se duplica (estándar en Bitcoin).  
- Se conocen todas las transacciones y su cantidad.

**Enfoque:**  
- Se generan todas las permutaciones de las transacciones (`itertools.permutations`).  
- Para cada permutación se calcula la raíz de Merkle y se compara con la objetivo.  
- Se detiene al encontrar la primera coincidencia.

**Limitación:**  
El método es factible solo para **pocas transacciones** (típicamente `N ≤ 10`), ya que `N!` crece muy rápido. Para `N=10` el tiempo en Colab es de unos pocos minutos.

**Uso:**  
Definir la lista de transacciones y el hash raíz objetivo, luego ejecutar la búsqueda.

---

## Ejecución en Google Colab

El notebook está diseñado para ejecutarse directamente en Colab. Solo es necesario copiar el código en celdas y seguir las instrucciones de entrada.

## Notas

- El problema 1 puede tardar horas si la secuencia buscada está cerca del final del espacio (`9999999999`).  
- El problema 2 es **combinatorialmente explosivo**; no intentar con más de 11 transacciones.

## Reconocimiento

Parte del código fue generado o refinado con asistencia de herramientas de inteligencia artificial, bajo la supervisión y criterio del autor.

Para cualquier duda, revisar los comentarios dentro del código.
