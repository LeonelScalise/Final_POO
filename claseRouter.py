from clasePaquete import Paquete
from datetime import datetime
from claseCola import Cola
import threading
import time
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
        self.habilitado = True
        self.latencia_event = threading.Event()
        
    def crearPaquete(self, mensaje:str, destino):

        if len(self.paquetes_enviados) == 0:
            id = 1
        else:
            id = self.paquetes_enviados[-1].metadata["id"] + 1
        
        hoy = datetime.now()
        newPaquete = Paquete(mensaje, {"id": id, "fecha": hoy, "origen": self, "destino": destino} )
        
        self.paquetes_enviados.append(newPaquete)
        
        return newPaquete
        
    def __str__(self) -> str:
        return self.nombre
    
    def iniciarLatencia(self):
        while True:
            self.latencia_event.set()  # Desbloquea el envío y la recepción de paquetes
            self.habilitado = True  # El router está habilitado
            time.sleep(5)  # Tiempo de latencia de 100 ms
            self.habilitado = False  # El router está deshabilitado durante el tiempo de latencia
            self.latencia_event.clear()  # Bloquea el envío y la recepción de paquetes

    # def latencia(self):
    #     self.habilitado = False
    #     time.sleep(1)
    #     self.habilitado = True

    def ordenarPaquetes(self):
        pass

    def averia(self):
        self.estado == "EN_RESET"