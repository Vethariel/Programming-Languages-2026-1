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


    # Visit a parse tree produced by EsJSParser#exprAritmetica.
    def visitExprAritmetica(self, ctx:EsJSParser.ExprAritmeticaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprFactor.
    def visitExprFactor(self, ctx:EsJSParser.ExprFactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprRelacional.
    def visitExprRelacional(self, ctx:EsJSParser.ExprRelacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprIgualdad.
    def visitExprIgualdad(self, ctx:EsJSParser.ExprIgualdadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprTernario.
    def visitExprTernario(self, ctx:EsJSParser.ExprTernarioContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#exprLogica.
    def visitExprLogica(self, ctx:EsJSParser.ExprLogicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorAcceso.
    def visitFactorAcceso(self, ctx:EsJSParser.FactorAccesoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorArregloBuiltin.
    def visitFactorArregloBuiltin(self, ctx:EsJSParser.FactorArregloBuiltinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorFalso.
    def visitFactorFalso(self, ctx:EsJSParser.FactorFalsoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorVerdadero.
    def visitFactorVerdadero(self, ctx:EsJSParser.FactorVerdaderoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorNulo.
    def visitFactorNulo(self, ctx:EsJSParser.FactorNuloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorMatrizBuiltin.
    def visitFactorMatrizBuiltin(self, ctx:EsJSParser.FactorMatrizBuiltinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorArreglo.
    def visitFactorArreglo(self, ctx:EsJSParser.FactorArregloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorCadenaBuiltin.
    def visitFactorCadenaBuiltin(self, ctx:EsJSParser.FactorCadenaBuiltinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorMate.
    def visitFactorMate(self, ctx:EsJSParser.FactorMateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorFlecha.
    def visitFactorFlecha(self, ctx:EsJSParser.FactorFlechaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorInfinito.
    def visitFactorInfinito(self, ctx:EsJSParser.FactorInfinitoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorObjeto.
    def visitFactorObjeto(self, ctx:EsJSParser.FactorObjetoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorAsignacion.
    def visitFactorAsignacion(self, ctx:EsJSParser.FactorAsignacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorIndice.
    def visitFactorIndice(self, ctx:EsJSParser.FactorIndiceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorNan.
    def visitFactorNan(self, ctx:EsJSParser.FactorNanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorIndefinido.
    def visitFactorIndefinido(self, ctx:EsJSParser.FactorIndefinidoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorId.
    def visitFactorId(self, ctx:EsJSParser.FactorIdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorNumeroBuiltin.
    def visitFactorNumeroBuiltin(self, ctx:EsJSParser.FactorNumeroBuiltinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorAmbiente.
    def visitFactorAmbiente(self, ctx:EsJSParser.FactorAmbienteContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorPrefijo.
    def visitFactorPrefijo(self, ctx:EsJSParser.FactorPrefijoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorNumero.
    def visitFactorNumero(self, ctx:EsJSParser.FactorNumeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorGrupo.
    def visitFactorGrupo(self, ctx:EsJSParser.FactorGrupoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorString.
    def visitFactorString(self, ctx:EsJSParser.FactorStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorBooleanoBuiltin.
    def visitFactorBooleanoBuiltin(self, ctx:EsJSParser.FactorBooleanoBuiltinContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorPostfijo.
    def visitFactorPostfijo(self, ctx:EsJSParser.FactorPostfijoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EsJSParser#factorLlamada.
    def visitFactorLlamada(self, ctx:EsJSParser.FactorLlamadaContext):
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