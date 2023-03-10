LAM_SIGN = '_lam'
APP_SIGN = '_app'
S_SIGN = '_s'
K_SIGN = '_k'
I_SIGN = '_i'


def Lam(v, e):
    """ variable list(v)와 lambda term(e)를 받아
        해당하는 abstraction의 내부 표현을 리턴
    """
    # v가 list일 경우 원소를 하나씩 꺼내서,
    # abstraction이 파라미터를 하나씩 가지도록 내부 표현을 구성 (recursive하게 구현)
    if isinstance(v, list):
        if len(v) == 1:
            return Lam(v[0], e)
        return Lam(v[0], Lam(v[1:], e))

    return (LAM_SIGN, v, e)


def App(*e_tuple):
    """ 복수의 lambda term(e_tuple)을 받아
        application을 취한 내부 표현을 리턴
    """
    if(len(e_tuple) < 2):
        print("error in App")
        return (APP_SIGN, e_tuple[0])

    res = (APP_SIGN, e_tuple[0], e_tuple[1])
    
    # e_tuple의 원소가 3개 이상일 경우 3번째 원소부터 다시 application 취하도록 함
    for i in range(2, len(e_tuple)):
        res = (APP_SIGN, res, e_tuple[i])

    return res


def is_lambda(expr):
    if isinstance(expr, tuple):
        if expr[0]==LAM_SIGN:
            return True
    return False

def is_application(expr):
    if isinstance(expr, tuple):
        if expr[0]==APP_SIGN:
            return True
    return False


def free_vars(term):
    """ term의 free variable들을 set의 형태로 리턴
    """
    if not isinstance(term, tuple):
        return set([term])
    if is_lambda(term):
        frees = free_vars(term[2])
        if term[1] in frees:
            frees.remove(term[1])
        return frees
    if is_application(term):
        frees = free_vars(term[1])
        frees.update(free_vars(term[2]))
        return frees

    print('error in free_vars. term: ')


def translate(term):
    """ 임의의 Lambda expression을 S,K,I combinator로 구성된 expression으로 번역
    """
    if not isinstance(term, tuple):  # Rule 1
        return term
    if is_application(term):  # Rule 2
        return App(translate(term[1]), translate(term[2]))
    if is_lambda(term):
        if term[1] not in free_vars(term[2]):  # Rule 3
            return App(K_SIGN, translate(term[2]))
        if term[1] == term[2]:  # Rule 4
            return I_SIGN
        if isinstance(term[2], tuple):
            if is_lambda(term[2]) and (term[1] in free_vars(term[2][2])):  # Rule 5
                return translate(Lam(term[1], translate(Lam(term[2][1], term[2][2]))))
            if is_application(term[2]) and ((term[1] in free_vars(term[2][1])) or (term[1] in free_vars(term[2][2]))):  # Rule 6
                return App(S_SIGN, translate(Lam(term[1], term[2][1])), translate(Lam(term[1], term[2][2])))
    
    print("error in translate. term:", term)


def is_evaluable_I(term):
    if term[1]==I_SIGN:
        return True
    return False

def is_evaluable_K(term):
    if is_application(term[1]):
        if term[1][1] == K_SIGN:
            return True
    return False

def is_evaluable_S(term):
    if is_application(term[1]):
        if is_application(term[1][1]):
            if term[1][1][1] == S_SIGN:
                return True
    return False

def evaluate(term):
    if not is_application(term):  # leaf
        return term
    
    if is_evaluable_I(term):
        x = evaluate(term[2])
        return x
    elif is_evaluable_K(term):
        x = evaluate(term[1][2])
        return x
    elif is_evaluable_S(term):
        x = evaluate(term[1][1][2])
        y = evaluate(term[1][2])
        z = evaluate(term[2])
        return evaluate(App(evaluate(App(x, z)), evaluate(App(y, z))))

    term1_evaluated = evaluate(term[1])
    term2_evaluated = evaluate(term[2])

    if term[1] == term1_evaluated and term[2] == term2_evaluated:
        return term

    return evaluate(App(term1_evaluated, term2_evaluated))


