import sys, os, math

def main():
    if len(sys.argv) != 2:
        print("USO:",sys.argv[0],"entrada", file=sys.stderr)
        exit(1)
    global file
    try:
        file = open(sys.argv[1], "r")
    except Exception as e:
        print(str(e), file=sys.stderr)
        exit(1)
    else:
        parse()

def parse():
    global pila
    pila = []
    if(S()):
        print("Result:", pila[-1])
        print("OK")
    else:
        print("ERROR", file=sys.stderr)
    file.close()

def S():
    global pila
    if M():
        t1 = next_token()
        if t1['type'] == 'sum':
            if(S()): 
                b = pila.pop(-1)
                a = pila.pop(-1)
                pila.append(a+b)
                return True
        if t1['type'] == 'res':
            if(S()):
                b = pila.pop(-1)
                a = pila.pop(-1)
                pila.append(a-b)
                return True
        unget_token(t1)
        return True
    return False


def M():
    global pila
    if P():
        t1 = next_token()
        if t1['type'] == 'mul':
            if(M()): 
                b = pila.pop(-1)
                a = pila.pop(-1)
                pila.append(a*b)
                return True
        if t1['type'] == 'div':
            if(M()):
                b = pila.pop(-1)
                a = pila.pop(-1)
                pila.append(a/b)
                return True
        unget_token(t1)
        return True
    return False

def P():
    if(F()):
        t1 = next_token()
        if t1['type'] == 'pot':
            if P():
                global pila
                b = pila.pop(-1)
                a = pila.pop(-1)
                pila.append(a**b)
                return True
        unget_token(t1)
        return True
    return False


def F():
    if(V()):
        return True
    t1 = next_token()
    if t1['type'] == 'res':
        if(F()):
            global pila
            valor = pila.pop(-1)
            pila.append(-valor)
            return True
    if t1['type'] == 'p_i':
        if(S()):
            t2 = next_token()
            if t2['type'] == 'p_d':
                return True
            else:
                print("Error: se esperaba un )", file=sys.stderr)
    unget_token(t1)
    return False


def V():
    global pila
    t1 = next_token()
    if t1['type'] == 'num':
        pila.append(t1['value'])
        return True
    if t1['type'] == 'nombre':
        if F():
            if t1['lexema'] == 'sqrt':
                a = pila.pop(-1)
                pila.append(math.sqrt(a))
                return True
            elif t1['lexema'] == 'cos':
                a = pila.pop(-1)
                pila.append(math.cos(a))
                return True
            else:
                print(f"Función {t1['lexema']} no implementada", file=sys.stderr)
                return True
    unget_token(t1)
    return False

        
#Analizador léxico
def next_token():
    global file
    matrix = []
    #              '', #, L, ., +, -, *, /, ^, (, ), \, 0, O
    matrix.append([ 0, 1,12, 2, 5, 6, 7, 8, 9,10,11,14,15,16]) #0
    matrix.append([ 4, 1, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]) #1
    matrix.append([16, 3,16,16,16,16,16,16,16,16,16,16,16,16]) #2
    matrix.append([ 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4]) #3
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #4
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #5
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #6
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #7
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #8
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #9
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #10
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #11
    matrix.append([13,13,12,13,13,13,13,13,13,13,13,13,13,13]) #12
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #13
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #14
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #15
    matrix.append([16,16,16,16,16,16,16,16,16,16,16,16,16,16]) #16
    q = 0
    lexema = ""
    while True:
        try:
            p = file.tell()
            c = file.read(1)
            
        except:
            return {'type': 'endf', 'lexema': '\0', 'position': p, 'value': 0}
        else:
            if c == '\n':
                lexema += c
                q = matrix[q][11]
            elif c.isspace():
                lexema += c
                q = matrix[q][0]
            elif c.isdigit():
                lexema += c
                q = matrix[q][1]
            elif c.isalpha():
                lexema += c
                q = matrix[q][2]
            elif c == '.':
                lexema += c
                q = matrix[q][3]
            elif c == '+':
                lexema += c
                q = matrix[q][4]
            elif c == '-':
                lexema += c
                q = matrix[q][5]
            elif c == '*':
                lexema += c
                q = matrix[q][6]
            elif c == '/':
                lexema += c
                q = matrix[q][7]
            elif c == '^':
                lexema += c
                q = matrix[q][8]
            elif c == '(':
                lexema += c
                q = matrix[q][9]
            elif c == ')':
                lexema += c
                q = matrix[q][10]
            elif c == '':
                lexema += c
                q = matrix[q][12]
            else:
                lexema += c
                q = matrix[q][13]

            if q == 4:
                file.seek(p,0)
                return {'type': 'num', 'lexema': lexema.removesuffix(c), 'position': p-len(lexema)+1, 'value': float(lexema.removesuffix(c))}
            elif q == 5: 
                return {'type': 'sum', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 6: 
                return {'type': 'res', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 7:
                return {'type': 'mul', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 8:
                return {'type': 'div', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 9: 
                return {'type': 'pot', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 10:
                return {'type': 'p_i', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 11: 
                return {'type': 'p_d', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 13:
                file.seek(p,0)
                return {'type': 'nombre', 'lexema': lexema.removesuffix(c), 'position': p-len(lexema)+1, 'value': 0}
            elif q == 14:
                return {'type': 'endl', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 15:
                return {'type': 'endf', 'lexema': lexema, 'position': p, 'value': 0}
            elif q == 16:
                return {'type': 'error', 'lexema': lexema, 'position': p, 'value': 0}

def unget_token(token: dict):
    global file
    file.seek(token['position'],0)
        
if __name__ == "__main__": main()