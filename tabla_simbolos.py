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
        num_puntos = nombre.count('.')
        cont = 0
        for key in nombre.split('.'):
            if obj is None:
                return -2
            if key not in obj:
                return 0    
            else:
                if cont == 0:
                    obj = obj[key][1]
                    cont += 1
                elif num_puntos - cont > 0:
                    obj = obj[key][0]
                    cont+=1
                else:
                    obj = obj[key]
        if(obj[1] == tipo):
            obj[0] = valor
        else:
            return 1

    
    def obtener_valor_objeto(self, nombre):
        obj = self.tabla
        cont = 0
        num_puntos = nombre.count('.')
        for key in nombre.split('.'):    
            if key not in obj:
                return -1, -1
            else:
                if cont == 0:
                    obj = obj[key][1]
                    cont += 1
                elif num_puntos - cont > 0:
                    obj = obj[key][0]
                    cont+=1
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