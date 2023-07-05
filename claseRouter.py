from clasePaquete import Paquete
from datetime import datetime
from claseCola import Cola
import random

class Router():
    def __init__(self, nombre, estado):
        self.nombre = nombre
        self.estado = estado
        self.retransmiciones_pendientes = Cola() # Retrasmiciones pendientes debe ser una cola
        self.retransmiciones = [] # Considerar que restransmiciones sea un contador y no una lista
        self.recepciones = []
        self.siguiente = None
        self.anterior = None
        self.paquetes_enviados = [] # Considerar que paquetes_enviados sea un contador y no una lista
        
    def crearPaquete(self, mensaje:str, destino):
        
        if len(self.paquetes_enviados) == 0:
            id = 1
        else:
            id = self.paquetes_enviados[-1].id + 1
        
        hoy = datetime.now()
        newPaquete = Paquete(mensaje, {"id": id, "fecha": hoy, "origen": self, "destino": destino} )
        
        self.paquetes_enviados.append(newPaquete)
        
        return newPaquete


    def ordenarPaquetes(self):
        pass

    def retransmitirPaquete(self):
        pass

    def averiar(self):
        pass