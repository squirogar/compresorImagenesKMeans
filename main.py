import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from PIL import ImageTk, Image
from tkinter import messagebox
import Kmeans as km
import numpy as np
from threading import Thread
import queue
import sys
            

class Aplicacion(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Compresor de imágenes K-means")

        # objeto imagen #
        self.__imageApp = None

        self.__imagenLabel = None        
        self.__ventanaConf = None
        self.__listaHiperparametros = []

        # menu #
        self.__myMenu = self.__creaMenu()
        self.config(menu=self.__myMenu)


        #### scrolleable
        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=1)

        my_canvas = tk.Canvas(main_frame)

        my_scrollbary = ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
        my_scrollbary.pack(side='right', fill='y')

        my_scrollbarx = ttk.Scrollbar(main_frame, orient='horizontal', command=my_canvas.xview)
        my_scrollbarx.pack(side='bottom', fill='x')

        my_canvas.pack(side='top', fill='both', expand=1)

        my_canvas.configure(yscrollcommand=my_scrollbary.set)
        my_canvas.configure(xscrollcommand=my_scrollbarx.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        self.second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0,0), window=self.second_frame, anchor="nw") 




    def __comprobarHiperparametros(self):
        """
        Comprueba que los hiperparametros y la imagen estén correctamente establecidos por el usuario.
        En el caso que sí lo sea, se ejecuta la vetana de carga y el algoritmo de K-means.
        
        """
        #si la lista de hiperparametros esta completa y la imagen esta cargada se ejecuta k-means
        if self.__imageApp is not None and len(self.__listaHiperparametros):
            proceso = LoadingScreen(self)
            proceso.run(self.__imageApp, self.__listaHiperparametros)
                        
        else:
            #si una de las condiciones anteriores no se cumplio entonces retornar un mensaje de error
            messagebox.showerror(
                title="Error", 
                message=("No es posible ejecutar K-means. Revise que se cargó la imagen correctamente "
                "y configuró adecuadamente los hiperparámetros en el menú 'Herramientas' > 'Configuración'.")
            )


    def clearListaHiperparametros(self):
        """
        Limpia la lista de hiperparámetros.
        """
        self.__listaHiperparametros.clear()


    def setListaHiperparametros(self, params):
        """
        Establece los hiperparámetros del algoritmo.

        Args:
            - params (list): lista de hiperparámetros.
        """
        self.__listaHiperparametros.extend(params)
        

    def __creaMenu(self):
        """
        Retorna una barra de menú con las opciones de 'archivo', 'run', 'herramientas', 'ayuda' y 'acerca de'

        """
        newMenu = tk.Menu(self)

        file = tk.Menu(self, tearoff=0)
        run = tk.Menu(self, tearoff=0)
        tools = tk.Menu(self, tearoff=0)
        help = tk.Menu(self, tearoff=0)
        about = tk.Menu(self, tearoff=0)

        file.add_command(label="Abrir archivo", command=self.__openFile)
        file.add_separator()
        file.add_command(label="Salir", command=self.__salida)

        run.add_command(label="Run K-means", command=self.__comprobarHiperparametros)

        tools.add_command(label="Limpiar imagen", command=self.__clearImg)
        tools.add_separator()
        tools.add_command(label="Configuración", command=self.__showConfig)

        help.add_command(label="Instrucciones de uso", command=self.__showInstruc)

        about.add_command(label="Licencia", command=self.__showLicencia)
        about.add_command(label="Autor", command=self.__showAutor)

        newMenu.add_cascade(label="Archivo", menu=file)
        newMenu.add_cascade(label="Run", menu=run)
        newMenu.add_cascade(label="Herramientas", menu=tools)
        newMenu.add_cascade(label="Ayuda", menu=help)
        newMenu.add_cascade(label="Acerca de", menu=about)

        return newMenu


    def __openFile(self):
        """
        Carga una imagen seleccionada por el usuario
        """
        
        try:
            rutaImagen = fd.askopenfilename(title = "Abrir imagen", initialdir = "./", filetypes = (("Imágenes png", "*.png"), ("Imágenes jpg", "*.jpg")))
            imagen = Image.open(rutaImagen)
            
        except AttributeError as ae:
            print("Error al cargar el archivo")
            self.__clearImg()

        else:
            self.__clearImg()
            self.__imageApp = Imagen(imagen, rutaImagen)
            self.__imagenLabel = tk.Label(self.second_frame, image=self.__imageApp.getPhotoImage())
            self.__imagenLabel.pack()
            

    def __showConfig(self):
        """
        Muestra la ventana de confguracion de hiperparámetros del algoritmo.
        """
        if self.__ventanaConf is not None:
            self.__ventanaConf.destroy()
        self.__ventanaConf = Configuracion(self)
    

    def __clearImg(self):
        """
        Limpia la imagen cargada.
        """
        if self.__imageApp is not None:
            del self.__imageApp
            self.__imageApp = None
        
        if self.__imagenLabel is not None:
            self.__imagenLabel.destroy()


    def __salida(self):
        """
        Sale de la aplicación
        """
        self.destroy()
    

    def __showInstruc(self):
        """
        Muestra las instrucciones para ayudar al usuario a utilizar correctamente el programa.
        
        """
        messagebox.showinfo(
            title="Instrucciones",
            message=("1. Cargue la imagen en el menú 'Archivo'>'Abrir' y seleccione la imagen correspondiente\n"
            "2. Establezca los hiperparámetros de K-means en el menú 'Herramientas' > 'Configuración'\n"
            "3. Ejecute el algoritmo mediante el menú 'Run' > 'Run K-means'. El algoritmo puede tardarse dependiendo "
            "de los cálculos que haga el algoritmo, por favor espere a que termine.\n"
            "4. Una vez terminado el algoritmo se mostrará en una nueva ventana la imagen comprimida. En el"
            " menú 'Archivo' puede guardar la imagen en su PC.")
        )
    

    def __showLicencia(self):
        """
        Muestra licencia de uso.
        """
        messagebox.showinfo(
            title="Licencia",
            message="Programa de libre uso y de código abierto."
        )


    def __showAutor(self):
        """
        Muestra el autor del programa.
        
        """
        messagebox.showinfo(
            title="Autor",
            message="Programa creado por Sebastián Quiroga R."
        )



