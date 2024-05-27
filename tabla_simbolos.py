import sys
class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor):
        if nombre in self.tabla:
           return -1
        else:   
            self.tabla[nombre] = [tipo, valor]

    def asignar(self, nombre, tipo, valor):
        if nombre not in self.tabla:
            return -1
        else:    
            self.tabla[nombre][1] = valor
            self.tabla[nombre][0] = tipo

    def obtener(self, nombre):
        if nombre not in self.tabla:
           return 0, 0
        else:   
            return self.tabla[nombre][1], self.tabla[nombre][0]
    
    def buscar_objeto(self, nombre, tipo, valor):
        obj = self.tabla
        cont = 0
        for key in nombre.split('.'):
            
            if key not in obj:
                print(f"[Error semántico] El objeto {key} no existe en la tabla de simbolos")
            else:
                if cont == 0:
                    obj = obj[key][1]
                    cont += 1
                else:
                    obj = obj[key]
        if(obj[1] == tipo):
            obj[0] = valor
        else:
            print(f"[Error semántico] El objeto {key} no tiene ese tipo")
    
    def obtener_valor_objeto(self, nombre):
        print("Nombre " + nombre)
        obj = self.tabla
        cont = 0
        for key in nombre.split('.'):
            print(str(obj) + "\n")
            print(key)
            if key not in obj:
                print(f"[Error semántico] El objeto {key} no existe en la tabla de simbolos")
            else:
                if cont == 0:
                    obj = obj[key][1]
                    
                    cont += 1
                else:
                    obj = obj[key]
        return obj[0], obj[1]

    def __str__(self):
        return str(self.tabla)
    
    def guardar_tabla_simbolos(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.tabla.items():
                tipo = datos[0]
                valor = datos[1]
                f.write(f"{nombre}, {tipo}, {valor}\n")