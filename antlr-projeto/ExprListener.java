// Generated from Expr.g4 by ANTLR 4.13.0
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ExprParser}.
 */
public interface ExprListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ExprParser#root}.
	 * @param ctx the parse tree
	 */
	void enterRoot(ExprParser.RootContext ctx);
	/**
	 * Exit a parse tree produced by {@link ExprParser#root}.
	 * @param ctx the parse tree
	 */
	void exitRoot(ExprParser.RootContext ctx);
	/**
	 * Enter a parse tree produced by the {@code AbsExpr}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAbsExpr(ExprParser.AbsExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code AbsExpr}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAbsExpr(ExprParser.AbsExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FactExpr}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterFactExpr(ExprParser.FactExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FactExpr}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitFactExpr(ExprParser.FactExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Number}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumber(ExprParser.NumberContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Number}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumber(ExprParser.NumberContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Pot}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterPot(ExprParser.PotContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Pot}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitPot(ExprParser.PotContext ctx);
	/**
	 * Enter a parse tree produced by the {@code Parent}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParent(ExprParser.ParentContext ctx);
	/**
	 * Exit a parse tree produced by the {@code Parent}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParent(ExprParser.ParentContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SomaSub}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterSomaSub(ExprParser.SomaSubContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SomaSub}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitSomaSub(ExprParser.SomaSubContext ctx);
	/**
	 * Enter a parse tree produced by the {@code MultDiv}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMultDiv(ExprParser.MultDivContext ctx);
	/**
	 * Exit a parse tree produced by the {@code MultDiv}
	 * labeled alternative in {@link ExprParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMultDiv(ExprParser.MultDivContext ctx);
	/**
	 * Enter a parse tree produced by {@link ExprParser#abs_}.
	 * @param ctx the parse tree
	 */
	void enterAbs_(ExprParser.Abs_Context ctx);
	/**
	 * Exit a parse tree produced by {@link ExprParser#abs_}.
	 * @param ctx the parse tree
	 */
	void exitAbs_(ExprParser.Abs_Context ctx);
	/**
	 * Enter a parse tree produced by {@link ExprParser#fact}.
	 * @param ctx the parse tree
	 */
	void enterFact(ExprParser.FactContext ctx);
	/**
	 * Exit a parse tree produced by {@link ExprParser#fact}.
	 * @param ctx the parse tree
	 */
	void exitFact(ExprParser.FactContext ctx);
}