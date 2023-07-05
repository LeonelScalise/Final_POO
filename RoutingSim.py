from claseRouter import Router
from claseRuta import Ruta
import sys
import threading

class RoutingSim():
    def __init__(self, duracion):
        self.duracion = duracion
        self.timer = None
    
    def crearRouter(self, coordenada = 0):
        if coordenada == 0:
            nombre = "router_0"
        else:
            nombre = "router_" + str(coordenada)

        estado = "AGREGADO"
        newRouter = Router(nombre, estado)
        newRouter.estado = "ACTIVO"

        return newRouter
    
    def inhabilitarRouter(self, router):
        router.estado == "INACTIVO"


    def terminarSimulacion(self):
        print("Simulación finalizada")
        # Salir del programa
        sys.exit()

    def iniciarSimulacion(self):
        router0 = self.crearRouter()
        router1 = self.crearRouter(1)
        router2 = self.crearRouter(2)
        router3 = self.crearRouter(3)

        ruta = Ruta()
        ruta.agregarRouter(router0)
        ruta.agregarRouter(router1)
        ruta.agregarRouter(router2)
        ruta.agregarRouter(router3)
        
        print("Routers en serie\n")
        print(router0.siguiente.nombre)

        print(router1.anterior.nombre)
        print(router1.siguiente.nombre)

        print(router2.anterior.nombre)
        print(router2.siguiente.nombre)

        print(router3.anterior.nombre)
        # print(router3.siguiente.nombre)



        print("\n\nRouter del inicio y del fin de la ruta")
        print(ruta.primero.nombre)
        print(ruta.ultimo.nombre)

        self.timer = threading.Timer(self.duracion, self.terminarSimulacion) # Ejecuta la función "terminarSimulación" durante los segundos que "duracion" indique 
        self.timer.start()
    
        threading.Timer(20, lambda : self.inhabilitarRouter(router0)).start() # A los 20 segundos de arrancar la simulación se deshabilita el router0

        # Realizar acá las operaciones de simulación (creacion de routers, creacion de paquetes, transmision de paquetes (armado de Ruta), etc.)

        # Todas las operaciones creemos que se deberían hacer en función de "duracion" ejemplo: threading.Timer(self.duracion * 0.1, self.crearRouter)

        
        # Esperar hasta que la simulación esté completa


# Crea una instancia de Simulacion con una duración de 120 segundos
simulacion = RoutingSim(120)

# Ejecuta la simulación
simulacion.iniciarSimulacion()
