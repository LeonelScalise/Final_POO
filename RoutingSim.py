from claseRouter import Router
from claseRuta import Ruta
from clasePaquete import Paquete
import sys
import threading

class RoutingSim():
    def __init__(self, duracion):
        self.duracion = duracion
        self.timer = None
    
    def crearRouter(self, coordenada):
        nombre = "router_" + str(coordenada)
        estado = "AGREGADO"
        newRouter = Router(nombre, estado)
        newRouter.estado = "ACTIVO"

        return newRouter
    
    def inhabilitarRouter(self, router):
        router.estado = "INACTIVO"

    def habilitarRouter(self, router):
        router.estado = "ACTIVO"

    def terminarSimulacion(self):
        print("Simulación finalizada")
        # Salir del programa
        sys.exit()

    def iniciarSimulacion(self):
        router0 = self.crearRouter(0)
        router1 = self.crearRouter(1)
        router2 = self.crearRouter(2)
        router3 = self.crearRouter(3)
        router4 = self.crearRouter(4)

        ruta = Ruta()
        
        ruta.agregarRouter(router0)
        ruta.agregarRouter(router1)
        ruta.agregarRouter(router2)
        ruta.agregarRouter(router3)
        ruta.agregarRouter(router4)
        # ruta.iniciarLatenciaRouters()

        #self.inhabilitarRouter(router1)
        #self.inhabilitarRouter(router3)
        #self.inhabilitarRouter(router2)

        


        p1 = router0.crearPaquete("Hola", router1)
        p2 = router1.crearPaquete("tas?", router4)
        p3 = router3.crearPaquete("CAPO", router2)


        #threading.Timer(5, lambda : ruta.averiaAleatoria()).start()
        threading.Timer(1, lambda : self.inhabilitarRouter(router2)).start()
        threading.Timer(5, lambda : ruta.viajePaquete(p3, router3)).start()
        threading.Timer(6, lambda : ruta.viajePaquete(p2, router1)).start()
        # threading.Timer(7, lambda : ruta.viajePaquete(p3, router3)).start()
        # threading.Timer(13, lambda : ruta.viajePaquete(p3, router0)).start()
        threading.Timer(15, lambda : self.habilitarRouter(router2)).start()


        # threading.Timer(5, lambda : ruta.viajePaquete(p2, router4)).start()
        # threading.Timer(7, lambda : ruta.viajePaquete(p3, router1)).start()
        #threading.Timer(20, lambda : ruta.averiaAleatoria()).start()

        
        
        #threading.Timer(10, lambda : self.inhabilitarRouter(router2)).start() # A los 20 segundos de arrancar la simulación se deshabilita el router0

        self.timer = threading.Timer(self.duracion, self.terminarSimulacion) # Ejecuta la función "terminarSimulación" durante los segundos que "duracion" indique 
        self.timer.start()
    
        

        # Realizar acá las operaciones de simulación (creacion de routers, creacion de paquetes, transmision de paquetes (armado de Ruta), etc.)

        # Todas las operaciones creemos que se deberían hacer en función de "duracion" ejemplo: threading.Timer(self.duracion * 0.1, self.crearRouter)

        
        # Esperar hasta que la simulación esté completa


# Crea una instancia de Simulacion con una duración de 30 segundos
simulacion = RoutingSim(35)

# Ejecuta la simulación
simulacion.iniciarSimulacion()

# if __name__ == '__main__':

    # rutita = Ruta()
    # r0=RoutingSim.crearRouter(0)
    # r1=RoutingSim.crearRouter(1)
    # r2=RoutingSim.crearRouter(2)
    # r3=RoutingSim.crearRouter(3)
    # r4=RoutingSim.crearRouter(4)

    # rutita.agregarRouter(r0)
    # rutita.agregarRouter(r1)
    # rutita.agregarRouter(r2)
    # rutita.agregarRouter(r3)
    # rutita.agregarRouter(r4)

    # p1 = Paquete('Leo sos un capo', {"id":1, "fecha":"fecha inventada", "origen":r4, "destino":r1} )
    # p2 = Paquete('Leo sos un capo', {"id":2, "fecha":"fecha inventada", "origen":r2, "destino":r1} )

    # p1 = r1.crearPaquete("Hola crack", r4)
    # p2 = r4.crearPaquete("Hola crack 2", r2)

    # rutita.viajePaquete(p1, r1)
    # rutita.viajePaquete(p2, r4)
    
    # rutita.crearPaqueteAleatorio(r0)
    # rutita.crearPaqueteAleatorio(r3)
    # rutita.crearPaqueteAleatorio(r0)
    # rutita.crearPaqueteAleatorio(r3)
    

    # print(r2.retransmiciones_pendientes.verCola)
    # print(r3.retransmiciones_pendientes.verCola)
    # print(r4.retransmiciones_pendientes.verCola)
    # print(r4.recepciones[-1].metadata)
    # print(r2.recepciones[-1].metadata)

    