# Generated from EsJS.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .EsJSParser import EsJSParser
else:
    from EsJSParser import EsJSParser

# This class defines a complete listener for a parse tree produced by EsJSParser.
class EsJSListener(ParseTreeListener):

    # Enter a parse tree produced by EsJSParser#programa.
    def enterPrograma(self, ctx:EsJSParser.ProgramaContext):
        pass

    # Exit a parse tree produced by EsJSParser#programa.
    def exitPrograma(self, ctx:EsJSParser.ProgramaContext):
        pass


    # Enter a parse tree produced by EsJSParser#stmt.
    def enterStmt(self, ctx:EsJSParser.StmtContext):
        pass

    # Exit a parse tree produced by EsJSParser#stmt.
    def exitStmt(self, ctx:EsJSParser.StmtContext):
        pass


    # Enter a parse tree produced by EsJSParser#declKeyword.
    def enterDeclKeyword(self, ctx:EsJSParser.DeclKeywordContext):
        pass

    # Exit a parse tree produced by EsJSParser#declKeyword.
    def exitDeclKeyword(self, ctx:EsJSParser.DeclKeywordContext):
        pass


    # Enter a parse tree produced by EsJSParser#declList.
    def enterDeclList(self, ctx:EsJSParser.DeclListContext):
        pass

    # Exit a parse tree produced by EsJSParser#declList.
    def exitDeclList(self, ctx:EsJSParser.DeclListContext):
        pass


    # Enter a parse tree produced by EsJSParser#declInit.
    def enterDeclInit(self, ctx:EsJSParser.DeclInitContext):
        pass

    # Exit a parse tree produced by EsJSParser#declInit.
    def exitDeclInit(self, ctx:EsJSParser.DeclInitContext):
        pass


    # Enter a parse tree produced by EsJSParser#sinoOpt.
    def enterSinoOpt(self, ctx:EsJSParser.SinoOptContext):
        pass

    # Exit a parse tree produced by EsJSParser#sinoOpt.
    def exitSinoOpt(self, ctx:EsJSParser.SinoOptContext):
        pass


    # Enter a parse tree produced by EsJSParser#sinoTail.
    def enterSinoTail(self, ctx:EsJSParser.SinoTailContext):
        pass

    # Exit a parse tree produced by EsJSParser#sinoTail.
    def exitSinoTail(self, ctx:EsJSParser.SinoTailContext):
        pass


    # Enter a parse tree produced by EsJSParser#blockStmt.
    def enterBlockStmt(self, ctx:EsJSParser.BlockStmtContext):
        pass

    # Exit a parse tree produced by EsJSParser#blockStmt.
    def exitBlockStmt(self, ctx:EsJSParser.BlockStmtContext):
        pass


    # Enter a parse tree produced by EsJSParser#paraInit.
    def enterParaInit(self, ctx:EsJSParser.ParaInitContext):
        pass

    # Exit a parse tree produced by EsJSParser#paraInit.
    def exitParaInit(self, ctx:EsJSParser.ParaInitContext):
        pass


    # Enter a parse tree produced by EsJSParser#casoList.
    def enterCasoList(self, ctx:EsJSParser.CasoListContext):
        pass

    # Exit a parse tree produced by EsJSParser#casoList.
    def exitCasoList(self, ctx:EsJSParser.CasoListContext):
        pass


    # Enter a parse tree produced by EsJSParser#exprOCrear.
    def enterExprOCrear(self, ctx:EsJSParser.ExprOCrearContext):
        pass

    # Exit a parse tree produced by EsJSParser#exprOCrear.
    def exitExprOCrear(self, ctx:EsJSParser.ExprOCrearContext):
        pass


    # Enter a parse tree produced by EsJSParser#crearType.
    def enterCrearType(self, ctx:EsJSParser.CrearTypeContext):
        pass

    # Exit a parse tree produced by EsJSParser#crearType.
    def exitCrearType(self, ctx:EsJSParser.CrearTypeContext):
        pass


    # Enter a parse tree produced by EsJSParser#expr.
    def enterExpr(self, ctx:EsJSParser.ExprContext):
        pass

    # Exit a parse tree produced by EsJSParser#expr.
    def exitExpr(self, ctx:EsJSParser.ExprContext):
        pass


    # Enter a parse tree produced by EsJSParser#factor.
    def enterFactor(self, ctx:EsJSParser.FactorContext):
        pass

    # Exit a parse tree produced by EsJSParser#factor.
    def exitFactor(self, ctx:EsJSParser.FactorContext):
        pass


    # Enter a parse tree produced by EsJSParser#arrowBody.
    def enterArrowBody(self, ctx:EsJSParser.ArrowBodyContext):
        pass

    # Exit a parse tree produced by EsJSParser#arrowBody.
    def exitArrowBody(self, ctx:EsJSParser.ArrowBodyContext):
        pass


    # Enter a parse tree produced by EsJSParser#consolaCall.
    def enterConsolaCall(self, ctx:EsJSParser.ConsolaCallContext):
        pass

    # Exit a parse tree produced by EsJSParser#consolaCall.
    def exitConsolaCall(self, ctx:EsJSParser.ConsolaCallContext):
        pass


    # Enter a parse tree produced by EsJSParser#consolaMethod.
    def enterConsolaMethod(self, ctx:EsJSParser.ConsolaMethodContext):
        pass

    # Exit a parse tree produced by EsJSParser#consolaMethod.
    def exitConsolaMethod(self, ctx:EsJSParser.ConsolaMethodContext):
        pass


    # Enter a parse tree produced by EsJSParser#paramsOpt.
    def enterParamsOpt(self, ctx:EsJSParser.ParamsOptContext):
        pass

    # Exit a parse tree produced by EsJSParser#paramsOpt.
    def exitParamsOpt(self, ctx:EsJSParser.ParamsOptContext):
        pass


    # Enter a parse tree produced by EsJSParser#argsOpt.
    def enterArgsOpt(self, ctx:EsJSParser.ArgsOptContext):
        pass

    # Exit a parse tree produced by EsJSParser#argsOpt.
    def exitArgsOpt(self, ctx:EsJSParser.ArgsOptContext):
        pass


    # Enter a parse tree produced by EsJSParser#arrayArgsOpt.
    def enterArrayArgsOpt(self, ctx:EsJSParser.ArrayArgsOptContext):
        pass

    # Exit a parse tree produced by EsJSParser#arrayArgsOpt.
    def exitArrayArgsOpt(self, ctx:EsJSParser.ArrayArgsOptContext):
        pass


    # Enter a parse tree produced by EsJSParser#objElements.
    def enterObjElements(self, ctx:EsJSParser.ObjElementsContext):
        pass

    # Exit a parse tree produced by EsJSParser#objElements.
    def exitObjElements(self, ctx:EsJSParser.ObjElementsContext):
        pass


    # Enter a parse tree produced by EsJSParser#objProp.
    def enterObjProp(self, ctx:EsJSParser.ObjPropContext):
        pass

    # Exit a parse tree produced by EsJSParser#objProp.
    def exitObjProp(self, ctx:EsJSParser.ObjPropContext):
        pass



del EsJSParser