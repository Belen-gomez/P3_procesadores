import sys
class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor):
        if nombre in self.tabla:
           print(f"Error semántico: El simbolo {nombre} ya existe en la tabla de simbolos")
           
        self.tabla[nombre] = [tipo, valor]

    def asignar(self, nombre, tipo, valor):
        if nombre not in self.tabla:
            print(f"Error semántico: El simbolo {nombre} no existe en la tabla de simbolos")
            
        self.tabla[nombre][1] = valor
        self.tabla[nombre][0] = tipo

    def obtener(self, nombre):
        if nombre not in self.tabla:
           print(f"Error semántico: El simbolo {nombre} no existe en la tabla de simbolos")
           
        return self.tabla[nombre][1], self.tabla[nombre][0]
    
    def buscar_objeto(self, nombre, tipo, valor):
        obj = self.tabla
        cont = 0
        for key in nombre.split('.'):
            
            if key not in obj:
                print(f"Error semántico: El objeto {key} no existe en la tabla de simbolos")
                sys.exit(1)
            if cont == 0:
                obj = obj[key][1]
                cont += 1
            else:
                obj = obj[key]
            print("Objeto: ", obj, "\n")
        if(obj[1] == tipo):
            obj[0] = valor
        else:
            print(f"Error semántico: El objeto {key} no tiene ese tipo")
            sys.exit(1)
    
    def obtener_valor_objeto(self, nombre):
        obj = self.tabla
        cont = 0
        for key in nombre.split('.'):
            
            if key not in obj:
                print(f"Error semántico: El objeto {key} no existe en la tabla de simbolos")
                sys.exit(1)
            if cont == 0:
                obj = obj[key][1]
                cont += 1
            else:
                obj = obj[key]
            print("Objeto: ", obj, "\n")
        return obj[0], obj[1]

    def __str__(self):
        return str(self.tabla)
    
    def guardar_tabla_simbolos(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.tabla.items():
                tipo = datos[0]
                valor = datos[1]
                f.write(f"{nombre}, {tipo}, {valor}\n")