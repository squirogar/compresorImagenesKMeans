import tkinter as tk
from tkinter import messagebox

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

