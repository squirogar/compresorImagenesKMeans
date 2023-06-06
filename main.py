import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from PIL import ImageTk, Image
from tkinter import messagebox
import Kmeans as km
import numpy as np
from threading import Thread
import queue

class Aplicacion(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Compresor de imágenes K-means")
#        self.resizable(True, True)

        # objeto imagen #
        self.__imageApp = None
        #self.__imagen = None # esta es PIL image
        #self.__photoImagenSubida = None #esta es PhotoImage

        self.__imagenLabel = None        
        #self.__imagenLabel = tk.Label(self)
        #self.__imagenLabel.pack()
        
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


        # buttons
        #tk.Button(self.second_frame, text="Abrir archivo", command=self.__openFile).pack()
        #tk.Button(self.second_frame, text="Run K-means", command=self.__comprobarHiperparametros).pack()

        


    def __comprobarHiperparametros(self):
        print(f"is not none la imagen? {self.__imageApp is not None}")
        print(f"is empty lista? {len(self.__listaHiperparametros)}")
        #print(len(self.__listaHiperparametros))
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
        self.__listaHiperparametros.clear()

    def setListaHiperparametros(self, params):
        self.__listaHiperparametros.extend(params)
        print(self.__listaHiperparametros)

    def __creaMenu(self):
        """
        Retorna una barra de menú con las opciones de 'archivo', 'herramientas', 'ayuda' y 'acerca de'

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
        # retorna la direccion donde esta la imagen
        try:
            rutaImagen = fd.askopenfilename(title = "Abrir imagen", initialdir = "./", filetypes = (("Imágenes png", "*.png"), ("Imágenes jpg", "*.jpg")))
            print(rutaImagen)

            imagen = Image.open(rutaImagen)
            
            
            #photoImagen = ImageTk.PhotoImage(imagen)
            
        except AttributeError as ae:
            print("Error al cargar el archivo")
            self.__clearImg()

        else:
            print("else :)")
            self.__clearImg()

            self.__imageApp = Imagen(imagen, rutaImagen)
            self.__imagenLabel = tk.Label(self.second_frame, image=self.__imageApp.getPhotoImage())
            self.__imagenLabel.pack()
            #self.__imagen = imagen
            #self.__photoImagenSubida = photoImagen

    def __showConfig(self):
        
        if self.__ventanaConf is not None:
            self.__ventanaConf.destroy()
            print("destroyed")
        self.__ventanaConf = Configuracion(self)
    
    def __clearImg(self):
        if self.__imageApp is not None:
            del self.__imageApp
            self.__imageApp = None
        
        if self.__imagenLabel is not None:
            self.__imagenLabel.destroy()


    def __salida(self):
        self.destroy()
    
    def __showInstruc(self):
        messagebox.showinfo(
            title="Instrucciones",
            message=("1. Cargue la imagen presionando el boton 'Abrir' y seleccione la imagen correspondiente\n"
            "2. Establezca los hiperparámetros de K-means en el menú 'Herramientas' > 'Configuración'\n"
            "3. Presione el botón 'Run K-means' para ejecutar el algoritmo K-means. El algoritmo puede tardarse"
            " dependiendo de los cálculos que hace el algoritmo, por favor espere a que termine.\n"
            "4. Una vez terminado el algoritmo se mostrará en una nueva ventana la imagen comprimida. En el"
            " menú 'opciones' puede guardar la imagen en su PC.")
        )
    
    def __showLicencia(self):
        messagebox.showinfo(
            title="Licencia",
            message="Programa de libre uso y de código abierto."
        )

    def __showAutor(self):
        messagebox.showinfo(
            title="Autor",
            message="Programa creado por Sebastián Quiroga R."
        )

######
class Imagen():
    def __init__(self, imagen, filename):
        self.__imagen = imagen
        self.__imagenPhoto = ImageTk.PhotoImage(imagen)
        self.__filename = filename
        
    def getExtension(self):
        extension = self.__filename.split(".")[-1]
        print(extension)
        return extension

    def getImage(self):
        return self.__imagen

    def getPhotoImage(self):
        return self.__imagenPhoto

    



#########


class Configuracion(tk.Toplevel):
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
        buttonGuardar = tk.Button(self, text="Guardar", command=self.__validaCampos)


        labelClusters.pack()
        self.__numberClusters.pack()
        labelNumEjecuciones.pack()
        self.__numEjecuciones.pack()
        labelNumIters.pack()
        self.__numIters.pack()
        buttonGuardar.pack()

    def __validaNum(self, val):
        if val.isdecimal() or val == "":
            return True
        return False

    def __validaCampos(self):
        flag = False

        lista = [self.__numberClusters.get(), self.__numEjecuciones.get(), self.__numIters.get()]
        print(f"lista {lista}")
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
    def __init__(self, root):#, imagen, hiperparametros):
        super().__init__(root)
        self.root = root
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

        #self.__imagen = None
        
        self.__pb.pack()
        self.__pb.start()
        #self.__hiperparametros = hiperparametros

        mensaje.pack()



    def run(self, imagen, hiperparametros):
        self.root.withdraw()
        self.__imagen = imagen.getImage()
        self.__ext = imagen.getExtension()
        self.__cola = queue.Queue()
        self.__thread1 = Thread(target=self.__run_algorithm, args=(self.__imagen, hiperparametros, self.__cola), daemon=True)
        #__run_algoritm debe tener acceso a la queue
        self.__thread1.start()

        self.__check_queue()


    def __check_queue(self):
        print("check queue")
        if self.__thread1.is_alive():
            # si aun esta vivo el hilo, volver a preguntar si termino despues de un tiempo
            self.root.after(5000, self.__check_queue)
        self.__access_queue()
        print(f"is alive {self.__thread1.is_alive()}")

        if not self.__thread1.is_alive():
            self.__pb.stop()
            
            VentanaResultado(self.root, self.__imagen, self.__ext)
            messagebox.showinfo(title="Aviso", message="Proceso finalizado")
            
            self.destroy()
        #if not self.running:
            # This is the brutal stop of the system.  You may want to do
            # some cleanup before actually shutting it down.
        #    import sys
        #    sys.exit(1)

    def __access_queue(self):
        print("access queue")
        # si la cola no esta vacia, entonces sacamos la imagen, ya que el hilo termino su ejecucion
        if self.__cola.qsize():
            try:
                img = self.__cola.get_nowait()
                self.__imagen = self.transformImagen(img)
            except queue.Empty:
                # get_nowait retorna un item sin bloquearse, sin embargo, si no hay nada disponible lanza
                # exception
                print("queue empty!")
                


    def __run_algorithm(self, imagen_original, hiperparametros, cola):
        # imagen_original es una PIL image
        # sin la división sería un array con int, necesitamos que sea float
        imagen = np.array(imagen_original) / 255
        #print(f"original {imagen.shape}")
        m, n, p = imagen.shape
        # se hace un reshape a array2d
        imagen_2d = np.reshape(imagen, (m * n, p))
        #print(f"imagen reshape {imagen_reshape.shape}, {imagen_reshape.dtype}")

        #imagen_2d = self.__imageToArray(imagen_original) #matrix 2d
        num_clusters, num_ejecuciones, num_iter = hiperparametros
        #print(f"hip {hiperparametros}, img {imagen_original.shape}")
        # hiperparametro es una lista 
        # se llama a fit()
        model = km.KMeans(num_clusters, num_ejecuciones, num_iter)
        _, centroids, index_centroids = model.fit(imagen_2d, True)
        # fit retorna costo, centroids, index_centroids
        imagen_nueva = centroids[index_centroids] #matrix 2d
        imagen_nueva = np.reshape(imagen_nueva, (m, n, p)) #matrix 3d
        #print(f"imagen_comprimida {imagen_nueva.shape}, {imagen_nueva.dtype}")

        #import matplotlib.pyplot as plt
        #plt.imshow(imagen_nueva)
        
        cola.put(imagen_nueva)
        print("terminamos")


    def transformImagen(self, imagen):
        # los valores de la imagen nueva son float, para poder convertirlo en photoimage deben ser int
        #print(self.__imagen.dtype)
        return Image.fromarray((imagen * 255).astype(np.uint8))





#######


class VentanaResultado(tk.Toplevel):
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
        #tk.Button(second_frame, text="Descargar", command=self.__descargarImagen).pack()

    def __descargarImagen(self):
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
