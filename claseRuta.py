from datetime import datetime
from clasePaquete import Paquete
import random

class Ruta:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.routers = []

    # Se implementa una lista doblemente enlazada en el agregador de routers a la ruta para poder hacer envios en ambos sentidos
    def agregarRouter(self, router): 
        if self.primero is None:
            self.primero = router
            self.ultimo = router
            self.routers.append(router)
        else:
            router.anterior = self.ultimo
            self.ultimo.siguiente = router
            self.ultimo = router
            self.routers.append(router)

    # Creacion de paquetes desde un router a otro difente al azar dentro de la ruta --> Tendriamos que fijarnos si va en Router
    def crearPaqueteAleatorio(self, router):
        ahora = datetime.now()
        router_destino = None
        inicio = True
        while inicio:
            pos_router = random.randint(0, len(self.routers)-1)
            router_destino = self.routers[pos_router]
            if router_destino != router:
                inicio = False
            else:
                continue
            
        # Donde dice "hola", en realidad deberia haber un mensaje que podría ser al azar
        
        if len(router.paquetes_enviados) == 0:
            paquete = Paquete("Hola", {"id": 1, "fecha": ahora, "origen": router, "destino": router_destino})
            router.paquetes_enviados.append(paquete)
            
        else:
            id_paquete = router.paquetes_enviados[-1].id + 1
            paquete = Paquete("Hola", {"id": id_paquete, "fecha": ahora, "origen": router, "destino": router_destino} )
            router.paquetes_enviados.append(paquete)
            
        
    # Funcion agregar paquete a la red

    def viajePaquete(self, paquete, router):
        router_actual = None # Router_actual es el router que contiene actualmente el paquete
        router_a_enviar = None # Router_a_enviar es el router que debe retransmitir el paquete (siguiente o anterior al router que tiene el paquete)
        coordenada_origen = int(router.nombre[-1])
        coordenada_destino = int(paquete.metadata["destino"].nombre[-1])
        inicio = True

        if coordenada_destino > coordenada_origen:
            router_actual = router.siguiente 
            router_actual.retransmiciones_pendientes.agregar(paquete)
            
            while inicio:
                if router_actual != paquete.metadata["destino"]:
                    router_a_enviar = getattr(router_actual, "siguiente")
                    
                    #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                    #Retrasmiciones pendientes tiene que ser una cola
                    router_a_enviar.retransmiciones_pendientes.agregar(paquete)
                    print(router_actual.nombre,)
                    
                    #Considerar que restransmiciones sea un contador y no una lista --> Porque no necesitamos manipular los objetos de esa lista, sino solo contarlos para estadisticas
                    router_actual.retransmiciones.append(paquete)
                    router_actual.retransmiciones_pendientes.borrar()

                    router_actual = router_a_enviar
                else:
                    router_actual.recepciones.append(paquete)
                    inicio = False

        else:
            router_actual = router.anterior
            router_actual.retransmiciones_pendientes.agregar(paquete)
            while inicio:
                if router_actual != paquete.metadata["destino"]:
                    router_a_enviar = getattr(router_actual, "anterior")
                    
                    #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                    router_a_enviar.retransmiciones_pendientes.agregar(paquete)

                    router_actual.retransmiciones.append(paquete)
                    router_actual.retransmiciones_pendientes.borrar()

                    router_actual = router_a_enviar
                
                else:
                    router_actual.recepciones.append(paquete)
                    inicio = False




        

