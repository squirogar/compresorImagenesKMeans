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
![main](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/cca363ed-4380-44c4-8782-221dc9dc6ee6)

Configuracion hiperparámetros:
![config](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/87789dec-acbb-41fa-865b-59807ccd9acd)

Archivo abierto:
![open_file](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/dd7da19e-845e-4295-9d74-be1d3072941a)

Pantalla de carga:
![loading](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/74b0e2a3-0ba4-43e3-8ff7-bdbcbf958ba4)

Imagen obtenida:
![final_file](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/d38d1e8f-dd91-4464-9041-be4261b6d527)

Comparación:
![resultado](https://github.com/squirogar/compresorImagenesKMeans/assets/50588970/e94f74ec-395e-479f-8521-a68473a0ea81)

## Dependencias
- Pillow (PIL)
- K-Means algorithm from scratch: [repositorio](https://github.com/squirogar/Clustering_algorithm)

## Licencia
GPL-3.0
