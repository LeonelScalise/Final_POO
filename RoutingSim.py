from claseRouter import Router
from claseRuta import Ruta
from clasePaquete import Paquete
import sys
import threading

class RoutingSim():
    def __init__(self, duracion):
        self.duracion = duracion
        self.timer = None
    
    def crearRouter(coordenada):
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

#     def iniciarSimulacion(self):
#         router0 = self.crearRouter()
#         router1 = self.crearRouter(1)
#         router2 = self.crearRouter(2)
#         router3 = self.crearRouter(3)

#         ruta = Ruta()
#         ruta.agregarRouter(router0)
#         ruta.agregarRouter(router1)
#         ruta.agregarRouter(router2)
#         ruta.agregarRouter(router3)
        
#         print("Routers en serie\n")
#         print(router0.siguiente.nombre)

#         print(router1.anterior.nombre)
#         print(router1.siguiente.nombre)

#         print(router2.anterior.nombre)
#         print(router2.siguiente.nombre)

#         print(router3.anterior.nombre)
#         # print(router3.siguiente.nombre)



#         print("\n\nRouter del inicio y del fin de la ruta")
#         print(ruta.primero.nombre)
#         print(ruta.ultimo.nombre)

#         self.timer = threading.Timer(self.duracion, self.terminarSimulacion) # Ejecuta la función "terminarSimulación" durante los segundos que "duracion" indique 
#         self.timer.start()
    
#         threading.Timer(20, lambda : self.inhabilitarRouter(router0)).start() # A los 20 segundos de arrancar la simulación se deshabilita el router0

#         # Realizar acá las operaciones de simulación (creacion de routers, creacion de paquetes, transmision de paquetes (armado de Ruta), etc.)

#         # Todas las operaciones creemos que se deberían hacer en función de "duracion" ejemplo: threading.Timer(self.duracion * 0.1, self.crearRouter)

        
#         # Esperar hasta que la simulación esté completa


# # Crea una instancia de Simulacion con una duración de 120 segundos
# simulacion = RoutingSim(120)

# # Ejecuta la simulación
# simulacion.iniciarSimulacion()

if __name__ == '__main__':

    rutita = Ruta()
    r0=RoutingSim.crearRouter(0)
    r1=RoutingSim.crearRouter(1)
    r2=RoutingSim.crearRouter(2)
    r3=RoutingSim.crearRouter(3)
    r4=RoutingSim.crearRouter(4)

    rutita.agregarRouter(r0)
    rutita.agregarRouter(r1)
    rutita.agregarRouter(r2)
    rutita.agregarRouter(r3)
    rutita.agregarRouter(r4)

    p1 = Paquete('Leo sos un capo', {"id":1, "fecha":"fecha inventada", "origen":r4, "destino":r1} )
    p2 = Paquete('Leo sos un capo', {"id":2, "fecha":"fecha inventada", "origen":r2, "destino":r1} )

    rutita.viajePaquete(p1, r4)
    rutita.viajePaquete(p2, r2)
    # print(r2.retransmiciones_pendientes.verCola)
    # print(r3.retransmiciones_pendientes.verCola)
    # print(r4.retransmiciones_pendientes.verCola)
    print(r1.recepciones)

    