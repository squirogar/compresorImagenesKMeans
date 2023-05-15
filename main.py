import tkinter as tk
import tkinter.filedialog as fd
from PIL import ImageTk, Image
from tkinter import messagebox

class Aplicacion(tk.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("Compresor de imágenes K-means")
        self.resizable(True, True)  
        self.__imagen = None
        self.__ventanaConf = None

        # menu #
        self.__myMenu = self.__creaMenu()
        self.config(menu=self.__myMenu)

        # open file #
        tk.Button(self, text="Abrir archivo", command=self.__openFile).pack()
        self.__imagenLabel = tk.Label(self, image=self.__imagen)
        self.__imagenLabel.pack()

        # run k-means #
        tk.Button(self, text="Run K-means", command=self.__comprobarHiperparametros).pack()


    def __comprobarHiperparametros(self):
        
        #si la lista de hiperparametros esta completa y la imagen esta cargada se ejecuta k-means
        #si una de las condiciones anteriores no se cumplio entonces retornar un mensaje de error
        messagebox.showerror(
            title="Error", 
            message=("No es posible ejecutar K-means. Revise que se cargó la imagen correctamente "
            "y configuró adecuadamente los hiperparámetros en el menú Herramientas -> Configuración.")
        )    


    def __creaMenu(self):
        newMenu = tk.Menu(self)

        file = tk.Menu(self, tearoff=0)
        tools = tk.Menu(self, tearoff=0)
        help = tk.Menu(self, tearoff=0)
        about = tk.Menu(self, tearoff=0)

        file.add_command(label="Abrir archivo")
        file.add_command(label="Cerrar archivo")
        file.add_separator()
        file.add_command(label="Salir")

        tools.add_command(label="Configuración", command=self.__showConfig)

        help.add_command(label="Guía de uso")

        about.add_command(label="Licencia")
        about.add_command(label="Autor")

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
            imagen = ImageTk.PhotoImage(Image.open(fichero))
        except AttributeError as ae:
            print("Error al cargar el archivo")
        else:
            print("else :)")
            self.__imagenLabel.destroy()
            self.__imagenLabel = tk.Label(self, image=imagen)
            self.__imagenLabel.pack()
            self.__imagen = imagen

    def __showConfig(self):
        
        if self.__ventanaConf is not None:
            self.__ventanaConf.destroy()
            print("destroyed")
        self.__ventanaConf = Configuracion(self)
    
    
        
        


class Configuracion(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        labelClusters = tk.Label(self, text="Número de clusters:")
        self.__numberClusters = tk.Entry(
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
        labelVerbose = tk.Label(self, text="Información adicional durante ejecución:")
        self.__verbose = tk.IntVar()
        RBNo = tk.Radiobutton(self, text="No", variable=self.__verbose, value=0)
        RBYes = tk.Radiobutton(self, text="Yes", variable=self.__verbose, value=1)
        buttonGuardar = tk.Button(self, text="Guardar", command=self.__validaCampos)


        self.__listaHiperparametros = None

        labelClusters.pack()
        self.__numberClusters.pack()
        labelNumIters.pack()
        self.__numIters.pack() 
        labelVerbose.pack()
        RBNo.pack()
        RBYes.pack()
        buttonGuardar.pack()

    def __validaNum(self, val):
        if val.isdecimal():
            return True
        return False

    def __validaCampos(self):
        print("verbose: ", self.__verbose.get())
        flag = False
        if self.__numberClusters.get() == "" or self.__numIters.get() == "":
            flag = True

        if flag:
            messagebox.showerror(title="Error", message="Uno o más campos están vacíos")
        else:
            if self.__listaHiperparametros is not None:
                del self.__listaHiperparametros
            self.__listaHiperparametros = []
            
            self.__listaHiperparametros.extend(
                self.__numberClusters.get(),
                self.__numIters.get(),
                self.__verbose.get()
            )
    
    #def getListaHiperparametros(self):
    #    return self.__listaHiperparametros


class VentanaResultado(tk.Toplevel):
    def __init__(self, root, imagen):
        super().__init__(root)
        self.__imagenComprimida = tk.Label(self, image=imagen)
        self.__imagenComprimida.pack()
        tk.Button("Descargar", command=self.__descargarImagen).pack()

    def __descargarImagen(self):
        pass



class LoadingScreen(tk.Toplevel):
    pass



if __name__ == "__main__":
    app = Aplicacion()
    app.mainloop()


#frame = tk.Frame(root)



#root.mainloop()
