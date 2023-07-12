from claseRouter import Router
from claseRuta import Ruta
from clasePaquete import Paquete
import datetime
import sys
import threading
import random
import time

class RoutingSim():
    def __init__(self, duracion):
        self.duracion = duracion
        self.timer = None
        self.sim_terminada = False
    
    def crearRouter(self, coordenada):
        nombre = "router_" + str(coordenada)
        newRouter = Router(nombre)
        newRouter.registrarEvento()
        newRouter.estado = "ACTIVO"
        newRouter.registrarEvento()

        return newRouter
    
    def inhabilitarRouter(self, router):
        router.estado = "INACTIVO"
        router.registrarEvento()


    def habilitarRouter(self, router):
        router.estado = "ACTIVO"
        router.registrarEvento()

    def terminarSimulacion(self, ruta):
        
        for router in ruta.routers:
            router.ordenarPaquetes()
        
        ruta.crearArchivos()
        ruta.tasas()

        self.sim_terminada = True

        print("\nSimulación finalizada")
   
    
    def limpiarCSV(self):
        with open('system_log.csv', mode='w', newline=''):
            pass

    def iniciarSimulacion(self): 
        self.limpiarCSV()

        time_ref = time.time()
        router1 = self.crearRouter(1)
        router2 = self.crearRouter(2)
        router3 = self.crearRouter(3)
        router4 = self.crearRouter(4)
        router5 = self.crearRouter(5)

        ruta = Ruta()
        
        ruta.agregarRouter(router1)
        ruta.agregarRouter(router2)
        ruta.agregarRouter(router3)
        ruta.agregarRouter(router4)
        ruta.agregarRouter(router5)


    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba el funcionamiento de la transmision y retransmision en ambos sentidos

        # p1 = router1.crearPaquete("Sali del 1", router5)
        # p2 = router5.crearPaquete("Sali del 5", router1)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(4, lambda : ruta.viajePaquete(p2, time_ref)).start()        

    #------------------------------------------------------------------------------------------------------------------

      # Este ejemplo prueba el funcionamiento del bypass con destino inactivo

        # self.inhabilitarRouter(router3)
        # self.inhabilitarRouter(router4)
        # self.inhabilitarRouter(router5)

        # p1 = router1.crearPaquete("Sali del 1", router5)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()

        # threading.Timer(4, lambda : self.habilitarRouter(router5)).start()
    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba el funcionamiento del bypass

        # self.inhabilitarRouter(router2)
        # self.inhabilitarRouter(router4)

        # p1 = router1.crearPaquete("Sali del 1", router5)
        # p2 = router5.crearPaquete("Sali del 5", router1)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(4, lambda : ruta.viajePaquete(p2, time_ref)).start()

    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba el funcionamiento de avería aleatoria --> se pueden probar varios conceptos.

        # p1 = router1.crearPaquete("Sali del 1", router5)
        # p2 = router5.crearPaquete("Sali del 5", router1)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(4, lambda : ruta.viajePaquete(p2, time_ref)).start()

        # threading.Timer(1, lambda : ruta.averiaAleatoria(time_ref)).start()

    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba el funcionamiento de la nube (cuando un router debe recibir INACTIVO)

        # p1 = router1.crearPaquete("Sali del 1", router4)

        
        # threading.Timer(1, lambda : self.inhabilitarRouter(router4)).start()

        # threading.Timer(5, lambda : ruta.viajePaquete(p1, time_ref)).start()

        # threading.Timer(10, lambda : self.habilitarRouter(router4)).start()

    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba el funcionamiento de la averia durante el procesamiento de un paquete --> Consideración: se debe utilizar una latencia de 5 segundos para observarlo
        
        # p1 = router1.crearPaquete("Sali del 1", router5)
        # p2 = router2.crearPaquete("Sali del 3", router3)
        

        # threading.Timer(2, lambda : ruta.viajePaquete(p2, time_ref)).start()
        # threading.Timer(3, lambda : ruta.viajePaquete(p1, time_ref)).start()

        # threading.Timer(4, lambda : router2.averia(time_ref)).start()


    #------------------------------------------------------------------------------------------------------------------

        # Este ejemplo prueba si dos paquetes llegan al mismo tiempo a un router (debería elegir uno y mandarlo y esperar la latencia para el otro)

        # p1 = router1.crearPaquete("Sali del 1", router5)
        # p2 = router5.crearPaquete("Sali del 5", router1)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(2, lambda : ruta.viajePaquete(p2, time_ref)).start()

    #------------------------------------------------------------------------------------------------------------------
         
        # Este ejemplo prueba el funcionamiento de la prioridad entre envios de un mismo router

        # p1 = router1.crearPaquete("Sali del 1.1", router5)
        # p2 = router1.crearPaquete("Sali del 1.2", router5)
        # p3 = router1.crearPaquete("Sali del 1.3", router5)
        
        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(2.01, lambda : ruta.viajePaquete(p2, time_ref)).start()
        # threading.Timer(2.02, lambda : ruta.viajePaquete(p3, time_ref)).start()


    #------------------------------------------------------------------------------------------------------------------
        # Este ejemplo prueba el funcionamiento de la prioridad de las retransmisiones contra los envios (a veces no funciona el print pero anda igual --> se cumple la prioridad)
        
        # p1 = router2.crearPaquete("Sali del 2.1", router3)
        # p2 = router2.crearPaquete("Sali del 2.2", router3)
        # p3 = router1.crearPaquete("Sali del 1", router3)

        # threading.Timer(2, lambda : ruta.viajePaquete(p1, time_ref)).start()
        # threading.Timer(2.01, lambda : ruta.viajePaquete(p3, time_ref)).start()
        # threading.Timer(2.06, lambda : ruta.viajePaquete(p2, time_ref)).start()
        

    #------------------------------------------------------------------------------------------------------------------

        self.timer = threading.Timer(self.duracion, lambda: self.terminarSimulacion(ruta)) # Cuando pasan "duración" segundos se ejecuta terminarSimulacion 
        self.timer.start()
        
        # Esperar hasta que la simulación esté completa
        while not self.sim_terminada:
            pass

        ruta.graficoBarras() # Esta función se ejecuta aca porque hay problemas con matplotlib y los Threads
        sys.exit()


# Crea una instancia de Simulacion con una duración de 20 segundos
simulacion = RoutingSim(20)

# Ejecuta la simulación
simulacion.iniciarSimulacion()

    