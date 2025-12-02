from ExprListener import ExprListener
import math

class ExprEvalListener(ExprListener):
    def __init__(self):
        self.stack = []

    def exitNumber(self, ctx):
        value = float(ctx.getText())
        self.stack.append(value)

    def exitParent(self, ctx):
        # Valor já processado
        pass

    def exitSomaSub(self, ctx):
        right = self.stack.pop()
        left = self.stack.pop()
        op = ctx.getChild(1).getText()
        self.stack.append(left + right if op == '+' else left - right)

    def exitMultDiv(self, ctx):
        right = self.stack.pop()
        left = self.stack.pop()
        op = ctx.getChild(1).getText()
        self.stack.append(left * right if op == '*' else left / right)

    def exitPot(self, ctx):
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(math.pow(left, right))

    def exitAbsExpr(self, ctx):
        val = self.stack.pop()
        self.stack.append(abs(val))

    def exitFactExpr(self, ctx):
        val = self.stack.pop()
        self.stack.append(math.factorial(int(val)))
