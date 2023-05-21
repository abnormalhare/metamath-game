import copy
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

clear()

# GLOBAL VARIABLES #
gWFFID = 0

# CLASSES #
class WFF:
    def __init__(self, name: str) -> None:
        global gWFFID
        self.name = name
        self.id = gWFFID
        gWFFID += 1
    
    def __str__(self) -> str:
        return self.name

phi = WFF("𝜑")
psi = WFF("𝜓")
chi = WFF("𝜒")
theta = WFF("𝜃")

class Syntax:
    def __init__(self, symbol: str, func: callable) -> None:
        self.symbol = symbol
        self.test = func

wi = Syntax("→", lambda var1, var2=None: var1 <= var2)

class Expression:
    def __init__(self, var1, syntax: Syntax=None, var2=None) -> None:
        self.var1 = var1
        self.syntax = syntax
        self.var2 = var2
        self.id = var1.id * gWFFID * 2
        try:
            self.id += var2.id * gWFFID * 3
        except:
            self.id += gWFFID * 3
    
    def __str__(self) -> str:
        try:
            return f"({self.var1} {self.syntax.symbol} {self.var2})"
        except:
            return f"{self.var1}"
    
    def substitute(self, var1, var2=None) -> list:
        if isinstance(self.var1, Expression):
            var1 = self.var1.substitute(var1, var2)
        if isinstance(self.var2, Expression):
            var2 = self.var2.substitute(var1, var2)
        return Expression(var1, self.syntax, var2)
    
    def test(self, var1: bool, var2: bool=None) -> bool:
        if self.syntax is None:
            return var1
        if isinstance(self.var1, Expression):
            var1 = self.var1.test(var1, var2)
        if isinstance(self.var2, Expression):
            var2 = self.var2.test(var1, var2)
        return self.syntax.test(var1, var2)

class Axiom:
    def __init__(self, name, *expressions) -> None:
        self.name = name
        self.expressions = expressions

    def rec_sub(self, expression, *vars) -> list:
        sub1 = None
        sub2 = None
        try:
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return Expression(sub1, expression.syntax, sub2)
        except:
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return expression.substitute(sub1)
        
    def rec_test(self, expression, *vars):
        sub1 = None
        sub2 = None
        try:
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return expression.syntax.test(sub1, sub2)
        except:
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return sub1
    
    def substitute(self, *vars) -> list:
        checkList = []
        retList = []
        print()
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_sub(i, *vars))
            print("wff", str(retList[-1]))

    def test(self, *vars):
        checkList = []
        retList = []
        print()
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_test(i, *vars))
            print("wff", i, " : ", str(retList[-1]))

class Theorem:
    def __init__(self, name, assertion, *expressions) -> None:
        self.name = name
        self.assertion = assertion
        self.expressions = expressions
    
    def rec_sub(self, expression, *vars) -> list:
        sub1 = None
        sub2 = None
        try:
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]

            if isinstance(expression.var2, Expression): sub2 = self.rec_sub(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return Expression(sub1, expression.syntax, sub2)
        except:
            if isinstance(expression.var1, Expression): sub1 = self.rec_sub(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return expression.substitute(sub1)
        
    def rec_test(self, expression, *vars):
        sub1 = None
        sub2 = None
        try:
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            if isinstance(expression.var2, Expression): sub2 = self.rec_test(expression.var2, *vars)
            else: sub2 = vars[expression.var2.id]

            return expression.syntax.test(sub1, sub2)
        except:
            if isinstance(expression.var1, Expression): sub1 = self.rec_test(expression.var1, *vars)
            else: sub1 = vars[expression.var1.id]
            
            return sub1
    
    def substitute(self, *vars) -> list:
        checkList = []
        retList = []
        print("\nHypotheses:")
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_sub(i, *vars))
            print("⊢", str(retList[-1]))
        print("Assertion:", self.rec_sub(self.assertion, *vars))

    def test(self, *vars):
        checkList = []
        retList = []
        print()
        for i in self.expressions:
            checkList.append(i)
            retList.append(self.rec_test(i, *vars))
            print("⊢", i, " : ", str(retList[-1]))
            if not retList[-1]:
                print("Assertion: False")
                return
        print("Assertion:", self.rec_test(self.assertion, *vars))
            


a1ii_1 = Expression(phi)
a1ii_2 = Expression(psi)
a1ii = Theorem("a1ii", Expression(phi), a1ii_1, a1ii_2)

a1ii.substitute(phi, psi)

ax_mp_min = Expression(phi)
ax_mp_maj = Expression(phi, wi, psi)
ax_mp = Theorem("Modus Ponens", Expression(psi), ax_mp_min, ax_mp_maj)

ax_mp.substitute(phi, psi)
ax_mp.test(True, True)

ax_1_wph = Expression(phi)
ax_1_wps = Expression(psi)
ax_1_3 = Expression(ax_1_wps, wi, ax_1_wph)
ax_1_4 = Expression(ax_1_wph, wi, ax_1_3)
ax_1 = Axiom("ax-1", ax_1_wph, ax_1_wps, ax_1_3, ax_1_4)

ax_1.substitute(phi, psi)
ax_1.test(True, True)