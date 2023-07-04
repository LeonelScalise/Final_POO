from clasePaquete import Paquete
from claseRouter import Router
from claseRuta import Ruta
import sys
import threading

class RoutingSim():
    def __init__(self, duracion):
        self.duracion = duracion
        self.timer = None

    def terminarSimulacion(self):
        print("Simulación finalizada")
        # Salir del programa
        sys.exit()

    def iniciarSimulacion(self):
        self.timer = threading.Timer(self.duracion, self.terminarSimulacion) # Ejecuta la función "terminarSimulación" durante los segundos que "duracion" indique 
        self.timer.start()

        # Realizar acá las operaciones de simulación (creacion de routers, creacion de paquetes, transmision de paquetes (armado de Ruta), etc.)

        # Todas las operaciones creemos que se deberían hacer en función de "duracion" ejemplo: threading.Timer(self.duracion * 0.1, self.crearRouter)

        
        # Esperar hasta que la simulación esté completa


# Crea una instancia de Simulacion con una duración de 120 segundos
simulacion = RoutingSim(120)

# Ejecuta la simulación
simulacion.iniciarSimulacion()
