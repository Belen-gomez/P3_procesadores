import sys

class TablaFunciones:
    def __init__(self):
        self.funciones = []
    
    def agregar(self, nombre, args, tipo):
        for funcion in self.funciones:
            if nombre == funcion[0] and args == funcion[1]:
                return False
        self.funciones.append([nombre, args, tipo])
        
    
    def guardar_tabla_funciones(self, archivo):
        with open(archivo, 'w') as f:
            for funcion in self.funciones:
                f.write(f"{funcion[0]}, {funcion[1]}, {funcion[2]}\n")
    
    def buscar(self, nombre):
        for funcion in self.funciones:
            if nombre == funcion[0]:
                return funcion[2]
        return False
        
        
    
    def comprobar_argumentos(self, nombre, argumentos):
        valor = -1
        for funcion in self.funciones:
            if nombre == funcion[0]:
                if argumentos == funcion[1]:
                    return funcion[2]
                else:
                    valor = -2
        return valor