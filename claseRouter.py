from clasePaquete import Paquete
from datetime import datetime
import time
import csv

class Router():
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = 'AGREGADO'
        self.retransmisiones_pendientes = []
        self.retransmisiones = []
        self.recepciones = []
        self.siguiente = None
        self.anterior = None
        self.envios_pendientes = []
        self.paquetes_enviados = []
        self.paquetes_creados = 0
        self.habilitado = True
        

    def crearPaquete(self, mensaje:str, destino):
        self.paquetes_creados += 1
        id = self.paquetes_creados
        
        if self.estado == 'ACTIVO':

            hoy = datetime.now()
            newPaquete = Paquete(mensaje, {"id": id, "fecha": hoy, "origen": self, "destino": destino} )
            self.envios_pendientes.append(newPaquete)
            return newPaquete
        else:
            print('No puede crear un paquete si el router no esta ACTIVO.')
        
        
    def __str__(self) -> str:
        return self.nombre
    

    def latencia(self):
        self.habilitado = False
        time.sleep(0.1)
        self.habilitado = True


    def averia(self):
        if self.estado == 'ACTIVO':
            self.estado = "EN_RESET"
            self.registrarEvento()
        else:
            print('No se puede averiar un router INACTIVO o que ya este EN_RESET')

    # Este metodo permite ordenar los paquetes que se encuentran en la lista recepciones ya que primero
    # Ordena por coordenada router de manera ascendente y luego procede a ordenar por id del paquete.
    def ordenarPaquetes(self):

        self.recepciones.sort(key=lambda p: (p.metadata['origen'].nombre[-1], p.metadata['id']))
    

    def registrarEvento(self):
        fecha_hora= datetime.now().strftime("%d-%m-%y %H:%M:%S")

        with open('system_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.nombre.upper(), fecha_hora, self.estado])





    





        

