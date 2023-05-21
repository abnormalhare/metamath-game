import copy
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

# GLOBAL VARIABLES #
gWFFID = 0
gSUB = 0

# CLASSES #
class WFF:
    def __init__(self, name: str) -> None:
        global gWFFID
        self.name = name
        self.id = gWFFID
        gWFFID += 1
    
    def __str__(self) -> str:
        return self.name

class Syntax:
    def __init__(self, symbol: str, func: callable) -> None:
        self.symbol = symbol
        self.test = func

class Expression:
    def __init__(self, var1=None, syntax: Syntax=None, var2=None):
        self.var1 = var1
        self.syntax = syntax
        self.var2 = var2
        self.id = var1.id * gWFFID * 2 if var1 is not None else gWFFID * 2
        try:
            self.id += var2.id * gWFFID * 3
        except:
            self.id += gWFFID * 3

        if var2 is None:
            self.type = "WFF"   
        elif var1 is None:
            self.type = "NOT"
        else:
            self.type = "EXP"
    
    def __str__(self) -> str:
        if self.type == "NOT":
            return f"{self.syntax.symbol} {self.var2}"
        elif self.type == "WFF":
            return f"{self.var1}"
        elif self.type == "EXP":
            return f"({self.var1} {self.syntax.symbol} {self.var2})"
    
    def substitute(self, var1, var2=None):
        if isinstance(var1, Expression):
            var1 = var1.substitute(var1.var1, var1.var2)
        if isinstance(var2, Expression):
            var2 = var2.substitute(var2.var1, var2.var2)
        
        if self.type == "NOT":
            return Expression(None, self.syntax, var1)
        return Expression(var1, self.syntax, var2)
    
    def test(self, var1, var2=None) -> bool:
        if self.syntax is None:
            return var1
        if isinstance(var1, Expression):
            var1 = var1.test(var1, var2)
        if isinstance(var2, Expression):
            var2 = var2.test(var1, var2)
        return self.syntax.test(var1, var2)

class Axiom:
    def __init__(self, name, *expressions) -> None:
        self.name = name
        self.expressions = expressions

    def rec_sub(self, expression, *vars) -> list:
        sub1 = None
        sub2 = None
        if expression.type == "EXP":
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return Expression(sub1, expression.syntax, sub2)
        elif expression.type == "WFF":
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return expression.substitute(sub1)
        elif expression.type == "NOT":
            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]
            
            return Expression(None, expression.syntax, sub2)
    
    # expression.syntax.test(sub1, sub2)
    def rec_test(self, expression: Expression, *vars: bool) -> bool:
        sub1 = None
        sub2 = None
        if expression.type == "EXP":
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return expression.syntax.test(sub1, sub2)
        elif expression.type == "WFF":
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return sub1
        elif expression.type == "NOT":
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]
            
            return expression.syntax.test(sub2)
    
    def substitute(self, *vars) -> list:
        global gSUB
        print("\n" + " " * gSUB + "Axiom:", self.name + ", Substituting")
        gSUB += 2

        checkList = []
        retList = []
        print()
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_sub(i, *vars))
            print(" " * gSUB + "wff", str(retList[-1]))
        
        gSUB -= 2
        print(" " * gSUB + "-" * (30 - gSUB))
        return retList[-1]

    def test(self, *vars):
        global gSUB
        print("\n" + " " * gSUB + "Axiom:", self.name + ", Testing")
        gSUB += 2
        
        checkList = []
        retList = []
        print()
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_test(i, *vars))
            print(" " * gSUB + "wff", i, " : ", str(retList[-1]))
        
        gSUB -= 2
        print(" " * gSUB + "-" * (30 - gSUB))
        return retList[-1]

