class Ruta:
    def __init__(self):
        self.primero = None
        self.ultimo = None

    def agregarRouter(self, router):
        if self.primero is None:
            self.primero = router
            self.ultimo = router
        else:
            router.anterior = self.ultimo
            self.ultimo.siguiente = router
            self.ultimo = router

    # def imprimirRuta(self):
    #     router_actual = self.primero
    #     while router_actual:
    #         print(f"Router: {router_actual.nombre}")
    #         router_actual = router_actual.siguiente