def unchurch_ski(expr):
    num = 0
    evaluated = evaluate(App(expr, '+1', '0'))
    while is_application(evaluated):
        if evaluated[1] != '+1':
            print('error in unchurch_ski.')
            return
        num += 1
        evaluated = evaluated[2]
    return num


def print_lam_expr(expr, new_line = True):
    """ 내부 표현으로 구성된 Lambda expression을 읽기 쉽게 출력
        new_line이 True이면 출력 후 개행하고 False이면 개행하지 않음
    """
    if not isinstance(expr, tuple):
        print(expr, end=' ')
    if is_lambda(expr):
        print('\\', end='')
        print_lam_expr(expr[1], new_line=False)
        print('->', end=' ')
        print_lam_expr(expr[2], new_line=False)
    if is_application(expr):
        if isinstance(expr[1], tuple):
            if is_lambda(expr[1]):
                print('(', end=' ')
                print_lam_expr(expr[1], new_line=False)
                print(')', end=' ')
            else:
                print_lam_expr(expr[1], new_line=False)
        else:
            print_lam_expr(expr[1], new_line=False)
        if isinstance(expr[2], tuple):
            print('(', end=' ')
            print_lam_expr(expr[2], new_line=False)
            print(')', end=' ')
        else:
            print_lam_expr(expr[2], new_line=False)
            
    if new_line:
        print()


def print_ski_expr(expr, new_line = True):
    """ 내부 표현으로 구성된 S, K, I combinator expression을 읽기 쉽게 출력
        new_line이 True이면 출력 후 개행하고 False이면 개행하지 않음
    """
    # expr이 application이 아닐 경우
    if not isinstance(expr, tuple):
        if expr == S_SIGN:
            print('S', end='')
        elif expr == K_SIGN:
            print('K', end='')
        elif expr == I_SIGN:
            print('I', end='')
        else:
            print('\nerror in print_ski_expr. expr:', expr)
        return

    # expr이 application일 경우
    print_ski_expr(expr[1], new_line = False)
    if isinstance(expr[2], tuple):
        print('(', end='')
    print_ski_expr(expr[2], new_line = False)
    if isinstance(expr[2], tuple):
        print(')', end='')
    
    if new_line:
        print()


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


if __name__ == "__main__":
    print('- ski')
    print('- 테스트')

    zero = Lam(['f', 'x'], 'x')
    one = Lam(['f', 'x'], App('f', 'x'))
    two = Lam(['f', 'x'], App('f', App('f', 'x')))
    five = Lam(['f', 'x'], App('f', App('f', App('f', App('f', App('f', 'x'))))))
    add = Lam(['m', 'n', 'f', 'x'], App('m', 'f', App('n', 'f', 'x')))
    mult = Lam(['m', 'n', 'f'], App('m', App('n', 'f')))

    print('\n1 :', end=' ')
    print_lam_expr(one)
    print('2 :', end=' ')
    print_lam_expr(two)
    print('5 :', end=' ')
    print_lam_expr(five)
    print('add :', end=' ')
    print_lam_expr(add)
    print('mult :', end=' ')
    print_lam_expr(mult)
    print()

    add_one_two = translate(App(add, one, two))
    print(color.BOLD + 'translate(add 1 2)' + color.END + ' :', end=' ')
    print_ski_expr(add_one_two, new_line=False)
    print(color.BOLD + ' ---> ' + str(unchurch_ski(add_one_two)) + color.END)
    #print(color.BOLD + '(add 1 2) (+1) 0' + color.END + ' ---> ' + color.BOLD + str(unchurch_ski(add_one_two)) + color.END)
    print()

    mult_five_two = translate(App(mult, five, two))
    print(color.BOLD + 'translate(mult 5 2)' + color.END+ ' :', end=' ')
    print_ski_expr(mult_five_two, new_line=False)
    print(color.BOLD + ' ---> ' + str(unchurch_ski(mult_five_two)) + color.END)
    print()
    #print(color.BOLD + '(mult 5 2) (+1) 0' + color.END + ' ---> ' + color.BOLD + str(unchurch_ski(mult_five_two)) + color.END)
    #print()