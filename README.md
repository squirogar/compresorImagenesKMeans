# compresorImagenesKMeans
Compresor de imágenes utilizando el algoritmo de clustering K-Means. El algoritmo K-means encontrará los clusters óptimos y luego, asignará el valor del centroid a todos los píxeles que se agrupen en el cluster correspondiente. El valor que toma el centroid es el promedio de los valores de los píxeles que están en el cluster (3 canales RGB, con un valor de 0-255 cada canal). Mientras más clusters elijamos menor tamaño debería tener la imagen y pero peor será su calidad. Sin embargo, el tamaño de la imagen se conservará.

Los detalles del algoritmo de clustering K-Means utilizado en este proyecto se pueden encontrar en este [repositorio](https://github.com/squirogar/Clustering_algorithm) de mi autoría.

## Funcionalidades
1. Carga de imágenes `.png` y `.jpg`.
2. Ingreso de hiperparámetros de algoritmo K-means:
- Número de clusters a encontrar
- Número de ejecuciones del algoritmo
- Número de iteraciones por ejecución del algoritmo
3. Ejecución del algoritmo K-means que comprimirá la calidad de imagen original conservando el tamaño.
4. Descarga de la imagen comprimida. El directorio de destino es el directorio actual donde se encuentra `main.py` y tendrá el nombre de `image.*` donde `*` es la extensión.

## Screnshoots
Ventana principal:


Configuracion hiperparámetros:


Archivo abierto:


Pantalla de carga:


Imagen obtenida:


Imagen descargada:


## Dependencias
- Pillow (PIL)
- K-Means algorithm from scratch: [repositorio](https://github.com/squirogar/Clustering_algorithm)

## Licencia
GPL-3.0