class Imagen():
    """
    Clase que crea un objeto Imagen. Los objetos de esta clase contendrán la ruta del aarchivo, la imagen 
    como objeto PIL.Image e ImageTk.photoImage.
    """
    def __init__(self, imagen, filename):
        self.__imagen = imagen
        self.__imagenPhoto = ImageTk.PhotoImage(imagen)
        self.__filename = filename
        
    def getExtension(self):
        """
        Retorna la extensión de la imagen como un string
        """
        extension = self.__filename.split(".")[-1]
        return extension

    def getImage(self):
        """
        Retorna la imagen como un objeto PIL.Image
        """
        return self.__imagen

    def getPhotoImage(self):
        """
        Retorna la imagen como un objeto PIL.ImageTk.PhotoImage
        """
        return self.__imagenPhoto

    



#########


class Configuracion(tk.Toplevel):
    """
    Ventana de configuración en donde se ingresan los hiperparámetros del algoritmo K-means.
    
    """
    def __init__(self, root):
        super().__init__(root)
        self.root = root

        labelClusters = tk.Label(self, text="Número de clusters:")
        self.__numberClusters = tk.Entry(
            self, 
            validate="key", 
            validatecommand=(self.register(self.__validaNum), "%P")
        )

        labelNumEjecuciones = tk.Label(self, text="Número de ejecuciones del algoritmo:")
        self.__numEjecuciones = tk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.__validaNum), "%P")
        )

        labelNumIters = tk.Label(self, text="Número de iteraciones por ejecución:")
        self.__numIters = tk.Entry(
            self,
            validate="key",
            validatecommand=(self.register(self.__validaNum), "%P")
        )
        buttonGuardar = tk.Button(self, text="Guardar", command=self.__validaCampos, pady=5)

        labelClusters.pack()
        self.__numberClusters.pack()
        labelNumEjecuciones.pack()
        self.__numEjecuciones.pack()
        labelNumIters.pack()
        self.__numIters.pack()
        buttonGuardar.pack()


    def __validaNum(self, val):
        """
        Valida que en un entry se escriban solamente números o esté vacío.
        
        Args: 
            - val (str): valor actual del entry luego de la inserción
        Returns:
            - (bool): True si es válido val. Caso contrario, False.
        """
        if val.isdecimal() or val == "":
            return True
        return False


    def __validaCampos(self):
        """
        Valida que los hiperparámetros ingresados por el usuario sean válidos antes de guardarlos.

        """
        flag = False

        lista = [self.__numberClusters.get(), self.__numEjecuciones.get(), self.__numIters.get()]
        
        for _, param in enumerate(lista):
            if param == "":
                flag = True
        
        if flag:
            messagebox.showerror(title="Error", message="Uno o más campos están vacíos")
        
        else:

            self.root.clearListaHiperparametros()        
            self.root.setListaHiperparametros((
                int(lista[0]),
                int(lista[1]),
                int(lista[2])
            ))

            messagebox.showinfo(
                title="Aviso",
                message="Configuración guardada correctamente."
            )

            self.destroy()




