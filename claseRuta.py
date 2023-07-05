from claseRouter import *

class Ruta:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.routers = []

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

    def crearPaqueteDeRouter(self, router):
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
        
        if router.paquetes_enviados == []:
            paquete = Paquete("Hola", {"id": 1, "fecha": ahora, "origen": router, "destino": router_destino})
            router.paquetes_enviados.append(paquete)
            
        else:
            id_paquete = router.paquetes_enviados[-1].id + 1
            paquete = Paquete("Hola", {"id": id_paquete, "fecha": ahora, "origen": router, "destino": router_destino} )
            router.paquetes_enviados.append(paquete)
            
        
        #funcion agregar paquete a la red

    def viajePaquete(self, paquete, router):
        router_actual = None
        router_a_enviar = None
        if int(paquete.metadata["destino"].nombre[-1]) > int(router.nombre[-1]):
            router_actual = router.siguiente
            router_actual.retransmiciones_pendientes.append(paquete)
            inicio = False
            while inicio:
                if router_actual != paquete.metadata["destino"]:
                    router_a_enviar = getattr(router_actual, "siguiente")
                    
                    #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                    router_a_enviar.retransmiciones_pendientes.append(paquete)

                    router_actual.retransmiciones_hechas.append(paquete)
                    router_actual.retransmiciones_pendientes.remove(paquete)

                    router_actual = router_a_enviar
                else:
                    router_actual.recepciones.append(paquete)
                    inicio = False

        else:
            router_actual = router.anterior
            router_actual.retransmiciones_pendientes.append(paquete)
            inicio = False
            while inicio:
                if router_actual != paquete.metadata["destino"]:
                    router_a_enviar = getattr(router_actual, "anterior")
                    
                    #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                    router_a_enviar.retransmiciones_pendientes.append(paquete)

                    router_actual.retransmiciones_hechas.append(paquete)
                    router_actual.retransmiciones_pendientes.remove(paquete)

                    router_actual = router_a_enviar
                
                else:
                    router_actual.recepciones.append(paquete)
                    inicio = False




        

    # def imprimirRuta(self):
    #     router_actual = self.primero
    #     while router_actual:
    #         print(f"Router: {router_actual.nombre}")
    #         router_actual = router_actual.siguiente