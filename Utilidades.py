from PIL import ImageTk

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

