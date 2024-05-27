import sys

class TablaRegistros:
    def __init__(self):
        self.registros = {}

    def agregar_registro(self, clave, registro):
        if clave in self.registros:
            return False
        else:         
            self.registros[clave] = registro


    def buscar(self, nombre):
        if nombre not in self.registros:
            return False
        else:
            return True
    
    def comprobar_estructura(self, nombre, estructura):
        if isinstance(nombre, dict):
            definido = nombre
        else:
            definido = self.registros[nombre]

        if definido.keys() != estructura.keys():
            return 0
        else:
            for clave in estructura:
                if isinstance(estructura[clave], dict) and isinstance(definido[clave], dict):
                    self.comprobar_estructura(definido[clave], estructura[clave])
                elif isinstance(estructura[clave], list) and len(estructura[clave]) == 2:
                    if estructura[clave][1] != definido[clave]:
                        return 1
                else:
                        return 0
    def guardar_tabla_registros(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.registros.items():
                f.write(f"{nombre}, {datos}\n")