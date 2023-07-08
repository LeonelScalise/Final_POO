from datetime import datetime
from clasePaquete import Paquete
import random
import time
import threading
from claseRouter import Router
from popularNube import nube
import matplotlib.pyplot as plt
import numpy as np

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

        try:
            if router.estado != "ACTIVO":
                raise Exception(f"{router.nombre} no puede crear un paquete. Está inhabilitado.")
            else:
                inicio = True
                contador0 = 0
                while not router.habilitado:
                    if contador0 == 0:
                        print(f'Esperando a que se habilite el {router.nombre} de origen.')
                    contador0 += 1
                threading.Thread(target=router.latencia).start()
                print(router.nombre)

                if coordenada_destino > coordenada_origen: #aca falta chequear si el router directamente adyacente al primero es el destino --> si esta inactivo lo baypassea
                    router_actual = router.siguiente
                    if router_actual != paquete.metadata["destino"]:
                        while router_actual.estado != 'ACTIVO':
                            if router_actual != paquete.metadata["destino"]:
                                print(f"{router_actual.nombre} baypaseado")
                                router_actual = router_actual.siguiente
                            else:
                                self.enviar_a_nube(paquete, router_actual)
                                conta = 0
                                while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                    if conta == 0:
                                        print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                    conta += 1
                                c = 0
                                while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                    if c == 0:
                                        print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                    c += 1

                            
                                router_actual.recepciones.append(paquete)
                                
                                nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                                print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')
                                
                                inicio = False 
                            #Lo mando a la nube
                                return 
                            
                        
                        while inicio:
                            
                            if router_actual != paquete.metadata["destino"]:
                                router_actual.retransmiciones_pendientes.agregar(paquete)
                                # print('Con cola agregada\n\n')
                                # router_actual.retransmiciones_pendientes.verCola()
                                router_a_enviar = getattr(router_actual, "siguiente")
                                
                                # Chequea si el router_a_enviar está habilitado
                                while router_a_enviar.estado != 'ACTIVO' and router_a_enviar != paquete.metadata["destino"]:
                                    print(f"{router_a_enviar.nombre} baypaseado")
                                    router_a_enviar = getattr(router_a_enviar, "siguiente")
                                    if router_a_enviar == paquete.metadata["destino"] and router_a_enviar.estado != 'ACTIVO':
                                        pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                
                                router_a_enviar.retransmiciones_pendientes.agregar(paquete)
                                
                                #Considerar que restransmiciones sea un contador y no una lista --> Porque no necesitamos manipular los objetos de esa lista, sino solo contarlos para estadisticas
                                contador = 0
                                


                                # c6 = 0
                                # while router_a_enviar.retransmiciones_pendientes.primero.valor != paquete:
                                #     if c6 == 0:
                                #         print(f'El paquete {paquete.mensaje} esta esperando que se habilite el {router_a_enviar.nombre}')
                                #     c6 += 1
                                
                                
                                while not router_actual.habilitado:
                                    if contador == 0:
                                        print(f'Esperando a que se habilite el {router_actual.nombre}.')
                                    contador += 1
                                threading.Thread(target=router_actual.latencia).start()
                                
                                print(router_actual.nombre)
                                
                                router_actual.retransmiciones.append(paquete)
                                
                                
                                router_actual.retransmiciones_pendientes.borrar()
                                
                                # router_actual.retransmiciones_pendientes.verCola()
                                router_actual = router_a_enviar
                            else:
                                if router_actual.estado != 'ACTIVO':
                                    self.enviar_a_nube(paquete, router_actual)
                                    conta = 0
                                    while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                        if conta == 0:
                                            print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                        conta += 1
                                    c = 0
                                    while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                        if c == 0:
                                            print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                        c += 1

                                    router_actual.recepciones.append(paquete)
                                    
                                    if len(router_actual.recepciones) > 2:
                                        print(router_actual.recepciones[0].mensaje + router_actual.recepciones[1].mensaje + router_actual.recepciones[2].mensaje)
                                    
                                    nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                                    print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')
                                    
                                    inicio = False
                                else:
                                    router_actual.recepciones.append(paquete)
                                    print(router_actual.nombre)
                                    inicio = False
                    else:
                        if router_actual.estado != 'ACTIVO':
                            self.enviar_a_nube(paquete, router_actual)
                            conta = 0
                            while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                if conta == 0:
                                    print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                conta += 1
                            c = 0
                            while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                if c == 0:
                                    print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                c += 1

                            router_actual.recepciones.append(paquete)

                            nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                            print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')

                        else:
                            router_actual.recepciones.append(paquete)
                            print(router_actual.nombre)

                else:
                    router_actual = router.anterior
                    if router_actual != paquete.metadata["destino"]:
                        while router_actual.estado != 'ACTIVO':
                            if router_actual != paquete.metadata["destino"]:
                                print(f"{router_actual.nombre} baypaseado")
                                router_actual = router_actual.anterior
                            else:
                                self.enviar_a_nube(paquete, router_actual)
                                conta = 0
                                while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                    if conta == 0:
                                        print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                    conta += 1
                                c = 0
                                while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                    if c == 0:
                                        print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                    c += 1

                            
                                router_actual.recepciones.append(paquete)
                                
                                nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                                print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')
                                
                                inicio = False 
                            #Lo mando a la nube
                                return 
                        
                        while inicio:
                        
                            if router_actual != paquete.metadata["destino"]:
                                router_actual.retransmiciones_pendientes.agregar(paquete)
                                # print('Con cola agregada\n\n')
                                # router_actual.retransmiciones_pendientes.verCola()
                                router_a_enviar = getattr(router_actual, "anterior")
                                
                                #chequearia un if de si el router_a_enviar esta inhabilitado o averiado o reseteandose
                                while router_a_enviar.estado != 'ACTIVO' and router_a_enviar != paquete.metadata["destino"]:
                                    print(f"{router_a_enviar.nombre} baypaseado")
                                    router_a_enviar = getattr(router_a_enviar, "anterior")
                                    if router_a_enviar == paquete.metadata["destino"] and router_a_enviar.estado != 'ACTIVO':
                                        
                                        pass #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                
                                router_a_enviar.retransmiciones_pendientes.agregar(paquete)
                                
                                contador = 0
                                
                                # c6 = 0
                                # while router_a_enviar.retransmiciones_pendientes.primero.valor != paquete:
                                #     if c6 == 0:
                                #         print(f'El paquete {paquete.mensaje} esta esperando que se habilite el {router_a_enviar.nombre}')
                                #     c6 += 1
                                # print('sali del while del c6')
                                while not router_actual.habilitado:
                                    if contador == 0:
                                        print(f'esperando a que se habilite el {router_actual.nombre}.')
                                    contador += 1              
                                threading.Thread(target=router_actual.latencia).start()

                                print(router_actual.nombre)

                                router_actual.retransmiciones.append(paquete)
                                router_actual.retransmiciones_pendientes.borrar()
                                # router_actual.retransmiciones_pendientes.verCola()
                                # # print('Con cola borrada\n\n')
                                # router_actual.retransmiciones_pendientes.verCola()

                                router_actual = router_a_enviar
                            
                            else:
                                if router_actual.estado != 'ACTIVO':
                                    self.enviar_a_nube(paquete, router_actual)
                                    conta = 0
                                    while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                        if conta == 0:
                                            print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                        conta += 1
                                    c = 0
                                    while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                        if c == 0:
                                            print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                        c += 1

                                
                                    router_actual.recepciones.append(paquete)
                                    
                                    nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                                    print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')
                                    
                                    inicio = False 
                                else:
                                    router_actual.recepciones.append(paquete)
                                    print(router_actual.nombre)
                                    inicio = False
                    
                    else:
                        if router_actual.estado != 'ACTIVO':
                            self.enviar_a_nube(paquete, router_actual)
                            conta = 0
                            while router_actual.estado != 'ACTIVO': #mandar a la nube que chequea el estado del nodo destino constantemente hasta que se habilite
                                if conta == 0:
                                    print(f'La nube esta esperando a que se active el {router_actual.nombre}.')
                                conta += 1
                            c = 0
                            while paquete != nube.paquetes_pendientes[router_actual.nombre][0]:
                                if c == 0:
                                    print(f"Todavia no es el turno del paquete {paquete.mensaje}")
                                c += 1

                            router_actual.recepciones.append(paquete)

                            nube.paquetes_pendientes[router_actual.nombre].remove(nube.paquetes_pendientes[router_actual.nombre][0])
                            print(f'Se envio el paquete {paquete.mensaje} desde la nube al {router_actual.nombre}')

                        else:
                            router_actual.recepciones.append(paquete)
                            print(router_actual.nombre)

                print(router_actual.recepciones[-1].metadata)

        except Exception as e:
             print(e)
    

    def averiaAleatoria(self):
        pos_aleatoria = random.randint(0,len(self.routers)-1)
        router = self.routers[pos_aleatoria]
        print(router.nombre)
        print(router.estado)
        router.estado = "EN_RESET"
        router.registrarEvento()
        print(router.nombre)
        print(router.estado)
        tiempo_aleatorio = random.randint(5, 10)

        print(tiempo_aleatorio)

        time.sleep(tiempo_aleatorio)

        router.estado = "ACTIVO"
        router.registrarEvento()
        print(router.nombre)
        print(router.estado)


    def enviar_a_nube(self, paquete, router):
       if router.nombre not in nube.paquetes_pendientes: 
            nube.paquetes_pendientes[router.nombre] = []
        
       nube.paquetes_pendientes[router.nombre].append(paquete)
    

    #Este metodo permite crear archivos .txt de cada router, en los cuales se puede observar los paquetes ordenados por cada router emisorl
    def crearArchivos(self):
        origen_anterior = ''
        c=0
        for router in self.routers:
            if len(router.recepciones)!= 0:
                nombre_archivo = f"Final_POO/{router.nombre}.txt"  # Nombre del archivo basado en el router que recibió los paquetes
                with open(nombre_archivo, "w") as archivo:
                    for paquete in router.recepciones:
                        origen = paquete.metadata['origen'].nombre
                        mensaje = paquete.mensaje
                        if origen == origen_anterior:
                            archivo.write(f"{mensaje}\n")
                        else:
                            if c==0:
                                archivo.write(f"Origen: {origen}\n")
                                c+=1
                            else:
                                archivo.write(f"\nOrigen: {origen}\n")

                            archivo.write(f"{mensaje}\n")
                            origen_anterior = origen
    
    #Este metodo permite observar un grafico de barras donde se encuentran la cantidad de paquetes enviados y recibidos de cada router
    def graficoBarras(self):
        enviados=[]
        recibidos=[]
        for router in self.routers:
            enviados.append(len(router.paquetes_enviados))
            recibidos.append(len(router.recepciones))
        
        x_axis = np.arange(len(self.routers))
        
        plt.bar(x_axis -0.2, enviados, width=0.4, label = 'Enviados')
        plt.bar(x_axis +0.2, recibidos, width=0.4, label = 'Recibidos')

        # Xticks

        plt.xticks(x_axis, self.routers)

        # Agregado de leyenda

        plt.legend()


        plt.show()
    
    #Este metodo permite visualizar por terminal las tasas de retransmisiones y recepciones de paquetes
    def tasas(self):
        cantidad_total_de_retransmisiones = sum(len(router.retransmiciones) for router in self.routers)
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
                    round(len(router.retransmiciones) / cantidad_total_de_retransmisiones, 2))
                    for router in self.routers]

            for fila in data:
                print(f'{fila[0]:>10s} {fila[1]:>10.2f} {fila[2]:>10.2f}')

        elif cantidad_total_de_retransmisiones == 0 and cantidad_total_de_recepciones != 0:
            print(header_string)
            print(separator_string)

            data = [(router.nombre.upper(),
                    round(len(router.recepciones) / cantidad_total_de_recepciones, 2))
                    for router in self.routers]

            for fila in data:
                print(f'{fila[0]:>10s} {fila[1]:>10.2f}')

            print("\nNo hay paquetes reenviados.\n")

        else:
            print("\nNo se han enviado paquetes.\n")
        

if __name__ == '__main__':
    ruta=Ruta()
    r1=Router('ruter1')
    r2=Router('ruter2')
    r3=Router('ruter3')
    ruta.agregarRouter(r1)
    ruta.agregarRouter(r2)
    ruta.agregarRouter(r3)
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r1.paquetes_enviados.append('pedo')
    r2.paquetes_enviados.append('caca')
    r2.paquetes_enviados.append('caca')
    r2.paquetes_enviados.append('caca')
    r2.paquetes_enviados.append('caca')
    r2.recepciones.append('pis')
    r2.recepciones.append('pis')
    r2.recepciones.append('pis')
    r2.recepciones.append('pis')
    r2.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')
    r1.recepciones.append('pis')

    ruta.graficoBarras()
    ruta.tasas()

                            
                    