######

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
            VentanaResultado(self.root, self.__imagen, self.__ext)
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
            print("terminamos")


    def transformImagen(self, imagen):
        """
        Transforma la imagen procesada por K-means. Los valores de la imagen son float, 
        para poder convertirlo en PIL.Image deben ser uint8

        Args:
            - imagen (ndarray (m,n,3)): imagen procesada por el algoritmo K-means.
        
        Returns:
            - img (PIL.Image): imagen transformada
        """
        img = Image.fromarray((imagen * 255).astype(np.uint8))
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



#######


class VentanaResultado(tk.Toplevel):
    """
    Ventana que muestra la imagen retornada por el algoritmo K-means.
    """
    def __init__(self, root, imagen, extension):
        super().__init__(root)
        self.__imagen = imagen
        self.__imagenPhoto = ImageTk.PhotoImage(imagen)
        self.__extension = extension

        root.deiconify()
        root.clearListaHiperparametros()

        # menu #
        self.__myMenu = self.__creaMenu()
        self.config(menu=self.__myMenu)

        #### scrolleable

        main_frame = tk.Frame(self)
        main_frame.pack(fill='both', expand=1)

        my_canvas = tk.Canvas(main_frame)


        my_scrollbary = ttk.Scrollbar(main_frame, orient='vertical', command=my_canvas.yview)
        my_scrollbary.pack(side='right', fill='y')

        my_scrollbarx = ttk.Scrollbar(main_frame, orient='horizontal', command=my_canvas.xview)
        my_scrollbarx.pack(side='bottom', fill='x')

        my_canvas.pack(side='top', fill='both', expand=1)

        my_canvas.configure(yscrollcommand=my_scrollbary.set)
        my_canvas.configure(xscrollcommand=my_scrollbarx.set)
        my_canvas.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

        second_frame = tk.Frame(my_canvas)
        my_canvas.create_window((0,0), window=second_frame, anchor="nw") 

        self.__imagenComprimida = tk.Label(second_frame, image=self.__imagenPhoto)
        self.__imagenComprimida.pack()


    def __descargarImagen(self):
        """
        Guarda la imagen en disco.
        """
        self.__imagen.save("image." + self.__extension)
        messagebox.showinfo(
            title="Aviso",
            message="Imagen descargada"
        )
    
    def __creaMenu(self):
        """
        Retorna una barra de menú con las opciones de 'archivo'
        """
        newMenu = tk.Menu(self)
        file = tk.Menu(self, tearoff=0)        
        file.add_command(label="Descargar imagen", command=self.__descargarImagen)
        newMenu.add_cascade(label="Archivo", menu=file)

        return newMenu





        





if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()
