from clasePaquete import Paquete
class Nodo():
    def __init__(self, valor):
        self.valor = valor
        self.siguiente = None

class Cola():
    def __init__(self):
        self.primero = None
    
    def agregar(self, valor):

        if self.esVacia():
            self.primero = Nodo(valor)
        
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = Nodo(valor)
    
    def borrar(self):
        if self.esVacia():
            print('La cola está vacía')
        else:
            self.primero = self.primero.siguiente
    
    def esVacia(self):
        return not self.primero
    
    def verCola(self):
        if self.esVacia():
            print("La cola está vacía")
        else:
            actual = self.primero
            while actual is not None:
                print(actual.valor.mensaje)
                actual = actual.siguiente

if __name__ == '__main__':
    c=Cola()
    p1=Paquete('caca','a')
    p2=Paquete('pis','b')
    c.agregar(p1)
    c.agregar(p2)
    c.borrar()
    c.borrar()
    print(c.esVacia())