import ply.yacc as yacc
from ajson_lexer import LexerClass
import sys
from tabla_simbolos import TablaSimbolos

class ParserClass:
    """
    Clase que define el parser para el lenguaje ajson
    """
    tokens = LexerClass.tokens #tokens que se pueden usar

    def __init__(self):
        self.parser = yacc.yacc(module=self,  debug=True)
        self.lexer = LexerClass().lexer #se crea el lexer
        self.simbolos = TablaSimbolos() #se crea la tabla de simbolos

    # Define la precedencia y asociatividad de los operadores
    precedence = (
        ('left', 'LE', 'LT', 'GE', 'GT', 'EQ'),
        ('right', 'NOT'),
        ('left', 'AND', 'OR'),
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
        p[0] = [p[1], "bool"]

    def p_declaration(self, p):
        """
        declaration : LET id
        """ 

    def p_id(self, p):
        """
        id : var
           | var COMA id
           | var IGUAL expr
           | var IGUAL expr COMA id
        """
        if len(p) == 2:
            self.simbolos.agregar(p[1][0], p[1][1], None)
        elif len(p) == 4:
            if p[2] == ",":
                self.simbolos.agregar(p[1][0], p[1][1], None)
                p[0] = p[3]
            else:
                print(p[0], p[1], p[3])
                self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
        else:
            print(p[0], p[1], p[3])
            self.simbolos.agregar(p[1][0], p[3][1], p[3][0])
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

    def p_tipo(self, p):
        """
        tipo : INT
             | FLOAT
             | CHARACTER
             | BOOLEAN
             | CSINCOMILLAS
        """
        p[0] = p[1]

    def p_assignment(self, p):
        """
        assignment : var IGUAL expr
        """
        self.simbolos.asignar(p[1][0], p[3][1], p[3][0])

    def p_variable(self, p):
        """
        variable : CSINCOMILLAS
        """
        valor, tipo = self.simbolos.obtener(p[1])
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
        if p[1] == "+":
            p[0] = [p[2][0], p[2][1]]
        else:
            p[0] = [-p[2][0], p[2][1]]
    
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
              | punto
              | corchete
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
        if p[2] == "+":
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
                print(p[0])

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
                resultado_ascii = ord(p[1][0]) * ord(p[3][0])
                p[0] = [chr(resultado_ascii %256), "character"]
        else:
            if p[1][1] == "float" or p[3][1] == "float":
                
                if p[3][0] == 0:
                    print("[parser] Parser error: Division por cero")
                    sys.exit(1)
                p[0] = [p[1][0] / p[3][0], "float"]
                
            else:
                if p[3][0] == 0:
                    print("[parser] Parser error: Division por cero")
                    sys.exit(1)
                else:
                    p[0] = [p[1][0] / p[3][0], "int"]


    def p_binaria(self, p):
        """
        binaria : expr AND expr
                | expr OR expr
                | NOT expr
        """
        if p[2] == "&&":
            if p[1][1] == "bool" and p[3][1] == "bool":
                p[0] = [p[1][0] and p[3][0], "bool"]
            else:
                print("[parser] Parser error: Tipos no compatibles")
                sys.exit(1)
        elif p[2] == "||":
            if p[1][1] == "bool" and p[3][1] == "bool":
                p[0] = [p[1][0] or p[3][0], "bool"]
            else:
                print("[parser] Parser error: Tipos no compatibles")
                sys.exit(1)
        else:
            if p[2][1] == "bool":
                p[0] = [not p[2][0], "bool"]
            else:
                print("[parser] Parser error: Tipos no compatibles")
                sys.exit(1)
     
    def p_comparation(self, p):
        """
        comparation : expr LE expr
                    | expr LT expr
                    | expr GE expr
                    | expr GT expr
                    | expr EQ expr
        """
        if p[2] == "==":
            if p[1][1] == "bool" and p[3][1] == "bool":
                p[0] = [p[1][0] == p[3][0], "bool"]

            elif p[1][1] == "bool" or p[3][1] == "bool":
                print("[parser] Parser error: Tipos no compatibles")
                sys.exit(1)
            
            else:
                if p[1][1] == "character":
                    resultado1= ord(p[1][0])
                else:
                    resultado1 = p[1][0]
                    
                if p[3][1] == "character":
                    resultado3 = ord(p[3][0])
                else:
                    resultado3 = p[3][0]
                
                p[0] = [resultado1 == resultado3, "bool"]
            
        else:
            if p[1][1] == "bool" or p[3][1] == "bool":
                print("[parser] Parser error: Tipos no compatibles")
                sys.exit(1)
            
            if p[1][1] == "character":
                resultado1= ord(p[1][0])
            else:
                resultado1 = p[1][0]
                    
            if p[3][1] == "character":
                resultado3 = ord(p[3][0])
            else:
                resultado3 = p[3][0]
            
            if p[2] == "<":
                p[0] = [resultado1 < resultado3, "bool"]
            elif p[2] == ">":
                p[0] = [resultado1 > resultado3, "bool"]
            elif p[2] == "<=":
                p[0] = [resultado1 <= resultado3, "bool"]
            else:
                p[0] = [resultado1 >= resultado3, "bool"]
                    
            

    def p_definicion_ajson(self, p):
        """
        definicion_ajson : TYPE CSINCOMILLAS IGUAL ajson_t
        """

    def p_ajson_t(self, p):
        """
        ajson_t : LBRACKET object_t RBRACKET
        """
    def p_object_t(self, p):
        """
        object_t : pair_t COMA object_t
                 | pair_t COMA
                 | pair_t
        """
    def p_pair_t(self, p):
        """
        pair_t : clave PUNTOS tipo
                | clave PUNTOS ajson_t
        """
    
    def p_clave(self, p):
        """
        clave : CCOMILLAS
                | CSINCOMILLAS
        """
    
    
    def p_ajson(self, p):
        """
        ajson : LBRACKET object RBRACKET
        """
    
    def p_object(self, p):
        """
        object : pair COMA object
               | pair COMA
               | pair
        """
    
    def p_pair(self, p):
        """
        pair : clave PUNTOS expr
        """
    def p_punto(self, p):
        """
        punto : CSINCOMILLAS PUNTO CSINCOMILLAS
                | CSINCOMILLAS PUNTO punto
                | CSINCOMILLAS PUNTO corchete
        """
    def p_corchete(self, p):    
        """
        corchete : CSINCOMILLAS LCORCHETE CCOMILLAS RCORCHETE recur_corchete
        """
    
    def p_recur_corchete(self, p):
        """
        recur_corchete : LCORCHETE CCOMILLAS RCORCHETE recur_corchete
                       | empty   
                       | PUNTO CSINCOMILLAS
                       | PUNTO punto                   
        """
    
    def p_condition(self, p):
        """
        condition : IF LPARENT expr RPARENT LBRACKET statement RBRACKET
                  | IF LPARENT expr RPARENT LBRACKET statement RBRACKET ELSE LBRACKET statement RBRACKET
        """
    
    def p_loop(self, p):
        """
        loop : WHILE LPARENT expr RPARENT LBRACKET statement RBRACKET
        """
    
    def p_function(self, p):
        """
        function : FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET statement RETURN expr SEMICOLON RBRACKET
                 | FUNCTION CSINCOMILLAS LPARENT RPARENT PUNTOS tipo LBRACKET RETURN expr SEMICOLON RBRACKET
                 | FUNCTION CSINCOMILLAS LPARENT arg_list RPARENT PUNTOS tipo LBRACKET statement RETURN expr SEMICOLON RBRACKET
                 | FUNCTION CSINCOMILLAS LPARENT arg_list RPARENT PUNTOS tipo LBRACKET RETURN expr SEMICOLON RBRACKET
        """
    def p_arg_list(self, p):
        """
        arg_list : CSINCOMILLAS PUNTOS tipo
                 | CSINCOMILLAS PUNTOS tipo COMA arg_list
        """
    
    def p_functioncall(self, p):
        """
        functioncall : CSINCOMILLAS LPARENT RPARENT 
                     | CSINCOMILLAS LPARENT argumentos RPARENT
        """
    def p_argumentos(self, p):
        """
        argumentos : expr
                   | expr COMA argumentos
        """
    
    def p_empty(self, p):
        """
        empty : 
        """
        pass
    
    def p_error(self, p):
        if not p:
            print("[parser] Parser error. Valor: " + str(p))
        else:
            print("[parser] Parser error. At line:%s" % p)
        sys.exit(1)
        
    def test(self, data):
        self.parser.parse(data)

    def test_with_file(self, path):
        file = open(path)
        content = file.read()
        self.test(content)
        output_file = path + ".symbols"
        self.simbolos.guardar_tabla_simbolos(output_file)