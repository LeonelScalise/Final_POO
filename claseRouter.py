from clasePaquete import Paquete
from datetime import datetime
from claseCola import Cola
import threading
import time
import random
import csv

class Router():
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = 'AGREGADO'
        self.retransmisiones_pendientes = Cola()
        self.retransmisiones = [] # Considerar que restransmiciones sea un contador y no una lista
        self.recepciones = []
        self.siguiente = None
        self.anterior = None
        self.paquetes_enviados = [] # Considerar que paquetes_enviados sea un contador y no una lista
        self.habilitado = True
        
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
    

    def latencia(self):
        self.habilitado = False
        time.sleep(0.1)
        self.habilitado = True


    def averia(self):
        if self.estado == 'ACTIVO':
            self.estado == "EN_RESET"
            self.registrarEvento()
        else:
            print('No se puede averiar un router INACTIVO o que ya este EN_RESET')

# Este metodo permite ordenar los paquetes que se encuentran en la lista recepciones ya que primero
# ordena por coordenada router de manera ascendente y luego procede a ordenar por id del paquete.
    def ordenarPaquetes(self):

        self.recepciones.sort(key=lambda p: (p.metadata['origen'].nombre[-1], p.metadata['id']))
    

    def registrarEvento(self):
        fecha_hora= datetime.now().strftime("%d-%m-%y %H:%M:%S")

        with open('system_log.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.nombre.upper(), fecha_hora, self.estado])


if __name__=='__main__':

    r1=Router('ruter1','Activo')
    r2=Router('ruter2','Activo')
    r3=Router('ruter3','Activo')

    p1=Paquete('caca',{"id": 1, "fecha": None, "origen": r3, "destino": r1})
    p2=Paquete('de mi culo',{"id": 2, "fecha": None, "origen": r3, "destino": r1})
    p3=Paquete('sale mas linda',{"id": 3, "fecha": None, "origen": r3, "destino": r1})
    p4=Paquete('estoy con diarrea',{"id": 1, "fecha": None, "origen": r2, "destino": r1})
    p5=Paquete('tengo que comer',{"id": 2, "fecha": None, "origen": r2, "destino": r1})
    p6=Paquete('arroz',{"id": 3, "fecha": None, "origen": r2, "destino": r1})
    p7=Paquete('con pollo',{"id": 4, "fecha": None, "origen": r3, "destino": r1})

    r1.recepciones.append(p2)
    r1.recepciones.append(p1)
    r1.recepciones.append(p5)
    r1.recepciones.append(p6)
    r1.recepciones.append(p3)
    r1.recepciones.append(p7)
    r1.recepciones.append(p4)

    r1.ordenarPaquetes()
    for paquete in r1.recepciones:
        print(paquete.mensaje,paquete.metadata['origen'].nombre)


    





        

