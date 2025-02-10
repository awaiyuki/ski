# ski
Lambda to SKI translator and SKI evaluator.
It translates lambda expressions into SKI combinator expresssions and evaluates them.

## How to use
* To use, import all elements from `ski.py` in the Python interpreter as shown below:
```
from ski import *
```

* To run example tests, execute `ski.py` directly with Python:
```
python3 ski.py
```

## Abstract grammar for lambda expression
* **Lambda expression**: Lam(variable list, lambda term)
* **Application**: App(lambda terms)
* **Variable**: a string

### Examples
```
add = Lam(['m', 'n', 'f', 'x'], App('m', 'f', App('n', 'f', 'x')))
one = Lam(['f', 'x'], App('f', 'x'))
```

## Functions
* `Lam(v, e)`  
  Takes a variable list (`v`) and a lambda term (`e`) as inputs and returns the internal representation of the corresponding abstraction.

* `App(*e_tuple)`  
  Takes multiple lambda terms (`e_tuple`) as inputs and returns the internal representation of their application.

* `free_vars(term)`  
  Returns the set of free variables in the given term.

* `translate(term)`  
  Translates the given lambda expression `term` into an expression composed of S, K, and I combinators.

* `print_lam_expr(expr)`  
  Prints the lambda expression constructed in internal representation in a human-readable format.

* `print_ski_expr(expr)`  
  Prints the S, K, I combinator expression constructed in internal representation in a human-readable format.
