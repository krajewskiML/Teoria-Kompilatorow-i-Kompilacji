grammar synth;

program: function* function_final EOF;

function: type IDENTIFIER '(' parameters ')' return_block;

parameters: (expression (',' expression)*)?;

function_final: FINAL bpm_definition block;

bpm_definition: BPM '=' INT;

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

for_statement: FOR '(' var_definition ';' expression ';' expression (',' expression)* ')' block;

assignment: IDENTIFIER '=' expression;

function_call: IDENTIFIER '(' parameters ')';

expression: IDENTIFIER
          | var_definition
          | function_call
          | '(' expression ')'
          | expression mult_op expression
          | expression add_op expression
          | expression compare_op expression
          | expression bool_op expression
          | CHANNEL chann_op expression
          ;

bool_op: 'and' | 'or';

compare_op: '==' | '!=' | '>' | '<' | '>=' | '<=';

add_op: '+' | '-';

mult_op: '*' | '/' | '%';

chann_op: 'append' | 'remove';

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

synth_definition: 'synth' IDENTIFIER '=' synth_name '(' synth_params* ')';

synth_name: (SINE | LFO | SUPERSAW | FASTSINE | RCOSC | PAUSE);

synth_params: FREQ '=' FLOAT | MUL '=' FLOAT | ADD '=' FLOAT;

sequence_definition: 'seq' IDENTIFIER '=' '[' (expression (',' expression)*)* ']';

value: BOOL | INT | FLOAT | SOUND | SYNTH | SEQ;

IF: 'if';
ELSE: 'else';
ELIF: 'elif';
FOR: 'for';
WHILE: 'while';
RETURN: 'return';
IN: 'in';
RANGE: 'range';
FINAL: 'final';
BOOL: 'true' | 'false';
INT: [+-]?[0-9]+;
FLOAT: [+-]?([0-9]*[.])?[0-9]+;

SINE: 'sine';
LFO: 'lfo';
SUPERSAW: 'supersaw';
FASTSINE: 'fastsine';
RCOSC: 'rscosc';
PAUSE: 'pause';

FREQ: 'freq';
MUL: 'mul';
ADD: 'add';

SOUND: 'sound';
SYNTH: 'synth';
SEQ: 'sequence';
CHANNEL: '#' [0-9]+;

BPM: 'BPM';

LP: '(';
RP: ')';
LB: '{';
RB: '}';
COMMA: ',';
EQUALS: '=';
SEMICOLON: ';';

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]*;

SPACE: [ \t\n\r] -> skip;
