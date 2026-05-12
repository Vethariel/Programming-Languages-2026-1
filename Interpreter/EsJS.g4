grammar EsJS;

// ─── PALABRAS CLAVE ───────────────────────────────────────────
MUT        : 'mut' ;
CONST      : 'const' ;
VAR        : 'var' ;
FUNCION    : 'funcion' ;
RETORNAR   : 'retornar' ;
SI         : 'si' ;
SINO       : 'sino' ;
MIENTRAS   : 'mientras' ;
PARA       : 'para' ;
ELEGIR     : 'elegir' ;
CASO       : 'caso' ;
POR_DEFECTO: 'porDefecto' ;
ROMPER     : 'romper' ;
AMBIENTE   : 'ambiente' ;
HACER      : 'hacer' ;
CONTINUAR  : 'continuar' ;
INTENTAR   : 'intentar' ;
CAPTURAR   : 'capturar' ;
CREAR      : 'crear' ;
ARREGLO    : 'Arreglo' ;
CADENA     : 'Cadena' ;
MATRIZ     : 'Matriz' ;
MATE       : 'Mate' ;
NUMERO     : 'Numero' ;
BOOLEANO   : 'Booleano' ;
CONSOLA    : 'consola' ;
NAN        : 'NuN' ;

// ─── LITERALES ESPECIALES ────────────────────────────────────
VERDADERO  : 'verdadero' ;
FALSO      : 'falso' ;
NULO       : 'nulo' ;
INDEFINIDO : 'indefinido' ;
INFINITO   : 'Infinito' ;

// ─── OPERADORES 3 CHARS ──────────────────────────────────────
STRICT_EQ  : '===' ;
STRICT_NEQ : '!==' ;

// ─── OPERADORES 2 CHARS ──────────────────────────────────────
EQUAL      : '==' ;
NEQ        : '!=' ;
LEQ        : '<=' ;
GEQ        : '>=' ;
ARROW      : '=>' ;
AND        : '&&' ;
OR         : '||' ;
PLUS_ASSIGN: '+=' ;
INCREMENT  : '++' ;
TERNARY      : '?' ;
MINUS_ASSIGN : '-=' ;
TIMES_ASSIGN : '*=' ;
DIV_ASSIGN   : '/=' ;
MOD_ASSIGN   : '%=' ;
DECREMENT    : '--' ;

// ─── OPERADORES 1 CHAR ───────────────────────────────────────
ASSIGN     : '=' ;
PLUS       : '+' ;
MINUS      : '-' ;
TIMES      : '*' ;
DIV        : '/' ;
MOD        : '%' ;
LESS       : '<' ;
GREATER    : '>' ;
NOT        : '!' ;

// ─── DELIMITADORES ───────────────────────────────────────────
LPAREN     : '(' ;
RPAREN     : ')' ;
LBRACE     : '{' ;
RBRACE     : '}' ;
LBRACKET   : '[' ;
RBRACKET   : ']' ;
SEMICOLON  : ';' ;
COMMA      : ',' ;
COLON      : ':' ;
PERIOD     : '.' ;

// ─── LITERALES ───────────────────────────────────────────────
NUMBER     : [0-9]+ ('.' [0-9]+)? ;
STRING     : ('"' ~["\n]* '"') | ('\'' ~['\n]* '\'') ;
ID         : [a-zA-Z_$\u00C0-\uFFFF] [a-zA-Z0-9_$\u00C0-\uFFFF]* ;

// ─── IGNORADOS ───────────────────────────────────────────────
COMMENT_SL : '//' ~[\n]* -> skip ;
COMMENT_ML : '/*' .*? '*/' -> skip ;
WS         : [ \t\r\n]+ -> skip ;

// ─── PARSER RULES ────────────────────────────────────────────

programa
    : stmt* EOF
    ;

stmt
    : declKeyword declList ';'?
    | SI LPAREN expr RPAREN blockStmt sinoOpt
    | MIENTRAS LPAREN expr RPAREN blockStmt
    | HACER blockStmt MIENTRAS LPAREN expr RPAREN ';'?
    | PARA LPAREN paraInit ';' expr? ';' expr? RPAREN blockStmt
    | ELEGIR LPAREN expr RPAREN LBRACE casoList RBRACE
    | ROMPER ';'?
    | CONTINUAR ';'?
    | INTENTAR blockStmt CAPTURAR blockStmt
    | FUNCION ID LPAREN paramsOpt RPAREN blockStmt
    | RETORNAR expr? ';'?
    | consolaCall ';'?
    | blockStmt
    | expr ';'?
    | ';'
    ;

declKeyword : MUT | CONST | VAR ;

declList
    : ID declInit (',' ID declInit)*
    ;

declInit
    : ASSIGN exprOCrear
    |
    ;

sinoOpt
    : SINO sinoTail
    |
    ;

sinoTail
    : SI LPAREN expr RPAREN blockStmt sinoOpt
    | blockStmt
    ;

blockStmt
    : LBRACE stmt* RBRACE
    ;

paraInit
    : declKeyword declList
    | expr?
    ;

casoList
    : (CASO expr COLON stmt*)*
      (POR_DEFECTO COLON stmt*)?
    ;

// ─── EXPRESIONES ─────────────────────────────────────────────

exprOCrear
    : CREAR crearType (LPAREN argsOpt RPAREN)?
    | expr
    ;

crearType : ID | ARREGLO | CADENA | MATRIZ ;

expr
    : expr ('+'|'-'|'*'|'/'|'%') expr
    | expr ('=='|'==='|'!='|'!==') expr
    | expr ('<'|'>'|'<='|'>=') expr
    | expr (AND|OR) expr
    | expr TERNARY expr COLON expr
    | factor
    ;

factor
    : factor LPAREN argsOpt RPAREN                   // llamada
    | factor LBRACKET expr RBRACKET                  // índice
    | factor PERIOD ID                               // acceso propiedad
    | factor (ASSIGN|PLUS_ASSIGN|MINUS_ASSIGN
             |TIMES_ASSIGN|DIV_ASSIGN|MOD_ASSIGN) exprOCrear  // asignación
    | factor ARROW arrowBody                         // flecha
    | factor (INCREMENT|DECREMENT)                   // sufijo
    | LPAREN argsOpt RPAREN                          // grupo/lambda params
    | LBRACKET arrayArgsOpt RBRACKET                 // arreglo literal
    | LBRACE objElements RBRACE                      // objeto literal
    | (MINUS|PLUS|NOT) factor                        // prefijo
    | ID | NUMBER | STRING
    | VERDADERO | FALSO | NULO | INDEFINIDO | INFINITO | NAN
    | MATE | NUMERO | ARREGLO | CADENA | MATRIZ | BOOLEANO
    | AMBIENTE
    ;

arrowBody
    : blockStmt
    | expr
    ;

// ─── CONSOLA ─────────────────────────────────────────────────

consolaCall
    : CONSOLA PERIOD consolaMethod LPAREN argsOpt RPAREN
    ;

consolaMethod
    : ID   // escribir, error, limpiar, etc.
    ;

// ─── PARÁMETROS Y ARGUMENTOS ─────────────────────────────────

paramsOpt : ID (',' ID)* | ;
argsOpt   : expr (',' expr)* | ;
arrayArgsOpt : expr (',' expr)* | ;

// ─── OBJETOS ─────────────────────────────────────────────────

objElements
    : objProp (',' objProp)*
    |
    ;

objProp
    : ID COLON expr                              // propiedad valor
    | ID LPAREN paramsOpt RPAREN blockStmt       // método
    ;