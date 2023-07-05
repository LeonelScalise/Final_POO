from clasePaquete import Paquete
from datetime import datetime
import random

class Router():
    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado
        self.retransmiciones_pendientes = []
        self.retransmiciones_hechas = []
        self.recepciones = []
        self.siguiente=None
        self.anterior=None
        self.paquetes_enviados = []

    def ordenarPaquetes(self):
        pass

    def retransmitirPaquete(self):
        pass

    def averiar(self):
        pass