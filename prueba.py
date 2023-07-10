import heapq


class Router():
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = 'AGREGADO'
        self.retransmisiones_pendientes = []  # Ahora es una cola de prioridad
        # Resto del código...

    def agregar_retransmision_pendiente(self, paquete):
        # Agrega un paquete a la cola de prioridad
        heapq.heappush(self.retransmisiones_pendientes, (paquete.prioridad, paquete))

    def obtener_siguiente_retransmision(self):
        # Obtiene el paquete con mayor prioridad
        return heapq.heappop(self.retransmisiones_pendientes)[1]  # [1] para obtener el paquete, no la prioridad
    


    