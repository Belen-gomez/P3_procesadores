import sys

class TablaFunciones:
    def __init__(self):
        self.funciones = []
    
    def agregar(self, nombre, args, tipo):
        for funcion in self.funciones:
            if nombre == funcion[0] and args == funcion[1]:
                print(f"Error semántico: La función {nombre} ya existe en la tabla de funciones")
                sys.exit(1)
        
        self.funciones.append([nombre, args, tipo])
        
    
    def guardar_tabla_funciones(self, archivo):
        with open(archivo, 'w') as f:
            for funcion in self.funciones:
                f.write(f"{funcion[0]}, {funcion[1]}, {funcion[2]}\n")
    
    def buscar(self, nombre):
        for funcion in self.funciones:
            if nombre == funcion[0]:
                return funcion[2]
        print(f"Error semántico: La función {nombre} no existe en la tabla de funciones")
        sys.exit(1)
    
    def comprobar_argumentos(self, nombre, argumentos):
        for funcion in self.funciones:
            if nombre == funcion[0]:
                if argumentos != funcion[1]:
                    print(f"Error semántico: Los argumentos de la función {nombre} no coinciden")
                    sys.exit(1)
                return funcion[2]
        print(f"Error semántico: La función {nombre} no existe en la tabla de funciones")
        sys.exit(1)
    