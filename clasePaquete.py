class Paquete():

    def __init__(self, mensaje, metadata = {"id":"", "fecha":"", "origen":None, "destino":None}):
        self.mensaje = mensaje
        self.metadata = metadata
    
    