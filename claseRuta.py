from clasePaquete import Paquete
import random
import time
import threading
from popularNube import nube
import matplotlib.pyplot as plt
import numpy as np
import time


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
    
        
             
    # Funcion que procesa todos los envios y retransmisiones de paquetes de los routers

    def viajePaquete(self, paquete:Paquete, timeRef):
        origen = paquete.metadata['origen']
        router_actual = None # Router_actual es el router que contiene actualmente el paquete
        router_a_enviar = None # Router_a_enviar es el router que debe retransmitir el paquete (siguiente o anterior al router que tiene el paquete)
        coordenada_origen = int(origen.nombre[-1])
        coordenada_destino = int(paquete.metadata["destino"].nombre[-1])
        inicio = True

        try:
            if origen.estado != "ACTIVO":
                raise Exception(f"{origen.nombre} no puede crear un paquete. Está inhabilitado.")
            elif coordenada_destino == coordenada_origen:
                raise Exception("Un router no puede enviarse un paquete a sí mismo.")
            
            
            flagEnvPend = self.prioridadEnviosPendientes(paquete, origen, timeRef)

            if flagEnvPend:
                return
            
            flagRtxEnvio = self.prioridadRtxEnvio(paquete, origen, timeRef)

            if flagRtxEnvio:
                return
            
            threading.Thread(target = origen.latencia, daemon = True).start()
            
            origen.envios_pendientes.remove(paquete)
            origen.paquetes_enviados.append(paquete)
            
            print(f'{round(time.time() - timeRef, 2)} - {paquete.mensaje}: salio de {origen.nombre}')

            if coordenada_destino > coordenada_origen:
                sentido_tx = 'siguiente'
            else:
                sentido_tx = 'anterior'

            router_actual = getattr(origen, sentido_tx)

            router_actual = self.bypassAdyacentes(paquete, sentido_tx, router_actual, timeRef)
           
            
            flagNube1 = self.nubeRouterDesactivado(paquete, router_actual, timeRef)

            if flagNube1:
                return
                
            flagDestDes1 = self.routerDestinoDeshabilitado(paquete, router_actual, timeRef)
                
            if flagDestDes1:    
                return
            
            router_actual.retransmisiones_pendientes.append(paquete)
 
            # Arrancan las retransmisiones
            while inicio:
                if router_actual != paquete.metadata["destino"]:

                    router_a_enviar = getattr(router_actual, sentido_tx)

                    
                    flagRx = self.prioridadRetransmisiones(paquete, router_actual, timeRef)

                    if flagRx:
                        return
                                        
                    flagInterDesh = self.routerIntermediarioDeshabilitado(paquete, router_actual, timeRef)

                    if flagInterDesh:
                        return
                    
                    threading.Thread(target = router_actual.latencia, daemon = True).start()
                    router_actual.retransmisiones.append(paquete)
                    
                    print(f'{round(time.time() - timeRef, 2)} - {paquete.mensaje}: salio de {router_actual.nombre}')
                        
                    flagbypass, router_a_enviar = self.bypassNoAdyacente(paquete, sentido_tx, router_a_enviar, timeRef)

                    if flagbypass:
                        return    
                    
                    if router_a_enviar != paquete.metadata["destino"]:
                        router_a_enviar.retransmisiones_pendientes.append(paquete)
                    
                    router_actual.retransmisiones_pendientes.remove(paquete)
                    
                    router_actual = router_a_enviar
                    
                else:
                    if router_actual.estado != 'ACTIVO':
                        flagNube2 = self.nubeRouterDesactivado(paquete, router_actual, timeRef)
                        if flagNube2:
                            return
                    else:
                        flagDestDes2 = self.routerDestinoDeshabilitado(paquete, router_actual, timeRef)
                        if flagDestDes2:
                            return

        except Exception as e:
             print(e)
    
    # Revisa si un router de origen tiene envios pendientes. No debe enviar todos los mensajes al mismo tiempo, sino esperar la latencia
    def prioridadEnviosPendientes(self, paquete, origen, timeRef):
        c = 0
        flag = True
        while paquete != origen.envios_pendientes[0] or origen.estado != "ACTIVO":
            if origen.estado != "ACTIVO":
                print(f'{round(time.time() - timeRef, 2)} - Oh no!, en la espera de prioridad de envios pendientes para enviar el paquete {paquete.mensaje} el {origen.nombre} se averio, el paquete se ha perdido :c')
                return flag
            elif c == 0:
                print(f'{round(time.time() - timeRef, 2)} - El paquete {paquete.mensaje} debe esperar su turno, todavia hay envios pendientes.')
            c += 1
        flag = False
        return flag

    # Procesa la prioridad de retransmisiones vs. envios de un router de origen
    def prioridadRtxEnvio(self, paquete, origen, timeRef):
        c1, c2 = 0, 0
        flag = True
        while not origen.habilitado or not origen.retransmisiones_pendientes == [] or origen.estado != "ACTIVO":
            if origen.estado != "ACTIVO":
                print(f'{round(time.time() - timeRef, 2)} - Oh no!, en la espera de la latencia para enviar el paquete {paquete.mensaje} el {origen.nombre} se averio, el paquete se ha perdido :c')
                return flag
            elif not origen.habilitado and c1 == 0:
                print(f'{round(time.time() - timeRef, 2)} - Esperando a que se habilite el {origen.nombre} de origen.')
                c1 += 1
            elif not origen.retransmisiones_pendientes == [] and c2 == 0:
                print(f'{round(time.time() - timeRef, 2)} - El {origen.nombre} tiene retransmisiones pendientes, no puede enviar un paquete propio todavía.')
                c2 += 1
            time.sleep(0.05)
        flag = False
        return flag
    
    # Revisa si un router adyacente al de origen está habilitado y sino lo baypassea        
    def bypassAdyacentes(self, paquete, sentido_tx, router_actual, timeRef):
        while router_actual.estado != 'ACTIVO' and  router_actual != paquete.metadata["destino"]:
            
            print(f'{round(time.time() - timeRef, 2)} - {router_actual.nombre} bypasseado')
            router_actual = getattr(router_actual, sentido_tx)

        return router_actual

    # Revisa si un paquete de destino esta inahabilitado y en consecuencia envia el paquete a la nube para que espere a que se habilite y reenviarle el paquete
    def nubeRouterDesactivado(self, paquete, router_actual, timeRef):
        if router_actual == paquete.metadata["destino"] and router_actual.estado != 'ACTIVO':    
            self.enviarANube(paquete, router_actual)
            c1 = 0
            flag = True
            while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                if c1 == 0:
                    print(f'{round(time.time() - timeRef, 2)} - La nube esta esperando a que se active el {router_actual.nombre}.')
                c1 += 1
            c2 = 0
            while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                if c2 == 0:
                    print(f"{round(time.time() - timeRef, 2)} - Todavia no es el turno del paquete {paquete.mensaje} de volver de la nube.")
                c2 += 1
        
            router_actual.recepciones.append(paquete)
            
            nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
            print(f'{round(time.time() - timeRef, 2)} - Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')
            return flag
        
        flag = False
        return flag

     # Revisa si un router de destino cumplió su periodo de latencia para recibir o enviar un paquete
    def routerDestinoDeshabilitado(self, paquete, router_actual, timeRef):
        if router_actual == paquete.metadata["destino"]:          
            c = 0
            flag = True
            while not router_actual.habilitado or router_actual.estado != 'ACTIVO':
                if router_actual.estado != 'ACTIVO':
                    print(f'{round(time.time() - timeRef, 2)} - Oh no!, en la espera de la latencia para enviar el paquete {paquete.mensaje} el {router_actual.nombre} se averio, el paquete se ha perdido :c')
                    return flag
                elif c == 0:
                    print(f'{round(time.time() - timeRef, 2)} - Esperando a que se habilite el {router_actual.nombre}.')
                c += 1
            router_actual.recepciones.append(paquete)
            print(f'{round(time.time() - timeRef, 2)} - {paquete.mensaje}: estoy en {router_actual.nombre}')
            return flag
        
        flag = False
        return flag
    
    # Envia un paquete al espacio de nube de un determinado router
    def enviarANube(self, paquete, router):
       if router.nombre not in nube.paquetes_pendientes: 
            nube.paquetes_pendientes[router.nombre] = []
        
       nube.paquetes_pendientes[router.nombre].append(paquete)
    
    # Revisa si un paquete tiene prioridad de paso con respecto a las retransmisiones pendientes de un mismo router
    def prioridadRetransmisiones(self, paquete, router_actual, timeRef):
        c = 0
        flag = True
        while paquete != router_actual.retransmisiones_pendientes[0] or router_actual.estado != 'ACTIVO':
            if router_actual.estado != 'ACTIVO':
                print(f'{round(time.time() - timeRef, 2)} - Oh no!, en la espera de prioridad de retransmisiones pendientes para enviar el paquete {paquete.mensaje} el {router_actual.nombre} se averio, el paquete se ha perdido :c')
                return flag
            elif c == 0:
                print(f'{round(time.time() - timeRef, 2)} - El paquete {paquete.mensaje} no tiene prioridad de paso todavia en el {router_actual.nombre}')
            c += 1
        flag = False
        return flag
    
    # Revisa si un router intermediario cumplió su periodo de latencia para recibir o enviar un paquete
    def routerIntermediarioDeshabilitado(self, paquete, router_actual, timeRef):
        c = 0
        flag = True
        while not router_actual.habilitado or router_actual.estado != 'ACTIVO':
            if router_actual.estado != 'ACTIVO':
                print(f'{round(time.time() - timeRef, 2)} - Oh no!, en la espera de la latencia para enviar el paquete {paquete.mensaje} el {router_actual.nombre} se averio, el paquete se ha perdido :c')
                return flag
            elif c == 0:
                print(f'{round(time.time() - timeRef, 2)} - Esperando a que se habilite el {router_actual.nombre}.')
            c += 1
        flag = False
        return flag
    
    # Revisa si un router que no es adyacente al original esta inactivo o en_reset y lo bypassea
    def bypassNoAdyacente(self, paquete, sentido_tx, router_a_enviar, timeRef):
        flag = True
        while router_a_enviar.estado != 'ACTIVO' and router_a_enviar != paquete.metadata["destino"]:
            print(f'{round(time.time() - timeRef, 2)} - {router_a_enviar.nombre} bypasseado')
            router_a_enviar = getattr(router_a_enviar, sentido_tx)
            if router_a_enviar == paquete.metadata["destino"] and router_a_enviar.estado != 'ACTIVO':
                self.nubeRouterDesactivado(paquete, router_a_enviar, timeRef) #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                return flag, router_a_enviar
        flag = False
        return flag, router_a_enviar

