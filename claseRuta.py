from datetime import datetime
from clasePaquete import Paquete
import random
import time
import threading
from claseRouter import Router

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
        try:
            if router.estado != "ACTIVO":
                raise Exception(f"{router.nombre} no puede crear un paquete. Está inhabilitado.")
            else:
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
                    id_paquete = router.paquetes_enviados[-1].metadata["id"] + 1
                    paquete = Paquete("Hola", {"id": id_paquete, "fecha": ahora, "origen": router, "destino": router_destino} )
                    router.paquetes_enviados.append(paquete)
                
                print(router_destino.nombre)
                self.viajePaquete(paquete, router)

        except Exception as e:
             print(e)
            
        
    # Funcion agregar paquete a la red

    def viajePaquete(self, paquete, router):
        
        router_actual = None # Router_actual es el router que contiene actualmente el paquete
        router_a_enviar = None # Router_a_enviar es el router que debe retransmitir el paquete (siguiente o anterior al router que tiene el paquete)
        coordenada_origen = int(router.nombre[-1])
        coordenada_destino = int(paquete.metadata["destino"].nombre[-1])
        # contador0 = 0
        # print(router.habilitado)
        # while not router.habilitado:
        #     if contador0 == 0:
        #         print(f'esperando a que se habilite el {router.nombre}')
        #     contador0 += 1
        # router.latencia()
        try:
            if router.estado != "ACTIVO":
                raise Exception(f"{router.nombre} no puede crear un paquete. Está inhabilitado.")
            else:
                inicio = True
                print(router.nombre)

                if coordenada_destino > coordenada_origen:
                    router_actual = router.siguiente
                    while router_actual.estado != 'ACTIVO':
                        print(f"{router_actual.nombre} baypaseado")
                        router_actual = router_actual.siguiente 
                    router_actual.retransmiciones_pendientes.agregar(paquete)
                    
                    while inicio:
                        
                        if router_actual != paquete.metadata["destino"]:
                            router_a_enviar = getattr(router_actual, "siguiente")
                            
                            # Chequea si el router_a_enviar está habilitado
                            while router_a_enviar.estado != 'ACTIVO':
                                print(f"{router_a_enviar.nombre} baypaseado")
                                router_a_enviar = getattr(router_a_enviar, "siguiente")
                                if router_a_enviar == paquete.metadata["destino"] and router_a_enviar.estado != 'ACTIVO':
                                    pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                            
                            # Esperar hasta que el router actual esté habilitado
                            while not router_actual.habilitado:
                                time.sleep(0.01)  # Pequeña pausa para evitar consumo excesivo de CPU
                                
                            router_actual.latencia_event.wait()
                            router_a_enviar.retransmiciones_pendientes.agregar(paquete)
                            
                            #Considerar que restransmiciones sea un contador y no una lista --> Porque no necesitamos manipular los objetos de esa lista, sino solo contarlos para estadisticas
                            # contador = 0
                            print(router_actual, paquete.metadata["id"])
                            # while not router_actual.habilitado:
                            #     if contador == 0:
                            #         print(f'esperando a que se habilite el {router_actual.nombre}')
                            #     contador += 1
                            router_actual.retransmiciones.append(paquete)
                            # latencia_thread = threading.Thread(target=router_actual.latencia)
                            # latencia_thread.start()
                            # latencia_thread.join()
                            router_actual.retransmiciones_pendientes.borrar()

                            router_actual = router_a_enviar
                        else:
                            if router_actual.estado != 'ACTIVO':
                                pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                            else:
                                router_actual.recepciones.append(paquete)
                                print(router_actual.nombre, paquete.metadata["id"])
                                inicio = False

                else:
                    router_actual = router.anterior

                    while router_actual.estado != 'ACTIVO':
                        print(f"{router_actual.nombre} baypaseado")
                        router_actual = router_actual.anterior

                    router_actual.retransmiciones_pendientes.agregar(paquete)
                    while inicio:
                        print(router_actual)
                        if router_actual != paquete.metadata["destino"]:
                            router_a_enviar = getattr(router_actual, "anterior")
                            
                            #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                            while router_a_enviar.estado != 'ACTIVO':
                                print(f"{router_a_enviar.nombre} baypaseado")
                                router_a_enviar = getattr(router_a_enviar, "anterior")
                                if router_a_enviar == paquete.metadata["destino"] and router_a_enviar.estado != 'ACTIVO':
                                    
                                    pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                            

                            # Esperar hasta que el router actual esté habilitado
                            while not router_actual.habilitado:
                                time.sleep(0.01)  # Pequeña pausa para evitar consumo excesivo de CPU

                            router_actual.latencia_event.wait()
                            router_a_enviar.retransmiciones_pendientes.agregar(paquete)

                            router_actual.retransmiciones.append(paquete)
                            router_actual.retransmiciones_pendientes.borrar()

                            router_actual = router_a_enviar
                        
                        else:
                            if router_actual.estado != 'ACTIVO':
                                pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                            else:
                                router_actual.recepciones.append(paquete)
                                print(router_actual.nombre, paquete.metadata["id"])
                                inicio = False
                
                print(router_actual.recepciones[-1].metadata)

        except Exception as e:
             print(e)
    
    def iniciarLatenciaRouters(self):
        for router in self.routers:
            threading.Thread(target=router.iniciarLatencia, daemon=True).start()
            
        

    def averiaAleatoria(self):
        pos_aleatoria = random.randint(0,len(self.routers)-1)
        router = self.routers[pos_aleatoria]
        print(router.nombre)
        print(router.estado)
        router.estado = "EN_RESET"
        print(router.nombre)
        print(router.estado)
        tiempo_aleatorio = random.randint(5, 10)

        print(tiempo_aleatorio)

        time.sleep(tiempo_aleatorio)

        router.estado = "ACTIVO"
        print(router.nombre)
        print(router.estado)




        

