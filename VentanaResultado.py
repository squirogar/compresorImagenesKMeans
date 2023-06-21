import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from tkinter import messagebox

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

