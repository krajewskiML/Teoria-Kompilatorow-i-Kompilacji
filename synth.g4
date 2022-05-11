grammar synth;

program: function* function_final EOF;

function: type IDENTIFIER '(' parameters ')' return_block;

parameters: (expression (',' expression)*)?;

function_final: 'final' block;

block: '{' line* '}';

return_block: '{' line* RETURN IDENTIFIER'}'

line: statement
     | if_statement
     | while_statement
     | for_statement
     ;

statement: (var_definition | assignment | function_call) ';' ;

if_statement: IF '(' expression ')' block (ELIF '(' expression ')' block)* (ELSE block)?;

while_statement: WHILE '(' expression ')' block;

for_statement: FOR '(' assignment ';' expression ';' block ')' block;

assignment: IDENTIFIER '=' expression;

function_call: IDENTIFIER '('  ')';

expression:
    constant
    | IDENTIFIER
    | function_call
    | '(' expression ')'
    | expression multOp expression
    | expression addOp expression
    | expression compareOp expression
    | expression boolOp expression

boolOp: 'and' | 'or' | 'xor';

compareOp: '==' | '!=' | '>' | '<' | '>=' | '<=';

addOp: '+' | '-';

multOp: '*' | '/' | '%';

var_definition: bool_definition | float_definition | int_definition | sound_definition;

bool_definition: 'bool' IDENTIFIER '=' (True | False);

float_definition: 'float' IDENTIFIER '=' FLOAT;

int_definition: 'int' IDENTIFIER '=' INT;

sound_definition: 'sound' IDENTIFIER '=' SOUND

synth_definition: 'synth' IDENTIFIER '=' synth_name synth_params

synth_name: (SINE | LFO | SUPERSAW | FASTSINE | RCOSC)
synth_params: '(' FREQ '=' FLOAT ',' MUL '=' FLOAT ',' ADD '=' FLOAT ')';

type: INT | FLOAT |

IF: 'if';
ELSE: 'else';
FOR: 'for';
WHILE: 'while';
RETURN: 'return'

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

INT: [+-]?[0-9]+;
FLOAT: [+-]?([0-9]*[.])?[0-9]+;

SINE: 'sine';
LFO: 'lfo';
SUPERSAW: 'supersaw';
FASTSINE: 'fastsine';
RCOSC: 'rscosc';

FREQ: 'freq';
MUL: 'mul';
ADD: 'add';

SOUND: 'sound';
SYNTH: 'synth';
SEQ: '[' (expression (',' expression)*)* ']'; # seq
CHANNEL: '#' INTEGER;
