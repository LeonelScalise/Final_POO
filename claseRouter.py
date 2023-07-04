class Router():
    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado
        self.retransmiciones = []
        self.recepciones = []
        self.siguiente=None
        self.anterior=None

    def ordenarPaquetes(self):
        pass

    def crearPaquete(self):
        pass

    def retransmitirPaquete(self):
        pass

    def averiar(self):
        pass