import sys

class TablaRegistros:
    def __init__(self):
        self.registros = {}

    def agregar_registro(self, clave, registro, agregar = True):
        if clave in self.registros:
            return -1
        
        else:  
            tipos = ["int", 'float', 'character', 'boolean']
            for key in registro:
                
                if (isinstance(registro[key],dict)):
                    self.agregar_registro(" ",registro[key], False)
    
                elif registro[key] not in self.registros and registro[key] not in tipos:  
                    return -2
            if agregar:
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
            if nombre not in self.registros:
                return 0
            definido = self.registros[nombre]
        if definido.keys() != estructura.keys():
            return 0
        else:
            for clave in estructura:                
                if isinstance(estructura[clave], list) and len(estructura[clave]) == 2:
                    if isinstance(estructura[clave][0], dict):
                         #ajson con tipo
                         valor= self.comprobar_estructura(definido[clave], estructura[clave][0])
                         if valor !=2:
                            return valor
                    else:
                        #Es un valor normal, no es un ajson
                        if estructura[clave][1] != definido[clave]:
                            return 1
                elif isinstance(estructura[clave], list) and len(estructura[clave]) == 1:
                    #ajson sin tipo
                    if isinstance(estructura[clave][0], dict):
                        valor =  self.comprobar_estructura(definido[clave], estructura[clave][0])
                        if valor !=2:
                                return valor

                else:
                        return 0
        return 2
    def guardar_tabla_registros(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.registros.items():
                f.write(f"{nombre}, {datos}\n")