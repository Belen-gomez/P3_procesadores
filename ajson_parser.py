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

    # Define la precedencia y asociatividad de los operadores
    precedence = (
        ('right', 'NOT'),
        ('left', 'AND', 'OR'),
         ('left', 'LE', 'LT', 'GE', 'GT', 'EQ'),
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MUL', 'DIV'),
        ('left', 'USUMA', 'URESTA'),
    )

    
    # El valor de laas variables no es importante cuenado haya control de flujo. 
    # En el control de flujo, la solucion mas facil es que el tipo de la variable sea el ultimo, la mas dificil que se guarden varias variables o algo asi
    # Tabla de registros para registrar tipos complejos, tener la plantilla de como son los objetos que el desarrollador crea y ver si cuando se cree uno sigue esa plantilla. Cuando se degina un tipo con la plabra type se mete en la tabal de registros. Caundo se declara un objeto se usa la tabla de registros para comprobar que sigue la estructura
    # Ejemplo: tyoe point = {int: x, int: y}
    #           type line = {a: Point, b: Point}
    #           este es el caso mas facil. En la tabla de registros hay tipos y campos 
    # Caso mas dificil: type line = {a: {x:int}, b: {y:int}}
    # Funciones: se comprueba que la expresion en return se corresponde con el tipo de salida. Tambien se correspone que los argumentos coincidan en tipo con los registrados. Las funciones por lo tanto van en la tabla de registros
    # Puede haber funciones con el mismo nombre pero distintos tipos o numeros de argumentos.
    # Las funciones se pueden crear en una tabla de registros (es una clase) o crear una tabla de funciones
    # En los tipos ir del menos restrictivo al mas restrictivo
    # ¿La tabla de simbolos es una clase?
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
            res = self.simbolos.agregar(p[1][0], p[1][1], None)
            if res == -1:
                print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
        elif len(p) == 4:
            if p[2] == ",":
                res = self.simbolos.agregar(p[1][0], p[1][1], None)
                if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                p[0] = p[3]
            else:
                if(p[3] == None):
                   pass
                elif(len(p[3]) == 2):
                    res = self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
                    if res == -1:
                        print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                else:
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
                   pass
            elif(len(p[3]) == 2):
                res = self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
                if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' ya definida")
                    
            else:
                if(not p[1][1]):
                    print(f"[error semántico] Error en la linea {p.lineno(2)}: tipo de ajson no definido")
                else:
                    p[3] = p[3][0]
                    #Esto indica que es un ajson y el tipo tiene que ser el que se ha declarado en la variables
                    self.registros.comprobar_estructura(p[1][1], p[3])
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
            pass
        elif(len(p[3]) == 2):
            if(len(p[1]) == 2):
                res = self.simbolos.asignar(p[1][0], p[3][1], p[3][0])
                if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' no definida")
            else:
                self.simbolos.buscar_objeto(p[1], p[3][1], p[3][0])
        else:
            p[3] = p[3][0]
            valor, tipo = self.simbolos.obtener(p[1][0])   
            self.registros.comprobar_estructura(tipo, p[3])        
            res = self.simbolos.asignar(p[1][0], tipo, p[3])
            if res == -1:
                    print(f"[error semántico] Error en la linea {p.lineno(2)}. Variable '{p[1][0]}' no definida")

    def p_variable(self, p):
        """
        variable : CSINCOMILLAS
        """
        valor, tipo = self.simbolos.obtener(p[1])
        if tipo==0:
           print(f"[error semántico] Error en la linea {p.lineno(1)}. Variable '{p[1]}' no definida" )
        else:
            p[0] = [valor, tipo]
    
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
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
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
                pass
            elif p[1][1] is None or p[3][1] is None:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            elif p[1][1] == "boolean" and p[3][1] == "boolean":
                if (p[1][0] == "fl" or p[3][0] == "fl"):
                    p[0] = ["fl", "boolean"]
                else:
                    p[0] = ["tr", "boolean"]
            else:
                print(f"[error semántico] Error en la líena {p.lineno(2)}: Tipos no compatibles")
            
        elif p[2] == "||":
            if(p[1] is None or p[3] is None):
                pass
            elif p[1][1] is None or p[3][1] is None:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
            elif p[1][1] == "boolean" and p[3][1] == "boolean":
                if (p[1][0] == "tr" or p[3][0] == "tr"):
                    p[0] = ["tr", "boolean"]
                else:
                    p[0] = ["fl", "boolean"]
            else:
                print(f"[error semántico] Error en la líena {p.lineno(2)}: Tipos no compatibles")
             
        else:
            if(p[2] is None):
                pass
            elif p[2][1] is None:
                print(f"[error semántico] Error en la línea {p.lineno(2)}: Tipos no compatibles")
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
            pass

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
        
        err = self.registros.agregar_registro(p[2], p[4])
        if (err == False):
            print(f"[error semántico] Error en la línea {p.lineno(2)}. El ajson '{p[2]}' ya existe")

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
        valor, tipo =  self.simbolos.obtener_valor_objeto(p[1])
        p[0] = [valor, tipo]
            
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
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La condición no es de tipo booleano")
        else:
            print(f"[error semántico] Error en la línea {p.lineno(2)}: Variable de la condición no definida correctamente")

    def p_loop(self, p):
        """
        loop : WHILE LPARENT expr RPARENT LBRACKET statement RBRACKET
        """
        if(p[3]):
            if(p[3][1] != "boolean"):
                print(f"[error semántico] Error en la línea {p.lineno(2)}: La condición del bucle no es de tipo booleano")
        else:
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
        if (len(p) == 14):
            if (p[7] != p[11][1]):
                print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")

        else:
            if (p[7] != p[10][1]):
                print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")

        err = self.funciones.agregar(p[2], p[4], p[7])
        if err==False:
            print(f"[error semántico] Error en la línea {p.lineno(2)}: La función '{p[2]}' ya existe")

    def p_function_no_args(self, p):
        """
        function_no_args : FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET statement RETURN expr SEMICOLON RBRACKET
                            | FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET RETURN expr SEMICOLON RBRACKET
        """
        if (len(p) == 13):
            if (p[6] != p[10][1]):
                 print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")
 
        else:
            if (p[6] != p[9][1]):
                 print(f"[error semántico] Error en la líena {p.lineno(2)}: El tipo de retorno de la funcion '{p[2]}' no coincide con el tipo de la expresión")


        err = self.funciones.agregar(p[2], None, p[6])
        if err == False:
            print(f"[error semántico] Error en la línea {p.lineno(2)}: La función '{p[2]}' ya existe")

    def p_arg_list(self, p):
        """
        arg_list : CSINCOMILLAS PUNTOS tipo
                 | CSINCOMILLAS PUNTOS tipo COMA arg_list
        """
        if (len(p) ==4):
            p[0] = [p[3]]
        else:
            p[0] = [p[3]] + p[5]
    
    def p_functioncall(self, p):
        """
        functioncall : CSINCOMILLAS LPARENT RPARENT 
                     | CSINCOMILLAS LPARENT argumentos RPARENT
        """
        if len(p) == 4:
            tipo = self.funciones.buscar(p[1])
        else:
            tipo = self.funciones.comprobar_argumentos(p[1], p[3])
        if tipo == False:
            print(f"[error semántico] Error en la línea {p.lineno(1)}: La función '{p[1]}' no está definida")
        elif tipo == 1:
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
            print(f"[parser] Error sintáctico en la línea {p.lineno}, columna {p.lexpos}: token inesperado '{p.value}'")

    

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