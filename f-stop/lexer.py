import rply
lexer  = rply.LexerGenerator()
lexer.add("OPEN", r"OPEN")
lexer.add("AS", r"AS")
lexer.add("STRING", r"\".+\"")
lexer.ignore(r"/s+")
l = lexer.build()
for t in l.lex('OPEN "test.png" AS im'):
	print(t)