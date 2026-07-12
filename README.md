# expression-evaluator
a plenty of implementations of a mathematical expression evaluator.
starting from my own naive algorithm and ending with an AST-based parser.

1. prototype.
my first attempt.
works, but primitive and contains many flaws in any aspect.
example: 1 + 1 = 2
status: done.

2. stack-rpn (reverse Polish Notation)
classic sorting approach using stacks.
example: 1 1 + = 2
status: work in progress

3. stack-infix
example: 1 + 1 = 2
a stack based evaluator that parses infix notation.
status: planned.

5. AST
builds an abstract syntax tree before evaluation
status: planned.

also planned but not necessarily: 
combine the second and third ones into one, and add an option for the user to select the mode.
