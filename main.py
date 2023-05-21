import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from PIL import ImageTk, Image
from tkinter import messagebox
import Kmeans as km
import numpy as np


class Aplicacion(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Compresor de imágenes K-means")
        self.resizable(True, True)  
        self.__imagen = None # esta es PIL image
        self.__photoImagenSubida = None #esta es PhotoImage
        self.__ventanaConf = None
        self.__listaHiperparametros = []

        # menu #
        self.__myMenu = self.__creaMenu()
        self.config(menu=self.__myMenu)

        # open file #
        tk.Button(self, text="Abrir archivo", command=self.__openFile).pack()
        self.__imagenLabel = tk.Label(self, image=self.__photoImagenSubida)
        

        # run k-means #
        tk.Button(self, text="Run K-means", command=self.__comprobarHiperparametros).pack()
        self.__imagenLabel.pack()

        


    def __comprobarHiperparametros(self):
        #print(self.__imagen == None)
        #print(len(self.__listaHiperparametros))
        #si la lista de hiperparametros esta completa y la imagen esta cargada se ejecuta k-means
        if self.__imagen != None and len(self.__listaHiperparametros):
            proceso = LoadingScreen(self, self.__imagen, self.__listaHiperparametros)
            imagenComprimida = proceso.getImagen()
            proceso.destroy()
            ventanaImagen = VentanaResultado(self, imagenComprimida)
            
        else:
            #si una de las condiciones anteriores no se cumplio entonces retornar un mensaje de error
            messagebox.showerror(
                title="Error", 
                message=("No es posible ejecutar K-means. Revise que se cargó la imagen correctamente "
                "y configuró adecuadamente los hiperparámetros en el menú Herramientas -> Configuración.")
            )


    def clearListaHiperparametros(self):
        self.__listaHiperparametros.clear()

    def setListaHiperparametros(self, params):
        self.__listaHiperparametros.extend(params)
        print(self.__listaHiperparametros)

    def __creaMenu(self):
        """
        Retorna una barra de menú con las opciones de "archivo", "herramientas", "ayuda" y "acerca de"

        """
        newMenu = tk.Menu(self)

        file = tk.Menu(self, tearoff=0)
        tools = tk.Menu(self, tearoff=0)
        help = tk.Menu(self, tearoff=0)
        about = tk.Menu(self, tearoff=0)

        file.add_command(label="Salir", command=self.__salida)

        tools.add_command(label="Limpiar imagen", command=self.__clearImg)
        tools.add_separator()
        tools.add_command(label="Configuración", command=self.__showConfig)

        help.add_command(label="Instrucciones de uso", command=self.__showInstruc)

        about.add_command(label="Licencia", command=self.__showLicencia)
        about.add_command(label="Autor", command=self.__showAutor)

        newMenu.add_cascade(label="Archivo", menu=file)
        newMenu.add_cascade(label="Herramientas", menu=tools)
        newMenu.add_cascade(label="Ayuda", menu=help)
        newMenu.add_cascade(label="Acerca de", menu=about)

        return newMenu

    def __openFile(self):
        # retorna la direccion donde esta la imagen
        try:
            fichero = fd.askopenfilename(title = "Abrir imagen", initialdir = "./", filetypes = (("Imágenes png", "*.png"), ("Imágenes jpg", "*.jpg")))
            print(fichero)
            imagen = Image.open(fichero)
            photoImagen = ImageTk.PhotoImage(imagen)
            
        except AttributeError as ae:
            print("Error al cargar el archivo")
            self.__clearImg()

        else:
            print("else :)")
            self.__clearImg()
            self.__imagenLabel = tk.Label(self, image=photoImagen)
            self.__imagenLabel.pack()
            self.__imagen = imagen
            self.__photoImagenSubida = photoImagen

    def __showConfig(self):
        
        if self.__ventanaConf is not None:
            self.__ventanaConf.destroy()
            print("destroyed")
        self.__ventanaConf = Configuracion(self)
    
    def __clearImg(self):
        self.__imagen = None
        self.__photoImagenSubida = None
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





class Configuracion(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

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
        #labelVerbose = tk.Label(self, text="Información adicional durante ejecución:")
        #self.__verbose = tk.IntVar()
        #RBNo = tk.Radiobutton(self, text="No", variable=self.__verbose, value=0)
        #RBYes = tk.Radiobutton(self, text="Yes", variable=self.__verbose, value=1)
        buttonGuardar = tk.Button(self, text="Guardar", command=lambda:self.__validaCampos(root))


        labelClusters.pack()
        self.__numberClusters.pack()
        labelNumIters.pack()
        self.__numIters.pack() 
        #labelVerbose.pack()
        #RBNo.pack()
        #RBYes.pack()
        buttonGuardar.pack()

    def __validaNum(self, val):
        if val.isdecimal():
            return True
        return False

    def __validaCampos(self, root):
        flag = False

        lista = [self.__numberClusters, self.__numEjecuciones, self.__numIters,]
        for _, param in enumerate():
            if param.get() == "":
                flag = True
        
        if flag:
            messagebox.showerror(title="Error", message="Uno o más campos están vacíos")
        else:

            root.clearListaHiperparametros()
            
            root.setListaHiperparametros((
                int(self.__numberClusters.get()),
                int(self.__numIters.get()),
                int(self.__verbose.get())
            ))

            messagebox.showinfo(
                title="Aviso",
                message="Configuración guardada correctamente."
            )

            self.destroy()






class LoadingScreen(tk.Toplevel):
    def __init__(self, root, imagen, hiperparametros):
        super().__init__(root)
        pb = ttk.Progressbar(
            self, 
            orient="horizontal", 
            mode="indeterminate", 
            length="300")
        
        mensaje = tk.Label(
            self, 
            text="Algoritmo de clustering K-means ejecutandose, por favor espere..."
        )


        pb.pack()
        mensaje.pack()

        pb.start()

        imagen = np.array(imagen)
        self.__run_algorithm(imagen, hiperparametros)
        
        pb.stop()



    def __run_algorithm(self, imagen_original, hiperparametros):
        num_clusters, num_ejecuciones, num_iter = hiperparametros
        # hiperparametro es una lista 
        # se llama a fit()
        model = km.KMeans(num_clusters, num_ejecuciones, num_iter)
        _, centroids, index_centroids = model.fit(imagen_original)
        # fit retorna costo, centroids, index_centroids
        imagen = centroids[index_centroids]
        imagen = np.reshape(imagen, imagen_original.shape)

        pass


class VentanaResultado(tk.Toplevel):
    def __init__(self, root, imagen):
        super().__init__(root)
        self.__imagenComprimida = tk.Label(self, image=imagen)
        self.__imagenComprimida.pack()
        tk.Button("Descargar", command=self.__descargarImagen).pack()

    def __descargarImagen(self):
        pass



        





if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()


#frame = tk.Frame(root)



#root.mainloop()
