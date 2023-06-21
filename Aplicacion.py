import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from PIL import Image
from tkinter import messagebox
import LoadingScreen as ls
import Utilidades as ut
import Configuracion as conf

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
            proceso = ls.LoadingScreen(self)
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
            imagen = imagen.convert("RGB")
            self.__imageApp = ut.Imagen(imagen, rutaImagen)
            self.__imagenLabel = tk.Label(self.second_frame, image=self.__imageApp.getPhotoImage())
            self.__imagenLabel.pack()
            

    def __showConfig(self):
        """
        Muestra la ventana de confguracion de hiperparámetros del algoritmo.
        """
        if self.__ventanaConf is not None:
            self.__ventanaConf.destroy()
        self.__ventanaConf = conf.Configuracion(self)
    

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