class Theorem:
    def __init__(self, name: str, assertion: Expression, *operations: list) -> None:
        self.name = name
        self.assertion = assertion
        self.operations = operations
    
    def rec_sub(self, expression, *vars) -> list:
        sub1 = None
        sub2 = None
        if expression.type == "EXP":
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return Expression(sub1, expression.syntax, sub2)
        elif expression.type == "WFF":
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return expression.substitute(sub1)
        elif expression.type == "NOT":
            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]
            
            return Expression(None, expression.syntax, sub2)
    
    def rec_test(self, expression: Expression, *vars: bool) -> bool:
        sub1 = None
        sub2 = None
        if expression.type == "EXP":
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return expression.syntax.test(sub1, sub2)
        elif expression.type == "WFF":
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return sub1
        elif expression.type == "NOT":
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]
            
            return expression.syntax.test(sub2)
    
    def substitute(self, *vars) -> list:
        global gSUB
        print("\n" + " " * gSUB + "Theorem:", self.name + ", Substituting")
        gSUB += 2

        checkList = []
        retList = []
        print("\n" + " " * gSUB + "Hypotheses:")
        for i in self.operations:
            if not isinstance(i, Expression):
                break
            checkList.append(i)
            retList.append(self.rec_sub(i, *vars))
            print(" " * gSUB + "⊢", str(retList[-1]))
        
        if isinstance(self.operations[-1], Expression):
            print(" " * gSUB + "Assertion: ⊢", self.rec_sub(self.assertion, *vars))
        
            gSUB -= 2
            print(" " * gSUB + "-" * (30 - gSUB))
            return self.rec_sub(self.assertion, *vars)

        print("\n" + " " * gSUB + "Steps:")
        for i in self.operations:
            if not any(isinstance(t, list) for t in self.operations):
                break
            if not isinstance(i, list):
                continue
            if not isinstance(i[1], Expression):
                i[1] = retList[i[1] - 1].var1
            checkList.append(i)

            sub1 = self.rec_sub(i[1].var1, *vars) if i[1].var1.id >= len(vars) else vars[i[1].var1.id]
            sub2 = self.rec_sub(i[1].var2, *vars) if i[1].var2.id >= len(vars) else vars[i[1].var2.id]
            retList.append(i[0].substitute(sub1, sub2))
            
            print(" " * gSUB + "Result: ⊢", str(retList[-1]))
                
        print("\n" + " " * gSUB + "Assertion: ⊢", self.rec_sub(self.assertion, *vars))
        
        gSUB -= 2
        print(" " * gSUB + "-" * (30 - gSUB))
        return self.rec_sub(self.assertion, *vars)

    def test(self, *vars):
        global gSUB
        print("\n" + " " * gSUB + "Theorem:", self.name + ", Testing")
        gSUB += 2

        checkList = []
        retList = []
        print("\n" + " " * gSUB + "Hypotheses:")
        for i in self.operations:
            if not isinstance(i, Expression):
                break
            checkList.append(i)
            retList.append(self.rec_test(i, *vars))
            print(" " * gSUB + "⊢", i, " : ", str(retList[-1]))
            if not retList[-1]:
                print("Assertion: False")
                return
            
        if isinstance(self.operations[-1], Expression):
            print(" " * gSUB + "Assertion:", self.rec_test(self.assertion, *vars))

            gSUB -= 2
            print(" " * gSUB + "-" * (30 - gSUB))
            return self.rec_test(self.assertion, *vars)
        
        print("\n" + " " * gSUB + "Steps:")
        for i in self.operations:
            if not any(isinstance(t, list) for t in self.operations):
                break
            if not isinstance(i, list):
                continue
            if not isinstance(i[1], Expression):
                i[1] = retList[i[1] - 1].var1
            checkList.append(i)

            sub1 = self.rec_test(i[1].var1, *vars) if i[1].var1.id >= len(vars) else vars[i[1].var1.id]
            sub2 = self.rec_test(i[1].var2, *vars) if i[1].var2.id >= len(vars) else vars[i[1].var2.id]
            retList.append(i[0].test(sub1, sub2))
            
            print(" " * gSUB + "Result: ⊢", str(retList[-1]))
                
        print("\n" + " " * gSUB + "Assertion: ⊢", self.rec_test(self.assertion, *vars))
        
        gSUB -= 2
        print(" " * gSUB + "-" * (30 - gSUB))
        return self.rec_test(self.assertion, *vars)