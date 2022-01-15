priorities={"+":(1,2), "-":(1,2), "*":(3,4), "/":(3,4)}

#Tokeni
Int="Integer"
Op="Operator"
EOF="EOF"
Par="Parenthesis"

functions={"+": lambda x,y: x+y, "-": lambda x,y: x-y,
           "*": lambda x,y: x*y, "/": lambda x,y: x/y}


def tokenize(text: str):
    i=0
    result=[]
    while i<len(text):
        if text[i].isdigit():
            num=""
            while i<len(text) and text[i].isdigit():
                num+=text[i]
                i+=1
            i-=1
            result.append((Int,int(num)))
        elif text[i] in priorities.keys():
            result.append((Op,text[i]))
        elif text[i] in "()":
            result.append((Par,text[i]))
        else:
            pass
        i+=1
        
    return result


class Iterator:
    def __init__(self,value:list)->None:
        self.value=value
        
    def next(self):
        try:
            return self.value.pop(0)
        except:
            return (EOF, None)
    
    def current(self):
        try:
            return self.value[0]
        except:
            return (EOF, None)


def parse(tokens: Iterator, priority: int):
    left_type, left = tokens.next()
    if left_type==Par and left=="(":
        left=parse(tokens,0)
        key,value=tokens.next()
        if key!= Par or value!=")":
            raise SyntaxError("Expected ')', got "+repr(value))
        
    elif left_type != Int:
        raise SyntaxError("Expected number, got " + repr(left))
    
    while True:
        operator_type, operator_value = tokens.current()
        if operator_type in (EOF,Par):
            break
        if operator_type != Op:
            raise SyntaxError("Expected operator, got " +repr(operator_value))
        
        l, r = priorities[operator_value]
        if l < priority:
            break
        
        tokens.next()
        
        right = parse(tokens,r)
        left = (functions[operator_value], left, right)
        
    return left


def calculate(expression):
    if type(expression)==int:
        return expression
    else:
        return expression[0](calculate(expression[1]),calculate(expression[2]))