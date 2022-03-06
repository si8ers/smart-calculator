# write your code here
import collections
import re


class Calc:
    priority = {')': 0, '+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3, '(': 4}

    def __init__(self):
        self.memory = {}
        self.go = True
        self.expr = ''
        self.numbers = collections.deque()
        self.operands = collections.deque()
        self.brackets = collections.deque()

    def on(self):
        while self.go:
            self.expr = input()
            ok = self.check()
            if ok is False:
                continue
            value = None
            while ok:
                ok = self.exec_operation(1)
            if ok is None:
                continue
            if self.numbers:
                value = self.numbers.popleft()
            if self.operands or self.numbers or self.brackets:
                print('Invalid expression')
            elif value is not False and value is not None:
                print(int(value))

    def check(self):
        if re.match(r'/[\D\w]\w*', self.expr):
            self.parse_command()
            return False
        if self.expr.find('=') > -1:
            return self.parse_assign()
        return self.parse_expression()

    def parse_command(self):
        if self.expr == '/exit':
            print('Bye!')
            self.go = False
            return False
        elif self.expr == '/help':
            print("""
                The program calculates the sum, the difference of the numbers.
                Checks the correctness of the input.
                Has the ability to remember variables.
            """)
        else:
            print('Unknown command')
            return False
        return True

    def parse_assign(self):
        parse = re.match(r'^\s*(\w+)\s*=\s*(\w+)\s*$', self.expr)
        if parse:
            value = None
            if re.match(r'^\d+$', parse[2]):
                value = int(parse[2])
            elif re.match(r'^[A-Za-z]+$', parse[2]) is None:
                print('Invalid identifier')
                return False
            elif parse[2] in self.memory.keys():
                value = self.memory[parse[2]]
            if re.match(r'^[A-Za-z]+$', parse[1]) is None:
                print('Invalid identifier')
            elif value is None:
                print('Unknown variable')
            else:
                self.memory[parse[1]] = value
                return True
        else:
            print('Invalid assignment')
        return False

    def parse_expression(self):
        self.numbers = collections.deque()
        self.operands = collections.deque()
        self.brackets = collections.deque()

        parse = re.findall(r'(\-?\w+|[\-\+/*%\^\(\)])', self.expr)
        if parse:
            while parse:
                item = parse.pop(0)

                # Parse operands
                if item == '-':
                    while parse and parse[0] == '-':
                        parse.pop(0)
                        item = '+' if item == '-' else '-'
                elif item == '+':
                    while parse and parse[0] == '+':
                        parse.pop(0)
                elif item == '/':
                    if parse and parse[0] == '/':
                        parse.pop(0)
                        item = '//'
                # preCalc if item is operand
                if item in self.priority.keys():
                    go_calc = True
                    while go_calc:
                        go_calc = self.exec_operation(self.priority[item])
                        if go_calc is None:
                            return False

                    if item == '(':
                        self.brackets.appendleft(len(self.brackets)+1)
                    if item == ')':
                        if self.brackets:
                            self.brackets.popleft()
                        else:
                            print('Invalid expression')
                            return False
                    else:
                        self.operands.appendleft(item)

                # find value if item is not operand
                else:
                    value = None
                    if re.match(r'-?\d+', item):
                        value = int(item)
                    elif re.match(r'^-?[A-Za-z]+$', item):
                        sign = -1 if item[0] == '-' else 1
                        item = item.lstrip('-')
                        if item in self.memory.keys():
                            value = self.memory[item] * sign
                    else:
                        print('Invalid identifier', item)
                        return False
                    if value is None:
                        print('Unknown variable')
                        return False
                    self.numbers.appendleft(value)
        return True

    def exec_operation(self, priority=0):
        last_operand = self.operands[0] if self.operands else None
        if last_operand is None or priority > self.priority[last_operand]:
            return False
        if last_operand == '(':
            if priority == 0:
                self.operands.popleft()
                return True
            return False
        operand = self.operands.popleft()
        len_numbers = len(self.numbers)
        if len_numbers < 2:
            print('Invalid expression')
            return None
        two = self.numbers.popleft()
        one = self.numbers.popleft()
        if operand == '+':
            self.numbers.appendleft(one + two)
            return True
        if operand == '-':
            self.numbers.appendleft(one - two)
            return True
        if operand == '*':
            self.numbers.appendleft(one * two)
            return True
        if operand == '/':
            if two == 0:
                print('Division by Zero')
                return None
            self.numbers.appendleft(one / two)
            return True
        if operand == '//':
            if two == 0:
                print('Division by Zero')
                return None
            self.numbers.appendleft(one // two)
            return True
        if operand == '%':
            if two == 0:
                print('Division by Zero')
                return None
            self.numbers.appendleft(one % two)
            return True
        if operand == '^':
            self.numbers.appendleft(one ** two)
            return True

        print('Unknown operand')
        return None


calc = Calc()
while calc.go:
    calc.on()
