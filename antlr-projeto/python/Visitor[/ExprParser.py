# Generated from Expr.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,11,49,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,1,0,1,0,1,0,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,1,3,1,20,8,1,1,1,3,1,23,8,1,1,1,1,1,1,1,1,1,
        1,1,1,1,1,1,1,1,1,1,5,1,34,8,1,10,1,12,1,37,9,1,1,2,1,2,1,2,1,2,
        1,2,1,3,1,3,1,3,1,3,1,3,1,3,0,1,2,4,0,2,4,6,0,2,1,0,4,5,1,0,6,7,
        51,0,8,1,0,0,0,2,22,1,0,0,0,4,38,1,0,0,0,6,43,1,0,0,0,8,9,3,2,1,
        0,9,10,5,0,0,1,10,1,1,0,0,0,11,12,6,1,-1,0,12,13,5,1,0,0,13,14,3,
        2,1,0,14,15,5,2,0,0,15,23,1,0,0,0,16,23,3,4,2,0,17,23,3,6,3,0,18,
        20,5,7,0,0,19,18,1,0,0,0,19,20,1,0,0,0,20,21,1,0,0,0,21,23,5,10,
        0,0,22,11,1,0,0,0,22,16,1,0,0,0,22,17,1,0,0,0,22,19,1,0,0,0,23,35,
        1,0,0,0,24,25,10,6,0,0,25,26,5,3,0,0,26,34,3,2,1,7,27,28,10,5,0,
        0,28,29,7,0,0,0,29,34,3,2,1,6,30,31,10,4,0,0,31,32,7,1,0,0,32,34,
        3,2,1,5,33,24,1,0,0,0,33,27,1,0,0,0,33,30,1,0,0,0,34,37,1,0,0,0,
        35,33,1,0,0,0,35,36,1,0,0,0,36,3,1,0,0,0,37,35,1,0,0,0,38,39,5,8,
        0,0,39,40,5,1,0,0,40,41,3,2,1,0,41,42,5,2,0,0,42,5,1,0,0,0,43,44,
        5,9,0,0,44,45,5,1,0,0,45,46,3,2,1,0,46,47,5,2,0,0,47,7,1,0,0,0,4,
        19,22,33,35
    ]

class ExprParser ( Parser ):

    grammarFileName = "Expr.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'^'", "'*'", "'/'", "'+'", 
                     "'-'", "'abs'", "'fat'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "NUM", "WS" ]

    RULE_root = 0
    RULE_expr = 1
    RULE_abs_ = 2
    RULE_fact = 3

    ruleNames =  [ "root", "expr", "abs_", "fact" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    NUM=10
    WS=11

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class RootContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ExprParser.ExprContext,0)


        def EOF(self):
            return self.getToken(ExprParser.EOF, 0)

        def getRuleIndex(self):
            return ExprParser.RULE_root

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRoot" ):
                listener.enterRoot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRoot" ):
                listener.exitRoot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRoot" ):
                return visitor.visitRoot(self)
            else:
                return visitor.visitChildren(self)




    def root(self):

        localctx = ExprParser.RootContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_root)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 8
            self.expr(0)
            self.state = 9
            self.match(ExprParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return ExprParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AbsExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def abs_(self):
            return self.getTypedRuleContext(ExprParser.Abs_Context,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbsExpr" ):
                listener.enterAbsExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbsExpr" ):
                listener.exitAbsExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbsExpr" ):
                return visitor.visitAbsExpr(self)
            else:
                return visitor.visitChildren(self)


    class FactExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def fact(self):
            return self.getTypedRuleContext(ExprParser.FactContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactExpr" ):
                listener.enterFactExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactExpr" ):
                listener.exitFactExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactExpr" ):
                return visitor.visitFactExpr(self)
            else:
                return visitor.visitChildren(self)


    class NumberContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUM(self):
            return self.getToken(ExprParser.NUM, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumber" ):
                return visitor.visitNumber(self)
            else:
                return visitor.visitChildren(self)


    class PotContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPot" ):
                listener.enterPot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPot" ):
                listener.exitPot(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPot" ):
                return visitor.visitPot(self)
            else:
                return visitor.visitChildren(self)


    class ParentContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(ExprParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParent" ):
                listener.enterParent(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParent" ):
                listener.exitParent(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParent" ):
                return visitor.visitParent(self)
            else:
                return visitor.visitChildren(self)


    class SomaSubContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSomaSub" ):
                listener.enterSomaSub(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSomaSub" ):
                listener.exitSomaSub(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSomaSub" ):
                return visitor.visitSomaSub(self)
            else:
                return visitor.visitChildren(self)


    class MultDivContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a ExprParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(ExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(ExprParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultDiv" ):
                listener.enterMultDiv(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultDiv" ):
                listener.exitMultDiv(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMultDiv" ):
                return visitor.visitMultDiv(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = ExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 22
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                localctx = ExprParser.ParentContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 12
                self.match(ExprParser.T__0)
                self.state = 13
                self.expr(0)
                self.state = 14
                self.match(ExprParser.T__1)
                pass
            elif token in [8]:
                localctx = ExprParser.AbsExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 16
                self.abs_()
                pass
            elif token in [9]:
                localctx = ExprParser.FactExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 17
                self.fact()
                pass
            elif token in [7, 10]:
                localctx = ExprParser.NumberContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 19
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==7:
                    self.state = 18
                    self.match(ExprParser.T__6)


                self.state = 21
                self.match(ExprParser.NUM)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 35
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 33
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,2,self._ctx)
                    if la_ == 1:
                        localctx = ExprParser.PotContext(self, ExprParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 24
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 25
                        self.match(ExprParser.T__2)
                        self.state = 26
                        self.expr(7)
                        pass

                    elif la_ == 2:
                        localctx = ExprParser.MultDivContext(self, ExprParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 27
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 28
                        _la = self._input.LA(1)
                        if not(_la==4 or _la==5):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 29
                        self.expr(6)
                        pass

                    elif la_ == 3:
                        localctx = ExprParser.SomaSubContext(self, ExprParser.ExprContext(self, _parentctx, _parentState))
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 30
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 31
                        _la = self._input.LA(1)
                        if not(_la==6 or _la==7):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 32
                        self.expr(5)
                        pass

             
                self.state = 37
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class Abs_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ExprParser.ExprContext,0)


        def getRuleIndex(self):
            return ExprParser.RULE_abs_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAbs_" ):
                listener.enterAbs_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAbs_" ):
                listener.exitAbs_(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAbs_" ):
                return visitor.visitAbs_(self)
            else:
                return visitor.visitChildren(self)




    def abs_(self):

        localctx = ExprParser.Abs_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_abs_)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 38
            self.match(ExprParser.T__7)
            self.state = 39
            self.match(ExprParser.T__0)
            self.state = 40
            self.expr(0)
            self.state = 41
            self.match(ExprParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(ExprParser.ExprContext,0)


        def getRuleIndex(self):
            return ExprParser.RULE_fact

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFact" ):
                listener.enterFact(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFact" ):
                listener.exitFact(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFact" ):
                return visitor.visitFact(self)
            else:
                return visitor.visitChildren(self)




    def fact(self):

        localctx = ExprParser.FactContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_fact)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(ExprParser.T__8)
            self.state = 44
            self.match(ExprParser.T__0)
            self.state = 45
            self.expr(0)
            self.state = 46
            self.match(ExprParser.T__1)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 4)
         




