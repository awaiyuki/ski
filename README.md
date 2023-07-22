# ski
Lambda to SKI translator and SKI evaluator

## How to use
* Python Interpreter에서 다음처럼 ski.py의 모든 요소를 import해서 사용한다.
```
from ski import *
```

* Python으로 ski.py를 직접 실행하면 예제 테스트를 행한다.
```
python3 ski.py
```

## Abstract grammar for lambda expression
* Lambda expression : Lam(variable list, lambda term)
* Application : App(lambda terms)
* Represent a variable in a string
* Examples
```
add = Lam(['m', 'n', 'f', 'x'], App('m', 'f', App('n', 'f', 'x')))
one = Lam(['f', 'x'], App('f', 'x'))
```

## Functions
* Lam(v, e) -- variable list(v)와 lambda term(e)를 받아 해당하는 Abstraction의 내부 표현을 리턴한다.
* App(*e_tuple) -- 복수의 lambda term(e_tuple)을 받아 그것들에 Application을 취한 내부 표현을 리턴한다.
* free_vars(term) -- term의 free variable들을 set의 형태로 리턴한다.
* translate(term) -- 임의의 Lambda expression을 S, K, I combinator로 구성된 expression으로 번역한다.
* print_lam_expr(expr) -- 내부 표현으로 구성된 Lambda expression을 읽기 쉽게 출력한다.
* print_ski_expr(expr) -- 내부 표현으로 구성된 S, K, I combinator expression을 읽기 쉽게 출력한다.