# Este metodo permite crear un a averia aleatoria
    def averiaAleatoria(self, timeRef):
        pos_aleatoria = random.randint(0,len(self.routers)-1)
        inicio = True
        while inicio:
            router_a_averiar = self.routers[pos_aleatoria]
            if router_a_averiar.estado == 'ACTIVO':
                inicio = False
            else:
                continue
                
        router_a_averiar.estado = "EN_RESET"
        router_a_averiar.registrarEvento()
        
        tiempo_aleatorio = random.randint(5, 10)

        print(f'{round(time.time() - timeRef, 2)} - {router_a_averiar.nombre} reiniciando...')
        time.sleep(tiempo_aleatorio)

        router_a_averiar.estado = "ACTIVO"
        router_a_averiar.registrarEvento()
        print(f'{round(time.time() - timeRef, 2)} - {router_a_averiar.nombre} ACTIVO.')


    # Este metodo permite crear archivos .txt de cada router, en los cuales se puede observar los paquetes ordenados por cada router emisor
    def crearArchivos(self):
        for router in self.routers:
            if len(router.recepciones) != 0:
                nombre_archivo = f"{router.nombre}.txt"  
                with open(nombre_archivo, "w") as archivo:
                    origen_anterior = ''
                    flag = True
                    for paquete in router.recepciones:
                        origen = paquete.metadata['origen'].nombre
                        mensaje = paquete.mensaje
                        if origen != origen_anterior:
                            if not flag:
                                archivo.write('\n')
                            archivo.write(f"Origen: {origen}\n")
                            flag = False
                        archivo.write(f"{mensaje}\n")
                        origen_anterior = origen

    #Este metodo permite observar un grafico de barras donde se encuentran la cantidad de paquetes enviados y recibidos de cada router
    def graficoBarras(self):
        enviados = [len(router.paquetes_enviados) for router in self.routers]
        recibidos = [len(router.recepciones) for router in self.routers]
        
        x_axis = np.arange(len(self.routers))
        
        plt.bar(x_axis -0.2, enviados, width = 0.4, label = 'Enviados')
        plt.bar(x_axis +0.2, recibidos, width = 0.4, label = 'Recibidos')

        plt.xticks(x_axis, self.routers)

        # Agregado de leyenda

        plt.legend()

        plt.show()


    #Este metodo permite visualizar por terminal las tasas de retransmisiones y recepciones de paquetes
    def tasas(self):
        cantidad_total_de_retransmisiones = sum(len(router.retransmisiones) for router in self.routers)
        cantidad_total_de_recepciones = sum(len(router.recepciones) for router in self.routers)
        headers = ('Nombres', 'Recepciones', 'Retransmisiones')
        header_string = ' '.join(header.center(10) for header in headers)
        separator_string = '-' * len(header_string)

        print("\t\nESTADISTICAS\n")

        if cantidad_total_de_recepciones != 0 and cantidad_total_de_retransmisiones != 0:
            print(header_string)
            print(separator_string)

            data = [(router.nombre.upper(),
                    round(len(router.recepciones) / cantidad_total_de_recepciones, 2),
                    round(len(router.retransmisiones) / cantidad_total_de_retransmisiones, 2))
                    for router in self.routers]

            for fila in data:
                print(f'{fila[0]:^10s} {fila[1]:^10.2f} {fila[2]:>10.2f}')

        elif cantidad_total_de_retransmisiones == 0 and cantidad_total_de_recepciones != 0:
            print(header_string)
            print(separator_string)

            data = [(router.nombre.upper(),
                    round(len(router.recepciones) / cantidad_total_de_recepciones, 2))
                    for router in self.routers]

            for fila in data:
                print(f'{fila[0]:^10s} {fila[1]:>10.2f}')

            print("\nNo hay paquetes reenviados.\n")

        else:
            print("\nNo se han enviado paquetes.\n")
    


    
    # Esta funcion es para intentar simular de forma aleatoria el enrutamiento pero consideramos complica las muestras de las funcionalidades

    # def crearPaqueteAleatorio(self, router):
    #     ahora = datetime.now()
    #     router_destino = None
    #     inicio = True
    #     try:
    #         if router.estado != "ACTIVO":
    #             raise Exception(f"{router.nombre} no puede crear un paquete. Está inhabilitado.")
    #         else:
    #             while inicio:
    #                 pos_router = random.randint(0, len(self.routers)-1)
    #                 router_destino = self.routers[pos_router]
    #                 if router_destino != router:
    #                     inicio = False
    #                 else:
    #                     continue
                    
    #             # Donde dice "hola", en realidad deberia haber un mensaje que podría ser al azar
                
    #             if len(router.paquetes_enviados) == 0:
    #                 router.crearPaquete()
    #                 paquete = Paquete("Hola", {"id": 1, "fecha": ahora, "origen": router, "destino": router_destino})
    #                 router.paquetes_enviados.append(paquete)
                    
    #             else:
    #                 id_paquete = router.paquetes_enviados[-1].metadata["id"] + 1
    #                 paquete = Paquete("Hola", {"id": id_paquete, "fecha": ahora, "origen": router, "destino": router_destino} )
    #                 router.paquetes_enviados.append(paquete)

    #     except Exception as e:
    #          print(e)





                            
                    