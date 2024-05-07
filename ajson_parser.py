import ply.yacc as yacc
from ajson_lexer import LexerClass
import sys

class ParserClass:
    """
    Clase que define el parser para el lenguaje ajson
    """
    tokens = LexerClass.tokens #tokens que se pueden usar

    def __init__(self):
        self.parser = yacc.yacc(module=self,  debug=True)
        self.lexer = LexerClass().lexer #se crea el lexer
        self.symbols = {} #se crea el diccionario de simbolos

    # Define la precedencia y asociatividad de los operadores
    precedence = (
        ('left', 'SUMA', 'RESTA'),
        ('left', 'MUL', 'DIV'),
        ('left', 'USUMA', 'URESTA'),
        ('left', 'LE', 'LT', 'GE', 'GT', 'EQ'),
        ('right', 'NOT'),
        ('left', 'AND', 'OR')
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

    def p_num(self, p):
        """
        num : ENTERO
            | DECIMAL
        """
    
    def p_bool(self, p):
        """
        bool : TR
             | FL
        """

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

    
    def p_var(self, p):
        """
        var : CSINCOMILLAS
            | CSINCOMILLAS PUNTOS tipo
        """
        if len(p) == 2:
            self.symbols[p[1]] = (None, None)
        else:
            self.symbols[p[1]] = (p[3], None)

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
        if p[1] not in self.symbols:
            print("[ERROR][SEMANTIC] Error: variable %s no declarada", p[1])
        else:
            
            self.symbols[p[1]] = (self.symbols[p[1]][0], p[3])

    def p_expr(self, p):
        """
        expr : operacion
              | num
              | bool
              | NULL  
              | CSINCOMILLAS
              | RESTA expr %prec URESTA
              | SUMA expr %prec USUMA
              | CARACTER
              | ajson
              | LPARENT expr RPARENT
              | punto
              | corchete
              | functioncall
        """
        

    def p_operacion(self, p):
        """
        operacion : aritmetica
                  | binaria
                  | comparation
        """
    
    def p_aritmetica(self, p):
        """
        aritmetica : expr SUMA expr
                   | expr RESTA expr
                   | expr MUL expr %prec MUL
                   | expr DIV expr %prec DIV
        """
    
    def p_binaria(self, p):
        """
        binaria : expr AND expr
                | expr OR expr
                | NOT expr
        """
    
    def p_comparation(self, p):
        """
        comparation : expr LE expr
                    | expr LT expr
                    | expr GE expr
                    | expr GT expr
                    | expr EQ expr
        """

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