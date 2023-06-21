import tkinter as tk
from tkinter import ttk
import queue
from threading import Thread
from tkinter import messagebox
import numpy as np
import VentanaResultado as vr
from PIL import Image
import Kmeans.Kmeans as km
import sys


class LoadingScreen(tk.Toplevel):
    """
    Ventana de carga. En el backgroud se ejecuta el algritmo K-means como un proceso paralelo
    a la aplicación.
    """
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.protocol('WM_DELETE_WINDOW', self.__avisoSalida)
        self.resizable(False, False)
        self.__pb = ttk.Progressbar(
            self, 
            orient="horizontal", 
            mode="indeterminate", 
            length="300")
        
        mensaje = tk.Label(
            self, 
            text="Algoritmo de clustering K-means ejecutandose, por favor espere..."
        )

        self.__pb.pack()
        self.__pb.start()
        
        mensaje.pack()


    def run(self, imagen, hiperparametros):
        """
        Ejecuta el algoritmo de K-means de acuerdo a la imagen e hiperparámetros ingresados. El algoritmo se ejecuta como
        un proceso (hilo) paralelo a la aplicación.
        """
        # oculta la ventana principal
        self.root.withdraw()

        self.__imagen = imagen.getImage()
        self.__ext = imagen.getExtension()

        # cola que comunicará la aplicación principal con el proceso paralelo
        self.__cola = queue.Queue()

        # hilo o proceso que ejecutará K-means
        self.__thread1 = Thread(
            target=self.__run_algorithm, 
            args=(self.__imagen, hiperparametros, self.__cola), 
            daemon=True)
        self.__thread1.start()

        self.__check_queue()


    def __check_queue(self):
        """
        Consulta periódicamente si el hilo que ejecuta el algoritmo K-means sigue vivo y si
        la cola de resultados tiene elementos. Que la cola esté con elementos significa que el 
        algoritmo K-means ya terminó y el hilo finalizó su ejecución.
        """
        if self.__thread1.is_alive():
            # si aun esta vivo el hilo, volver a preguntar despues de un tiempo si terminó 
            self.root.after(5000, self.__check_queue)

        # chequea si la cola de resultados tiene algún elemento      
        self.__access_queue()
        
        if not self.__thread1.is_alive():
            # si el hilo finallizó su ejecución se detiene la barra de progreso y se muestra la ventana
            # de resultados.
            self.__pb.stop()
            vr.VentanaResultado(self.root, self.__imagen, self.__ext)
            messagebox.showinfo(title="Aviso", message="Proceso finalizado")            
            self.destroy()


    def __access_queue(self):
        """
        Accede a la cola de resultados. Esta cola comunica a la aplicación principal con el hilo que
        ejecuta K-means. Si la cola tiene algún elemento quiere decir que el algoritmo terminó su
        ejecución.
        """
        # si la cola no esta vacia, entonces sacamos la imagen, ya que el hilo termino su ejecucion
        if self.__cola.qsize():
            try:
                resultado = self.__cola.get_nowait()
                if isinstance(resultado, str):
                    messagebox.showerror(
                    title="Error", 
                    message=f"Ha ocurrido un error grave en el programa: {resultado}")
                    
                else:
                    self.__imagen = self.transformImagen(resultado)
            except queue.Empty:
                # get_nowait retorna un item sin bloquearse, sin embargo, si no hay nada disponible lanza
                # exception
                print("queue empty!")
                


    def __run_algorithm(self, imagen_original, hiperparametros, cola):
        """
        Ejecuta el algoritmo de K-means realizando previamente una modificación de la imagen.
        Este método debe ser ejecutado por un hilo o proceso paralelo a la aplicación. Si se
        hace en la misma aplicación principal, la interfaz se congelará y el programa dejará
        de responder con el fin de ejecutar el algoritmo.

        La modificación de la imagen es la división de cada valor de pixel por 255. Esto sirve
        para escalar dichos valores, lo que beneficiará al algoritmo a ejecutarse más rápidamente.
        Además se debe hacer un reshape, ya que la clase KMeans solo acepta arrays 2d.

        Cuando termine el procedimiento, este método pondrá el ndarray resultante en la cola de 
        resultados comunicando a la aplicación principal que terminó la ejecución.

        Args:
            - imagen_original (PIL.Image): imagen ingresada por el usuario
            - hiperparametros (list): lista de hiperparámetros.
            - cola (queue.Queue): cola que comunica un hilo con la aplicación principal.
        """
        # imagen_original es una PIL image
        # sin la división sería un array con int, necesitamos que sea float
        imagen = np.array(imagen_original) / 255
        
        m, n, p = imagen.shape
        imagen_2d = np.reshape(imagen, (m * n, p))
        
        num_clusters, num_ejecuciones, num_iter = hiperparametros
        
        model = km.KMeans(num_clusters, num_ejecuciones, num_iter)

        try:
            _, centroids, index_centroids = model.fit(imagen_2d, True)
        except ValueError as e:
                cola.put(str(e))                                
        else:
            imagen_nueva = centroids[index_centroids] #matrix 2d
            imagen_nueva = np.reshape(imagen_nueva, (m, n, p)) #matrix 3d
            cola.put(imagen_nueva)
            


    def transformImagen(self, imagen):
        """
        Transforma la imagen procesada por K-means. Los valores de la imagen son float, 
        para poder convertirlo en PIL.Image deben ser uint8

        Args:
            - imagen (ndarray (m,n,3)): imagen procesada por el algoritmo K-means.
        
        Returns:
            - img (PIL.Image): imagen transformada
        """
        img = Image.fromarray((imagen * 255).astype(np.uint8)).convert("RGB")
        return img 

    def __avisoSalida(self):
        """
        Muestra ventana de Aviso de salida
        """
        valor = messagebox.askquestion(
            title="Salir", message="¿Esta seguro que quiere salir de la aplicación?"
        )
        print(f"val {valor}")
        if valor=="yes":
            self.root.destroy()
            sys.exit(1)

