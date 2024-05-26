import ply.lex as lex
import sys

class LexerClass:
    """
    Clase que define el lexer para el lenguaje ajson
    """
    reserved = ("TR", "FL", "NULL", "let", "INT", "FLOAT", "CHARACTER", "WHILE", "BOOLEAN", "FUNCTION", "RETURN", "TYPE", "IF", "ELSE") #palabras reservadas

    tokens = ("CCOMILLAS", "CSINCOMILLAS", "CARACTER",
              "ENTERO", "DECIMAL",
              "LBRACKET", 'RBRACKET', 
              'LCORCHETE', 'RCORCHETE', 
              'LPARENT', 'RPARENT',
              'LT','LE', 'GT', 'GE','EQ', "IGUAL",
              "COMA", "PUNTOS", "SEMICOLON", 
              "SUMA", "RESTA", "MUL", "DIV", 
              "AND", "OR", "NOT",
              "PUNTO") + reserved  #tokens que se pueden usar

    def __init__(self):
        self.reserved_map = {}
        for r in self.reserved: #se añaden las palabras reservadas al mapa, tanto en mayusculas como en minusculas
            self.reserved_map[r.upper()] = r
            #self.reserved_map[r.lower()] = r.lower()
        self.lexer = lex.lex(module=self)


    t_LBRACKET = r'\{'
    t_RBRACKET = r'\}'
    t_LCORCHETE = r'\['
    t_RCORCHETE = r'\]'
    t_LT = r'<'
    t_GT = r'>'
    t_LE = r'<='
    t_GE = r'>='
    t_EQ = r'=='
    t_IGUAL = r'='
    t_COMA = r','
    t_PUNTOS = r':'
    t_PUNTO = r'\.'
    t_LPARENT = r'\('
    t_RPARENT = r'\)'
    t_SUMA = r'\+'
    t_RESTA = r'\-'
    t_MUL = r'\*'
    t_DIV = r'/'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_SEMICOLON = r';'


    #notacion ceientifica permita floats, signos infinitos, revisar los floats para caso de solo ., comparaciones.
    
    def t_DECIMAL(self, t):
        #La notacion cientifica no funciona con signos
        r'\d+[eE]-?\d+|\d+\.\d*|\d*\.\d+'
        t.value = float(t.value)
        return t    

    def t_ENTERO(self, t):
        r'0[xX][0-9A-Fa-f]+|0[bB][01]+|\d+|0[0-7]+'
        if t.value.startswith(('0x', '0X')):
            t.value = int(t.value, 16)  # Convierte a entero hexadecimal
        elif t.value.startswith(('0b', '0B')):
            t.value = int(t.value, 2)  # Convierte a entero binario
        elif t.value.startswith('0'):
            if len(t.value) > 1 and all(c in '01234567' for c in t.value[1:]):
                t.value = int(t.value, 8)      # Convierte a entero octal
            else:
                t.value = int(t.value)
            
        else:
            t.value = int(t.value)  # Convierte a entero
        return t
    
    def t_COMMENT(self, t):
        r'//.*|/\*(.|\n)*?\*/'
        pass
        

    def t_CSINCOMILLAS(self, t):
        r'[A-Za-z_][A-Za-z_0-9]*'
        t.type = self.reserved_map.get(t.value.upper(), "CSINCOMILLAS")  # Busca en el mapa de palabras reservadas
        return t
    #incluir ñ y tildes en ccomillas
    
    def t_CCOMILLAS(self, t):
        r'"[^"\n]*"'
        if(t.value=='""'):
            t.value = "'Null'"
        t.value = t.value[1:-1]  # Quita las comillas dobles
        return t

    def t_CARACTER(self, t):
        r"'[\x00-\xff]?'"
        if(t.value=="''"):
            t.value = "'Null'"
        t.value = t.value[1:-1]  # Quita las comillas simples
        
        return t

    t_ignore = ' \t' #para ignorar cualquier valor que coincida con el espacio vacío y con la tabulación
    def t_newline(self, t):
        r'\n+' #el cambio de linea puede cambiar dependiendo del fichero por lo que hay que revisar el fichero
        t.lexer.lineno += t.value.count('\n') #aumenta la posicion del lexer en tantas unidades como saltos haya

    def t_error(self, t):
        print("[Lexer] Illegal character", t)
        t.lexer.skip(1) #se salta ese caracter

    def test(self, data, path):
        self.lexer.input(data)
        output_file = open(path + ".token", "w")
        for token in self.lexer:
            output_file.write(f"{token.type} {token.value}\n")
        output_file.close()

    def test_with_file(self, path):
        with open(path) as file:
            content = file.read()
            self.test(content, path)


