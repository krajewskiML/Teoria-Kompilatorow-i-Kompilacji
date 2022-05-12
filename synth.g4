grammar synth;

program: function* function_final EOF;

function: type IDENTIFIER '(' parameters ')' return_block;

parameters: (expression (',' expression)*)?;

function_final: 'final' block;

block: '{' line* '}';

return_block: '{' line* RETURN IDENTIFIER'}';

line: statement
     | if_statement
     | while_statement
     | for_statement
     ;

statement: (var_definition | assignment | function_call) ';' ;

if_statement: IF '(' expression ')' block (ELIF '(' expression ')' block)* (ELSE block)?;

while_statement: WHILE '(' expression ')' block;

for_statement: FOR '(' assignment ';' expression ';' expression (',' expression)* ')' block;

assignment: IDENTIFIER '=' expression;

function_call: IDENTIFIER '(' parameters ')';

expression: IDENTIFIER
          | function_call
          | '(' expression ')'
          | expression multOp expression
          | expression addOp expression
          | expression compareOp expression
          | expression boolOp expression
          ;

boolOp: 'and' | 'or';

compareOp: '==' | '!=' | '>' | '<' | '>=' | '<=';

addOp: '+' | '-';

multOp: '*' | '/' | '%';

var_definition: bool_definition
              | float_definition
              | int_definition
              | sound_definition
              | synth_definition
              | sequence_definition
              ;

bool_definition: 'bool' IDENTIFIER '=' BOOL;

float_definition: 'float' IDENTIFIER '=' FLOAT;

int_definition: 'int' IDENTIFIER '=' INT;

sound_definition: 'sound' IDENTIFIER '=' SOUND;

synth_definition: 'synth' IDENTIFIER '=' synth_name synth_params;

synth_name: (SINE | LFO | SUPERSAW | FASTSINE | RCOSC);
synth_params: '(' FREQ '=' FLOAT ',' MUL '=' FLOAT ',' ADD '=' FLOAT ')';

sequence_definition: 'seq' IDENTIFIER '=' '[' (expression (',' expression)*)* ']';

type: BOOL | INT | FLOAT | SOUND | SYNTH | SEQ;

IF: 'if';
ELSE: 'else';
ELIF: 'elif';
FOR: 'for';
WHILE: 'while';
RETURN: 'return';

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

BOOL: TRUE | FALSE;
INT: [+-]?[0-9]+;
FLOAT: [+-]?([0-9]*[.])?[0-9]+;

TRUE: 'True';
FALSE: 'False';

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
SEQ: 'sequence';
CHANNEL: '#' INT;
