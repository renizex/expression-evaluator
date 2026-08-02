# expression-evaluator
a plenty of implementations of a mathematical expression evaluator.
starting from my own naive algorithm and ending with an AST-based parser.

1. prototype.
my first attempt.
works, but primitive and contains many flaws in any aspect.
example: 1 + 1 = 2
status: done.

2. stack-based evaluator
a stack-based mathematical expression evaluator supporting Reverse Polish Notation (RPN) and infix notation.
uses a multi-stage processing pipeline:
input -> tokenization -> expression conversion -> evaluation -> output

supported features:
Reverse Polish Notation (RPN):
example: 1 1 + = 2
infix notation:
example: 1 + 1 = 2
you can switch between modes by typing 'RPN' and 'INFIX' respectively.

architecture:
token-based processing.
stack-based evaluation.
separate tokenization and evaluation stages.

variables and memory:

rpn:
x 5 =
infix:
x = 5

in memory: x = 5

basic operations:
+, -, *, /.

status: active development.

planned:
parentheses for infix expressions.
operators: ^, %.
further architectural improvements.

3. AST
builds an abstract syntax tree before evaluation
status: planned.
