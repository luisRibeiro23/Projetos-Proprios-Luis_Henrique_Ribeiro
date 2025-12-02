import java.util.Stack;

public class ExprEvalListener extends ExprBaseListener {

    private Stack<Double> stack = new Stack<>();

    public double getResult() {
        return stack.peek();
    }

    @Override
    public void exitNumber(ExprParser.NumberContext ctx) {
        double value = Double.parseDouble(ctx.getText());
        stack.push(value);
    }

    @Override
    public void exitParent(ExprParser.ParentContext ctx) {
        // O valor da expressão entre parênteses já está na pilha
    }

    @Override
    public void exitSomaSub(ExprParser.SomaSubContext ctx) {
        double right = stack.pop();
        double left = stack.pop();
        if (ctx.getChild(1).getText().equals("+")) {
            stack.push(left + right);
        } else {
            stack.push(left - right);
        }
    }

    @Override
    public void exitMultDiv(ExprParser.MultDivContext ctx) {
        double right = stack.pop();
        double left = stack.pop();
        if (ctx.getChild(1).getText().equals("*")) {
            stack.push(left * right);
        } else {
            stack.push(left / right);
        }
    }

    @Override
    public void exitPot(ExprParser.PotContext ctx) {
        double right = stack.pop();
        double left = stack.pop();
        stack.push(Math.pow(left, right));
    }

    @Override
    public void exitAbsExpr(ExprParser.AbsExprContext ctx) {
        double val = stack.pop();
        stack.push(Math.abs(val));
    }

    @Override
    public void exitFactExpr(ExprParser.FactExprContext ctx) {
        double val = stack.pop();
        int intVal = (int) val;
        double result = 1;
        for (int i = 2; i <= intVal; i++) {
            result *= i;
        }
        stack.push(result);
    }
}
