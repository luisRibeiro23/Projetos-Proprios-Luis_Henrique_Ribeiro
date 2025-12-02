# ExprEvalVisitor.py
from ExprVisitor import ExprVisitor
import math

class ExprEvalVisitor(ExprVisitor):
    def visitRoot(self, ctx):
        return self.visit(ctx.expr())

    def visitParent(self, ctx):
        return self.visit(ctx.expr())

    def visitNumber(self, ctx):
        return float(ctx.getText())

    def visitSomaSub(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        return left + right if op == '+' else left - right

    def visitMultDiv(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        op = ctx.getChild(1).getText()
        return left * right if op == '*' else left / right

    def visitPot(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return math.pow(left, right)

    def visitAbsExpr(self, ctx):
        value = self.visit(ctx.expr())
        return abs(value)

    def visitFactExpr(self, ctx):
        value = self.visit(ctx.expr())
        return math.factorial(int(value))
