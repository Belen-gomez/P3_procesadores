class TablaSimbolos:
    def __init__(self):
        self.tabla = {}

    def agregar(self, nombre, tipo, valor):
        if nombre in self.tabla:
            raise Exception(f"El simbolo {nombre} ya existe en la tabla de simbolos")
        self.tabla[nombre] = [tipo, valor]

    def asignar(self, nombre, tipo, valor):
        if nombre not in self.tabla:
            raise Exception(f"El simbolo {nombre} no existe en la tabla de simbolos")
        self.tabla[nombre][1] = valor
        self.tabla[nombre][0] = tipo

    def obtener(self, nombre):
        if nombre not in self.tabla:
            raise Exception(f"El simbolo {nombre} no existe en la tabla de simbolos")
        return self.tabla[nombre][1], self.tabla[nombre][0]

    def __str__(self):
        return str(self.tabla)
    
    def guardar_tabla_simbolos(self, archivo):
        with open(archivo, 'w') as f:
            for nombre, datos in self.tabla.items():
                tipo = datos[0]
                valor = datos[1]
                f.write(f"{nombre}, {tipo}, {valor}\n")