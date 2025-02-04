class Nodo:
    def _init_(self, n):
        self.n = n
        self.izquierda = None
        self.derecha = None

class Arbol:
    def _init_(self):
        self.raiz = None

    def vacio(self):
        return self.raiz is None

    def buscarNodo(self, n):
        return self._buscarNodo_recursivo(self.raiz, n)

    def _buscarNodo_recursivo(self, actual, n):
        if actual is None or actual.n == n:
            return actual
        if n < actual.n:
            return self._buscarNodo_recursivo(actual.izquierda, n)
        return self._buscarNodo_recursivo(actual.derecha, n)

    def insertar(self, n):
        nuevo_nodo = Nodo(n)
        if self.raiz is None:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo)

    def _insertar_recursivo(self, actual, nuevo_nodo):
        if nuevo_nodo.n < actual.n:
            if actual.izquierda is None:
                actual.izquierda = nuevo_nodo
            else:
                self._insertar_recursivo(actual.izquierda, nuevo_nodo)
        else:
            if actual.derecha is None:
                actual.derecha = nuevo_nodo
            else:
                self._insertar_recursivo(actual.derecha, nuevo_nodo)

    def imprimir_arbol(self):
        self._imprimir_recursivo(self.raiz)
        print()

    def _imprimir_recursivo(self, actual):
        if actual is not None:
            self._imprimir_recursivo(actual.izquierda)
            print(actual.n, end=' ')
            self._imprimir_recursivo(actual.derecha)

if _name_ == "_main_":
    arbol = Arbol()
    while True:
        print("\n1. Insertar nodo")
        print("2. Buscar nodo")
        print("3. Imprimir árbol")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            n = input("Ingrese el n del nodo: ")
            arbol.insertar(n)
        elif opcion == "2":
            n = input("Ingrese el n a buscar: ")
            nodo = arbol.buscarNodo(n)
            if nodo:
                print(f"Nodo encontrado: {nodo.n}")
            else:
                print("Nodo no encontrado.")
        elif opcion == "3":
            print("Árbol en orden:")
            arbol.imprimir_arbol()
        elif opcion == "4":
            break
        else:
            print("Opción no válida. Intente de nuevo.")