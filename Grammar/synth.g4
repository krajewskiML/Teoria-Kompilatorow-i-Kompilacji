grammar synth;

program: function* function_final EOF;

function: type IDENTIFIER LP (var_definition (COMMA  var_definition)*)? RP return_block;

parameters: (expression (COMMA expression)*)?;

function_final: FINAL bpm_definition block;

bpm_definition: BPM EQUALS INT;

block: LB line* RB;

return_block: LB line* RETURN expression RB;

line: statement
     | if_statement
     | while_statement
     | for_statement
     ;

statement: (var_definition | assignment | var_definition_assignment) SEMICOLON ;

if_statement: IF LP expression RP block (ELIF LP expression RP block)* (ELSE block)?;

while_statement: WHILE LP expression RP block;

for_statement: FOR LP IDENTIFIER IN (RANGE INT RP | SEQ) block;

assignment: IDENTIFIER EQUALS expression;

function_call: IDENTIFIER LP parameters RP;

expression: IDENTIFIER
          | function_call
          | LP expression RP
          | expression mult_op expression
          | expression add_op expression
          | expression compare_op expression
          | expression bool_op expression
          | value
          ;

bool_op: 'and' | 'or';

compare_op: '==' | '!=' | '>' | '<' | '>=' | '<=';

add_op: '+' | '-';

mult_op: '*' | '/' | '%';

chann_op: 'append' | 'remove';

var_definition: type IDENTIFIER;

var_definition_assignment: bool_definition
                    | float_definition
                    | int_definition
                    | sound_definition
                    | synth_definition
                    | sequence_definition
                    ;

bool_definition: 'bool' IDENTIFIER EQUALS BOOL;

float_definition: 'float' IDENTIFIER EQUALS FLOAT;

int_definition: 'int' IDENTIFIER EQUALS INT;

sound_definition: 'sound' IDENTIFIER EQUALS SOUND;

synth_definition: 'synth' IDENTIFIER EQUALS synth_name LP synth_params* RP;

synth_name: (SINE | LFO | SUPERSAW | FASTSINE | RCOSC | PAUSE);

synth_params: FREQ EQUALS FLOAT | MUL EQUALS FLOAT | ADD EQUALS FLOAT;

sequence_definition: 'seq' IDENTIFIER EQUALS '[' (expression (COMMA expression)*)* ']';

type: 'bool' | 'float' | 'int' | 'sound' | 'synth' | 'seq';

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
