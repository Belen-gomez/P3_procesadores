import sys

class TablaRegistros:
    def __init__(self):
        self.registros = {}

    def agregar_registro(self, clave, registro):
        if clave in self.registros:
            print(f"Error semántico: El ajson {clave} ya existe en la tabla de registros")
            sys.exit(1)
        self.registros[clave] = registro

    def buscar(self, nombre):
        if nombre not in self.registros:
            print(f"Error semántico: El ajson {nombre} no existe en la tabla de registros")
            sys.exit(1)
        return True
    
    def comprobar_estructura(self, nombre, estructura):
        if isinstance(nombre, dict):
            definido = nombre
        else:
            definido = self.registros[nombre]

        if definido.keys() != estructura.keys():
            print("Error semántico: La estructura no coincide con la definición")
            sys.exit(1)

        for clave in estructura:
            if isinstance(estructura[clave], dict) and isinstance(definido[clave], dict):
                print("Es un diccionario")
                self.comprobar_estructura(definido[clave], estructura[clave])
            elif isinstance(estructura[clave], list) and len(estructura[clave]) == 2:
                if estructura[clave][1] != definido[clave]:
                    print("Error semántico: Los tipos de la estructura no coincide con la definición")
                    sys.exit(1)
            else:
                print("Error semántico: Estrucutura no coincide con la definición")
                sys.exit(1)
        

    
    def guardar_tabla_registros(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.registros.items():
                f.write(f"{nombre}, {datos}\n")