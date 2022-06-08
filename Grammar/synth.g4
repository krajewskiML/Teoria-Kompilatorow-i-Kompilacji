grammar synth;

program: function* function_final EOF;

function: type IDENTIFIER LP (var_definition (COMMA  var_definition)*)? RP return_block;

return_block: LB line* RETURN expression SEMICOLON RB;

function_final: FINAL bpm_definition block;

bpm_definition: BPM IS INT;

block: LB line* RB;

line: statement
     | if_statement
     | while_statement
     | for_statement
     | print_statement
     ;

statement: (var_definition | var_definition_assignment) SEMICOLON ;

if_statement: IF LP expression RP block (ELIF LP expression RP block)* (ELSE block)?;

while_statement: WHILE LP expression RP block;

for_statement: FOR LP IDENTIFIER IN (RANGE INT | IDENTIFIER) RP block ;

print_statement: PRINT LP expression RP SEMICOLON;

function_call: IDENTIFIER LP parameters RP;

parameters: (expression (COMMA expression)*)?;

expression: IDENTIFIER
          | function_call
          | logic_expression
          | math_expression
          ;

logic_expression: IDENTIFIER
                | function_call
                | LP logic_expression RP
                | math_expression compare_op math_expression
                | logic_expression bool_op logic_expression
                | BOOL
                ;

math_expression: IDENTIFIER
                | function_call
                | LP math_expression RP
                | math_expression mult_op math_expression
                | math_expression add_op math_expression
                | INT
                | FLOAT
                ;

bool_op: AND | OR;

compare_op: EQUALS | NOT_EQUALS | GT | LT | GOET | LOET;

add_op: ADDITION | SUBTRACTION;

mult_op: MULTIPLICATION | DIVISION | MODULO;

chann_op: APPEND | REMOVE;

var_definition: type IDENTIFIER;

var_definition_assignment: IDENTIFIER IS expression
                         | (INT_TYPE | FLOAT_TYPE) IDENTIFIER IS math_expression
                         | BOOL_TYPE IDENTIFIER IS logic_expression
                         ;

synth_name: (SINE | LFO | SUPERSAW | FASTSINE | RCOSC | PAUSE);

synth_params: FREQ IS FLOAT | MUL IS FLOAT | ADD IS FLOAT;

synth_constructor: synth_name LP synth_params* RP;

sequence_constructor: LSB (expression (COMMA expression)*)* RSB;

type: BOOL_TYPE | FLOAT_TYPE | INT_TYPE | SOUND_TYPE | SYNTH_TYPE | SEQUENCE_TYPE;

value: BOOL | INT | FLOAT | SOUND | synth_constructor | sequence_constructor;

IF: 'if';
ELSE: 'else';
ELIF: 'elif';
FOR: 'for';
WHILE: 'while';
RETURN: 'return';
IN: 'in';
RANGE: 'range';
FINAL: 'final';
PRINT: 'print';

BOOL: 'true' | 'false';
INT: [+-]?[0-9]+;
FLOAT: [+-]?([0-9]*[.])?[0-9]+;

BOOL_TYPE: 'bool';
INT_TYPE: 'int';
FLOAT_TYPE: 'float';
SOUND_TYPE: 'sound';
SYNTH_TYPE: 'synth';
SEQUENCE_TYPE: 'seq';

SINE: 'sine';
LFO: 'lfo';
SUPERSAW: 'supersaw';
FASTSINE: 'fastsine';
RCOSC: 'rscosc';
PAUSE: 'pause';

FREQ: 'freq';
MUL: 'mul';
ADD: 'add';

SOUND: ["][a-zA-Z0-9_]+.[m][p][3]["];
CHANNEL: '#' [0-9]+;

BPM: 'BPM';

AND: 'and';
OR: 'or';
EQUALS: '==';
NOT_EQUALS: '!=';
GT: '>';
LT: '<';
GOET: '>=';
LOET: '<=';
ADDITION: '+';
SUBTRACTION: '-';
MULTIPLICATION: '*';
DIVISION: '/';
MODULO: '%';
APPEND: 'append';
REMOVE: 'remove';

LP: '(';
RP: ')';
LSB: '[';
RSB: ']';
LB: '{';
RB: '}';
COMMA: ',';
IS: '=';
SEMICOLON: ';';

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

SPACE: [ \t\n\r] -> skip;
