import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.tree.*;

public class Main {
    public static void main(String[] args) throws Exception {
        String input = args.length > 0 ? args[0] : "fat(3 + 2)";
        CharStream cs = CharStreams.fromString(input);
        ExprLexer lexer = new ExprLexer(cs);
        CommonTokenStream tokens = new CommonTokenStream(lexer);
        ExprParser parser = new ExprParser(tokens);

        ParseTree tree = parser.root();

        ParseTreeWalker walker = new ParseTreeWalker();
        ExprEvalListener listener = new ExprEvalListener();
        walker.walk(listener, tree);

        System.out.println("Resultado: " + listener.getResult());
    }
}
