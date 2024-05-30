import ply.yacc as yacc
from ajson_lexer import LexerClass
import sys
from tabla_simbolos import TablaSimbolos
from tabla_registros import TablaRegistros
from tabla_funciones import TablaFunciones

class ParserClass:
    """
    Clase que define el parser para el lenguaje ajson
    """
    tokens = LexerClass.tokens #tokens que se pueden usar

    def __init__(self):
        self.parser = yacc.yacc(module=self,  debug=True)
        self.lexer = LexerClass().lexer #se crea el lexer
        self.simbolos = TablaSimbolos() #se crea la tabla de simbolos
        self.registros = TablaRegistros() #se crea la tabla de registros
        self.funciones = TablaFunciones()
        self.locales = {}

    # Define la precedencia y asociatividad de los operadores
    precedence = (
        ('right', 'NOT'),
        ('left', 'AND', 'OR'),
         ('left', 'LE', 'LT', 'GE', 'GT', 'EQ'),
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MUL', 'DIV'),
        ('left', 'USUMA', 'URESTA'),
    )
    
    def p_program(self, p):
        """
        program :  statement
                | empty
        """
    
    def p_statement(self, p):
        """
        statement : content SEMICOLON
                  | content SEMICOLON statement
                  | noSM statement
                  | noSM
        """
    
    def p_content(self, p):
        """
        content : declaration
                | assignment
                | definicion_ajson
        """
    
    def p_noSM(self, p):
        """
        noSM : function
             | condition
             | loop
        """
    
    def p_entero(self, p):
        """
        entero : ENTERO
        """
        p[0] = [p[1], "int"]

    def p_decimal(self, p):
        """
        decimal : DECIMAL
        """
        p[0] = [p[1], "float"]
    
    def p_num(self, p):
        """
        num : entero
            | decimal
        """
        p[0] = p[1]

    def p_bool(self, p):
        """
        bool : TR
             | FL
        """
        p[0] = [p[1], "boolean"]

    def p_declaration(self, p):
        """
        declaration : let id
        """ 
    
    def p_id(self, p):
        """
        id : var
           | var COMA id
           | var IGUAL expr
           | var IGUAL expr COMA id
        """
        if len(p) == 2:
            #se declara sin valor
            res = self.simbolos.agregar(p[1][0], p[1][1], None)
            if res == -1:
                print(f"[error semántico] Error en la linea {p.lineno(0)}. Variable '{p[1][0]}' ya definida")
        elif len(p) == 4:
            if p[2] == ",":
                #se declaran varias variables en una sola linea
                res = self.simbolos.agregar(p[1][0], p[1][1], None)
                if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                p[0] = p[3]
            else:
                 #solo hay una variable pero con valor
                if(p[3] == None):
                   #error en la expresion
                   pass
                elif(len(p[3]) == 2):
                   #vairable simple
                    res = self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
                    if res == -1:
                        print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                else:
                    #ajson
                    if(not p[1][1]):
                        print(f"[error semántico] Error en la linea {p.lineno(2)}: tipo de ajson no definido")
                    else:
                        p[3] = p[3][0]
                        #Esto indica que es un ajson y el tipo tiene que ser el que se ha declarado en la variables
                        err = self.registros.comprobar_estructura(p[1][1], p[3])

                        if(err == 0):
                            print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                        elif(err == 1):
                            print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                        else:
                            res = self.simbolos.agregar(p[1][0], p[1][1], p[3])
                            if res == -1:
                                print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
        else:
            if(p[3] == None):
                   #error en la expresion
                   pass
            elif(len(p[3]) == 2):
                #variable simple
                res = self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
                if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                    
            else:
                #ajson
                if(not p[1][1]):
                    print(f"[error semántico] Error en la linea {p.lineno(2)}: tipo de ajson no definido")
                else:
                    p[3] = p[3][0]
                    #Esto indica que es un ajson y el tipo tiene que ser el que se ha declarado en la variables
                    err = self.registros.comprobar_estructura(p[1][1], p[3])

                    if(err == 0):
                            print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                    elif(err == 1):
                        print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                    else:
                        res = self.simbolos.agregar(p[1][0], p[1][1], p[3])
                        if res == -1:
                            print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
            p[0] = p[5]
        
    def p_var(self, p):
        """
        var : CSINCOMILLAS
            | CSINCOMILLAS PUNTOS tipo
        """
        if len(p) == 2:
            p[0] =  [p[1], None]
        else:
            #el tipo puede ser un ajson ya declarado o un tipo simple
            err = self.registros.buscar(p[3])
            if err == False:
                if p[3] not in ["int", "float", "character", "boolean"]:
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipo no válido")
            p[0] = [p[1], p[3]]

    def p_tipo_ajson(self, p):
        """
        tipo_ajson : CSINCOMILLAS
        """
        if (self.registros.buscar(p[1])):
            p[0] = p[1]
        
    def p_tipo(self, p):
        """
        tipo : INT
             | FLOAT
             | CHARACTER
             | BOOLEAN
             | tipo_ajson
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : var IGUAL expr
                     | punto_valor IGUAL expr
                     | corchete IGUAL expr
        """
        if(p[3] is None):
            #error en la expresion
            pass
        elif(len(p[3]) == 2):
            #la expresión es un tipo simple 
            if(len(p[1]) == 2):
                if p[1][0] not in self.locales.keys():
                        res = self.simbolos.asignar(p[1][0], p[3][1], p[3][0])
                        if res == -1:
                            print(f"[error semántico] Error en la linea {p.lineno(1)}. Variable '{p[1]}' no definida" )
                else:
                    #esto solo se hace cuando es un argumento de la funcion
                    if self.locales[p[1][0]] == 'int':
                        p[0] = [0, 'int']
                    elif self.locales[p[1][0]] == 'float':
                        p[0] = [0.0, 'float']
                    elif self.locales[p[1][0]] == 'character':
                        p[0] = ['a', 'character']
                    elif self.locales[p[1][0]] == 'boolean':
                        p[0] = ['tr', 'boolean']
                    else:
                        p[0] = [None, self.locales[p[1][0]]]                    
            else:
                err = self.simbolos.buscar_objeto(p[1], p[3][1], p[3][0])
                if err == 0:
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: El objeto {p[3][1]} no existe en la tabla de simbolos")
                elif err == 1:
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipo de la variable no válido")
                elif err == -2:
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Error en la asignación, el objeto no ha sido inicializado")
        else:
            #la expresión es un ajson. Hay que comprobar que la estrutura es correcta
            p[3] = p[3][0]
            valor, tipo = self.simbolos.obtener(p[1][0])   
            err = self.registros.comprobar_estructura(tipo, p[3])  
            if(err == 0):
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
            elif(err == 1):
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
            else:      
                res = self.simbolos.asignar(p[1][0], tipo, p[3])
                if res == -1:
                        print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' no definida")

    def p_variable(self, p):
        """
        variable : CSINCOMILLAS
        """
        if p[1] not in self.locales.keys():
                valor, tipo = self.simbolos.obtener(p[1])
                if tipo==0:
                    print(f"[error semántico] Error en la linea {p.lineno(1)}. Variable '{p[1]}' no definida" )
                else:
                    p[0] = [valor, tipo]
        else:
            #esto solo se hace cuando es un argumento de la funcion
            if self.locales[p[1]] == 'int':
                p[0] = [0, 'int']
            elif self.locales[p[1]] == 'float':
                p[0] = [0.0, 'float']
            elif self.locales[p[1]] == 'character':
                p[0] = ['a', 'character']
            elif self.locales[p[1]] == 'boolean':
                p[0] = ['tr', 'boolean']
            else:
                p[0] = [None, self.locales[p[1]]]
                
       
    
    def p_cadena(self, p):
        """
        cadena : CARACTER
        """
        p[0] = [p[1], "character"]
    
    def p_parentesis(self, p):
        """
        parentesis : LPARENT expr RPARENT
        """
        p[0] = p[2]

    def p_signos(self, p):
        """
        signos : SUMA expr %prec USUMA
               | RESTA expr %prec URESTA
        """
        if(p[2][1] == "int" or p[2][1] == "float"):
            if p[1] == "+":
                p[0] = [p[2][0], p[2][1]]
            else:
                p[0] = [-p[2][0], p[2][1]]
        else:
            print(f"[error semántico] Error en la liena {p.lineno(1)}: Tipos no compatibles")
    
    def p_expr(self, p):
        """
        expr : operacion
              | num
              | bool
              | NULL  
              | variable
              | signos
              | cadena
              | ajson
              | parentesis
              | pc
              | functioncall
        """
        p[0] = p[1]

    def p_operacion(self, p):
        """
        operacion : aritmetica
                  | binaria
                  | comparation
        """
        p[0] = p[1]

    def p_aritmetica(self, p):
        """
        aritmetica : expr SUMA expr
                   | expr RESTA expr
                   | expr MUL expr %prec MUL
                   | expr DIV expr %prec DIV
        """
        if p[1]is None or p[3] is None:
            pass
        elif p[1][1] is None or p[3][1] is None:
            #error en la expresion
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
        elif p[1][0] is None or p[3][0] is None:
            #error en la expresion
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable sin valor. No se puede utilizar en una operacion")
        
        elif p[2] == "+":
            if p[1][1] == "float" or p[3][1] == "float":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii + p[3][0], "float"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii + p[1][0], "float"]
                else:
                    p[0] = [p[1][0] + p[3][0], "float"]
                
            elif p[1][1] == "int" or p[3][1] == "int":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii + p[3][0], "int"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii + p[1][0], "int"]
                else:
                    p[0] = [p[1][0] + p[3][0], "int"]

            else:
                resultado_ascii = ord(p[1][0]) + ord(p[3][0])
                p[0] = [chr(resultado_ascii %256), "character"]


        elif p[2] == "-":
            if p[1][1] == "float" or p[3][1] == "float":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii - p[3][0], "float"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii - p[1][0], "float"]
                else:
                    p[0] = [p[1][0] - p[3][0], "float"]
                
            elif p[1][1] == "int" or p[3][1] == "int":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii - p[3][0], "int"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii - p[1][0], "int"]
                else:
                    p[0] = [p[1][0] - p[3][0], "int"]

            else:
                resultado_ascii = ord(p[1][0]) - ord(p[3][0])
                p[0] = [chr(resultado_ascii %256), "character"]

        elif p[2]=="*":
            if p[1][1] == "float" or p[3][1] == "float":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii * p[3][0], "float"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii * p[1][0], "float"]
                else:
                    p[0] = [p[1][0] * p[3][0], "float"]
                
            elif p[1][1] == "int" or p[3][1] == "int":
                if p[1][1] == "character":
                     resultado_ascii = ord(p[1][0])
                     p[0] = [resultado_ascii * p[3][0], "int"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    p[0] = [resultado_ascii * p[1][0], "int"]
                else:
                    p[0] = [p[1][0] * p[3][0], "int"]

            else:
                print(f"[error semántico] Error en la liena {p.lineno(2)}: No se permite la multiplicación entre caracteres")

        else:
            if p[3][0] == 0:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Division por cero")

            elif p[1][1] == "float" or p[3][1] == "float":
                if p[1][1] == "character":
                    resultado_ascii = ord(p[1][0])
                    p[0] = [resultado_ascii / p[3][0], "float"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    if resultado_ascii == 0:
                        print(f"[error semántico] Error en la línea {p.lineno(2)}: Division por cero")
                    else:
                        p[0] = [p[1][0]/resultado_ascii, "float"] 
                else:
                    p[0] = [p[1][0] / p[3][0], "float"]
                           
            elif p[1][1] == "int" or p[3][1] == "int":
                if p[1][1] == "character":
                    resultado_ascii = ord(p[1][0])
                    p[0] = [resultado_ascii // p[3][0], "int"]
                elif p[3][1] == "character":
                    resultado_ascii = ord(p[3][0])
                    if resultado_ascii == 0:
                        print(f"[error semántico] Error en la línea {p.lineno(2)}: Division por cero")
                    else:
                        p[0] = [p[1][0]//resultado_ascii, "int"]        
                else:
                    p[0] = [p[1][0] // p[3][0], "int"]
            else:
                print(f"[error semántico] Error en la liena {p.lineno(2)}: No se permite la división entre caracteres")



    def p_binaria(self, p):
        """
        binaria : expr AND expr
                | expr OR expr
                | NOT expr
        """
        
        if p[2] == "&&":
            if(p[1] is None or p[3] is None):
                #error en la expresion
                pass
            elif p[1][1] is None or p[3][1] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            elif p[1][0] is None or p[3][0] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable sin valor. No se puede utilizar en una operacion")
            elif p[1][1] == "boolean" and p[3][1] == "boolean":
                if (p[1][0] == "fl" or p[3][0] == "fl"):
                    p[0] = ["fl", "boolean"]
                else:
                    p[0] = ["tr", "boolean"]
            else:
                print(f"[error semántico] Error en la líena {p.lineno(2)}: Tipos no compatibles")
            
        elif p[2] == "||":
            if(p[1] is None or p[3] is None):
                #error en la expresion
                pass
            elif p[1][1] is None or p[3][1] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            elif p[1][0] is None or p[3][0] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable sin valor. No se puede utilizar en una operacion")
            elif p[1][1] == "boolean" and p[3][1] == "boolean":
                if (p[1][0] == "tr" or p[3][0] == "tr"):
                    p[0] = ["tr", "boolean"]
                else:
                    p[0] = ["fl", "boolean"]
            else:
                print(f"[error semántico] Error en la líena {p.lineno(2)}: Tipos no compatibles")
             
        else:
            if(p[2] is None):
                #error en la expresion
                pass
            elif p[2][1] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            elif p[2][0] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable sin valor. No se puede utilizar en una operacion")
            elif p[2][1] == "boolean":
                if p[2][0] == "tr":
                    p[0] = ["fl", "boolean"]
                else:
                    p[0] = ["tr", "boolean"]

            else:
                print(f"[error semántico] Error en la líena {p.lineno(1)}: Tipos no compatibles")
           
     
    def p_comparation(self, p):
        """
        comparation : expr LE expr
                    | expr LT expr
                    | expr GE expr
                    | expr GT expr
                    | expr EQ expr
        """
        if p[1]is None or p[3] is None:
            #error en la expresion
            pass
        elif p[1][1] is None or p[3][1] is None:
                #error en la expresion
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
        elif p[1][0] is None or p[3][0] is None:
            #error en la expresion
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable sin valor. No se puede utilizar en una operacion")

        elif p[2] == "==":
            if p[1][1] == "boolean" and p[3][1] == "boolean":
                if (p[1][0] == p[3][0]):
                    p[0] = ["tr", "boolean"]
                else:
                    p[0] = ["fl", "boolean"]

            elif p[1][1] == "boolean" or p[3][1] == "boolean":
                print(f"[error semántcio] Error en la línea {p.lineno(2)}: Tipos no compatibles")

            else:
                if p[1][1] == "character":
                    resultado1= ord(p[1][0])
                else:
                    resultado1 = p[1][0]
                    
                if p[3][1] == "character":
                    resultado3 = ord(p[3][0])
                else:
                    resultado3 = p[3][0]
                if (resultado1 == resultado3):
                    p[0] = ["tr", "boolean"]
                else:
                    p[0] = ["fl", "boolean"]
            
        else:
            if p[1][1] == "boolean" or p[3][1] == "boolean":
                print(f"[error semántcio] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            else:
                if p[1][1] == "character":
                    resultado1= ord(p[1][0])
                else:
                    resultado1 = p[1][0]
                        
                if p[3][1] == "character":
                    resultado3 = ord(p[3][0])
                else:
                    resultado3 = p[3][0]
                
                if p[2] == "<":
                    if (resultado1 < resultado3):
                        p[0] = ["tr", "boolean"]
                    else:
                        p[0] = ["fl", "boolean"]
                    
                elif p[2] == ">":
                    if (resultado1 > resultado3):
                        p[0] = ["tr", "boolean"]
                    else:
                        p[0] = ["fl", "boolean"]
                elif p[2] == "<=":
                    if (resultado1 <= resultado3):
                        p[0] = ["tr", "boolean"]
                    else:
                        p[0] = ["fl", "boolean"]
                else:
                    if (resultado1 >= resultado3):
                        p[0] = ["tr", "boolean"]
                    else:
                        p[0] = ["fl", "boolean"]
                    
            

    def p_definicion_ajson(self, p):
        """
        definicion_ajson : TYPE CSINCOMILLAS IGUAL ajson_t
        """
        if p[4] is not None:
            #se guarda en la tabla de registros
            err = self.registros.agregar_registro(p[2], p[4])
            if (err == -1):
                print(f"[error semántico] Error en la línea {p.lineno(2)}. El ajson '{p[2]}' ya existe")
            elif (err ==-2):
                print(f"[error semántico] Error en la línea {p.lineno(2)}. Tipos del ajson no válidos")

    def p_ajson_t(self, p):
        """
        ajson_t : LBRACKET object_t RBRACKET
        """
        p[0] = p[2]


    def p_object_t(self, p):
        """
        object_t : pair_t COMA object_t
                 | pair_t COMA
                 | pair_t
        """
       
        if len(p) == 2 or len(p) == 3:
            p[0] = p[1]
        else:
            claves_comunes = set(p[1].keys()) & set(p[3].keys())
            if claves_comunes:
                #no puede haber claves repetidas
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Claves repetidas en el ajson")
            else:
                p[0] = {**p[1], **p[3]}

    def p_pair_t(self, p):
        """
        pair_t : clave PUNTOS tipo
                | clave PUNTOS ajson_t
        """

        p[0] = {p[1]: p[3]}
    
    def p_clave(self, p):
        """
        clave : CCOMILLAS
                | CSINCOMILLAS
        """
        p[0] = p[1]

    def p_ajson(self, p):
        """
        ajson : LBRACKET object RBRACKET
        """
        p[0] = [p[2]]


    def p_object(self, p):
        """
        object : pair COMA object
               | pair COMA
               | pair
        """
        if len(p) == 2 or len(p) == 3:
            p[0] = p[1]
        else:
            p[0] = {**p[1], **p[3]}

    def p_pair(self, p):
        """
        pair : clave PUNTOS expr
        """
        p[0] = {p[1]: p[3]}

    def p_punto_valor(self, p):
        """
        punto_valor : punto1
                    | punto2
                    | punto_corchete
        """
        p[0] = p[1]

    def p_pc(self, p):
        """
        pc : punto_valor
            | corchete
        """
        tipo = 0;
        if len(self.locales) != 0:
            #obtener el valor de una clave si es un argumento de la funcion
            tipo = self.registros.obtener_valor_objeto(p[1], self.locales)
        if tipo == -1 or len(self.locales) == 0:
            #si no es un argumento tiene que estar en la tabla de simbolos
            valor, tipo =  self.simbolos.obtener_valor_objeto(p[1])
            if tipo == -1:
                print(f"[error semántico] Error en la línea {p.lineno(1)}: No se puede acceder a las claves del objeto")
            else:
                p[0] = [valor, tipo]
        else:
            p[0] = [None, tipo]
            
    def p_punto1(self, p):
        """
        punto1 : CSINCOMILLAS PUNTO CSINCOMILLAS    
        """
        p[0] = p[1] + "." + p[3]
    
    def p_punto2(self, p):
        """
        punto2 : CSINCOMILLAS PUNTO punto_valor
        """
        p[0] = p[1] + "." + p[3]
    
    def p_punto_corchete(self, p):
        """
        punto_corchete : CSINCOMILLAS PUNTO corchete
        """
        p[0] = p[1] + "." + p[3]

    def p_corchete(self, p):    
        """
        corchete : CSINCOMILLAS LCORCHETE CCOMILLAS RCORCHETE recur_corchete
        """
        if(p[5]):
            p[0] = p[1] + "." + p[3] + "." + p[5]
        else:
            p[0] = p[1] + "." + p[3]
        
    def p_recur_corchete(self, p):
        """
        recur_corchete : LCORCHETE CCOMILLAS RCORCHETE recur_corchete
                       | empty   
                       | PUNTO CSINCOMILLAS
                       | PUNTO punto_valor                   
        """
        if len(p) == 5:
            if(p[4]):
                p[0] = p[2] + "." + p[4]
            else:
                p[0] = p[2]
        elif len(p) == 3:
            p[0] = p[2]
        else:
            p[0] = None
    
    def p_condition(self, p):
        """
        condition : IF LPARENT expr RPARENT LBRACKET statement RBRACKET
                  | IF LPARENT expr RPARENT LBRACKET statement RBRACKET ELSE LBRACKET statement RBRACKET
        """
        if(p[3]):
            if(p[3][1] != "boolean"):
                #solo se acpetan tipos booleanos
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La condición no es de tipo booleano")
        else:
            #error en la expresion
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable de la condición no definida correctamente")

    def p_loop(self, p):
        """
        loop : WHILE LPARENT expr RPARENT LBRACKET statement RBRACKET
        """
        if(p[3]):
            if(p[3][1] != "boolean"):
                #solo se acpetan tipos booleanos
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La condición del bucle no es de tipo booleano")
        else:
            #error en la expresion
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable de la condición del bucle no definida correctamente")
    
    def p_function(self, p):
        """
        function : function_no_args
                 | function_args
        """
        
    def p_function_args(self, p):
        """
        function_args : FUNCTION CSINCOMILLAS LPARENT arg_list RPARENT PUNTOS tipo LBRACKET statement RETURN expr SEMICOLON RBRACKET
                        | FUNCTION CSINCOMILLAS LPARENT arg_list RPARENT PUNTOS tipo LBRACKET RETURN expr SEMICOLON RBRACKET
        """
        res = True
        if (len(p) == 14):
            #hay statements
            if(p[11] == None):
                #error en la expresion
                pass
            elif len(p[11]) == 2: 
                #el tipo de retorno es una variable simple o un ajson ya declarado
                if (p[7] != p[11][1]):
                    res = False
                    print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")
            else:
                p[11] = p[11][0]
                #si el tipo de retorno es un ajson no declarado, se devuelve directamente el diccionario, hay que comprobar la estructura
                err = self.registros.comprobar_estructura(p[7], p[11])

                if(err == 0):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                    res = False
                elif(err == 1):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                    res = False   
        else:
            if(p[10] == None):
                #error en la expresion
                pass
            elif len(p[10]) == 2:
                #el tipo de retorno es una variable simple o un ajson ya declarado
                if (p[7] != p[10][1]):
                    res = False
                    print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")
            else:
                p[10] = p[10][0]
                 #si el tipo de retorno es un ajson no declarado, se devuelve directamente el diccionario, hay que comprobar la estructura
                err = self.registros.comprobar_estructura(p[7], p[10])

                if(err == 0):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                    res = False
                elif(err == 1):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                    res = False 
            
        if res != False:
            err = self.funciones.agregar(p[2], p[4], p[7])
            if err==False:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La función '{p[2]}' ya existe")

    def p_function_no_args(self, p):
        """
        function_no_args : FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET statement RETURN expr SEMICOLON RBRACKET
                            | FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET RETURN expr SEMICOLON RBRACKET
        """
        res = True
        if (len(p) == 13):
            if (p[13] == None):
                pass
            elif len(p[10]) == 2:
                if (p[6] != p[10][1]):
                    res = False
                    print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")
            else:
                p[10] = p[10][0]
                err = self.registros.comprobar_estructura(p[6], p[10])

                if(err == 0):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                    res = False
                elif(err == 1):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                    res = False   
        else:
            if (p[9] == None):
                pass
            elif len(p[9]) == 2:
                if (p[6] != p[9][1]):
                    res = False
                    print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")
            else:
                p[9] = p[9][0]
                err = self.registros.comprobar_estructura(p[6], p[9])

                if(err == 0):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: La estructura no coincide con la definición")
                    res = False
                elif(err == 1):
                    print(f"[error semántico] Error en la línea {p.lineno(2)}: Los tipos de la estructura no coincide con la definición")
                    res = False  
        if res != False:
            err = self.funciones.agregar(p[2], None, p[6])
            if err == False:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La función '{p[2]}' ya existe")

    def p_arg_list(self, p):
        """
        arg_list : CSINCOMILLAS PUNTOS tipo
                 | CSINCOMILLAS PUNTOS tipo COMA arg_list
        """
        #se añaden los argumentos al diccionario de locales
        if (len(p) ==4):
            p[0] = [p[3]]
            self.locales[p[1]] = p[3]
        else:
            p[0] = [p[3]] + p[5]
            self.locales[p[1]] = p[3]
        
    def p_functioncall(self, p):
        """
        functioncall : CSINCOMILLAS LPARENT RPARENT 
                     | CSINCOMILLAS LPARENT argumentos RPARENT
        """
        if len(p) == 4:
            tipo = self.funciones.buscar(p[1])
        else:
            tipo = self.funciones.comprobar_argumentos(p[1], p[3])
        if tipo == -1:
            print(f"[error semántico] Error en la línea {p.lineno(1)}: La función '{p[1]}' no está definida")
        elif tipo == -2:
            print(f"[error semántico] Error en la línea {p.lineno(1)}: Los argumentos de la función '{p[1]}' no coinciden")
        else:
            p[0] = [None, tipo]

    def p_argumentos(self, p):
        """
        argumentos : expr
                   | expr COMA argumentos
        """
        if(len(p) == 2):
            p[0] = [p[1][1]]
        else:
            p[0] = [p[1][1]] + p[3]

    def p_empty(self, p):
        """
        empty : 
        """
        pass
    
    def p_error(self, p):
        if not p:
            print("[parser] Parser error. Error al final del archivo")
        else:
            print(f"[parser] Error sintáctico en la línea {p.lineno}: token inesperado '{p.value}'")

    

    def test(self, data):
        self.parser.parse(data)

    def test_with_file(self, path):
        file = open(path)
        content = file.read()
        self.test(content)
        output_file = path + ".symbols"
        self.simbolos.guardar_tabla_simbolos(output_file)
        output_file2 = path + ".register"
        self.registros.guardar_tabla_registros(output_file2)
        output_file3 = path + ".function"
        self.funciones.guardar_tabla_funciones(output_file3)