import sys
from ajson_lexer import LexerClass
from ajson_parser import ParserClass

if len(sys.argv)==2:
    print("Error: Faltan argumentos")

elif sys.argv[2] == "-lex":
    l = LexerClass()
    l.test_with_file(sys.argv[1])

elif sys.argv[2] == "-par":
    p = ParserClass()
    p.test_with_file(sys.argv[1])

