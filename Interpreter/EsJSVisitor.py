# Generated from EsJS.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EsJSParser import EsJSParser
else:
    from EsJSParser import EsJSParser

# This class defines a complete generic visitor for a parse tree produced by EsJSParser.

class EsJSVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EsJSParser#programa.
    def visitPrograma(self, ctx:EsJSParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#stmt.
    def visitStmt(self, ctx:EsJSParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#declKeyword.
    def visitDeclKeyword(self, ctx:EsJSParser.DeclKeywordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#declList.
    def visitDeclList(self, ctx:EsJSParser.DeclListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#declInit.
    def visitDeclInit(self, ctx:EsJSParser.DeclInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#sinoOpt.
    def visitSinoOpt(self, ctx:EsJSParser.SinoOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#sinoTail.
    def visitSinoTail(self, ctx:EsJSParser.SinoTailContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#blockStmt.
    def visitBlockStmt(self, ctx:EsJSParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#paraInit.
    def visitParaInit(self, ctx:EsJSParser.ParaInitContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#casoList.
    def visitCasoList(self, ctx:EsJSParser.CasoListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprOCrear.
    def visitExprOCrear(self, ctx:EsJSParser.ExprOCrearContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#crearType.
    def visitCrearType(self, ctx:EsJSParser.CrearTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#expr.
    def visitExpr(self, ctx:EsJSParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factor.
    def visitFactor(self, ctx:EsJSParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#arrowBody.
    def visitArrowBody(self, ctx:EsJSParser.ArrowBodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#consolaCall.
    def visitConsolaCall(self, ctx:EsJSParser.ConsolaCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#consolaMethod.
    def visitConsolaMethod(self, ctx:EsJSParser.ConsolaMethodContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#paramsOpt.
    def visitParamsOpt(self, ctx:EsJSParser.ParamsOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#argsOpt.
    def visitArgsOpt(self, ctx:EsJSParser.ArgsOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#arrayArgsOpt.
    def visitArrayArgsOpt(self, ctx:EsJSParser.ArrayArgsOptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#objElements.
    def visitObjElements(self, ctx:EsJSParser.ObjElementsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#objProp.
    def visitObjProp(self, ctx:EsJSParser.ObjPropContext):
        return self.visitChildren(ctx)



del EsJSParser