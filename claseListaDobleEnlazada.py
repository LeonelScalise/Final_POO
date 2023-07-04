class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None
        self.anterior = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def estaVacia(self):
        return self.primero is None

    def agregarInicio(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo

    def agregarFinal(self, valor):
        nuevo_nodo = Nodo(valor)
        if self.esta_vacia():
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.ultimo
            self.ultimo.siguiente = nuevo_nodo
            self.ultimo = nuevo_nodo

    def eliminarInicio(self):
        if self.esta_vacia():
            return None
        valor_eliminado = self.primero.valor
        if self.primero is self.ultimo:
            self.primero = None
            self.ultimo = None
        else:
            self.primero = self.primero.siguiente
            self.primero.anterior = None
        return valor_eliminado

    def eliminarFinal(self):
        if self.esta_vacia():
            return None
        valor_eliminado = self.ultimo.valor
        if self.primero is self.ultimo:
            self.primero = None
            self.ultimo = None
        else:
            self.ultimo = self.ultimo.anterior
            self.ultimo.siguiente = None
        return valor_eliminado

    def imprimir_lista(self):
        nodo_actual = self.primero
        while nodo_actual:
            print(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
