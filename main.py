class Nodo:
    def __init__(self, clave):
        self.clave = clave
        self.izquierda = None
        self.derecha = None

class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, clave):
        if self.raiz is None:
            self.raiz = Nodo(clave)
        else:
            self._insertar_recursivo(self.raiz, clave)

    def _insertar_recursivo(self, nodo, clave):
        if clave < nodo.clave:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(clave)
            else:
                self._insertar_recursivo(nodo.izquierda, clave)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(clave)
            else:
                self._insertar_recursivo(nodo.derecha, clave)
    
    def imprimirArbol(self):
        self._imprimir_recursivo(self.raiz, "", True)
    
    def _imprimir_recursivo(self, nodo, prefijo, esIzquierda):
        if nodo is not None:
            print(prefijo + ("|-- " if esIzquierda else "\-- ") + str(nodo.clave))
            self._imprimir_recursivo(nodo.izquierda, prefijo + ("|   " if esIzquierda else "    "), True)
            self._imprimir_recursivo(nodo.derecha, prefijo + ("|   " if esIzquierda else "    "), False)

# Crear el árbol
arbol = Arbol()

# Permitir que el usuario ingrese números
numeros = input("Ingrese los números separados por espacios: ")
for num in map(int, numeros.split()):
    arbol.insertar(num)

# Imprimir el árbol
print("\nÁrbol binario de búsqueda:")
arbol.imprimirArbol()