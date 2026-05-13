from EsJSVisitor import EsJSVisitor
import sys

class BreakException(Exception): pass
class ContinueException(Exception): pass

NULO      = object()  # sentinel for nulo
INDEFINIDO = object() # sentinel for indefinido

class Interpreter(EsJSVisitor):

    def __init__(self):
        # Entorno de variables: pila de diccionarios (scopes)
        self.scopes = [{}]

    # ── Manejo de scopes ─────────────────────────────────────
    def push_scope(self):
        self.scopes.append({})

    def pop_scope(self):
        self.scopes.pop()

    def get_var(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise NameError(f"Variable no definida: {name}")

    def set_var(self, name, value):
        # Busca en scopes existentes primero
        for scope in reversed(self.scopes):
            if name in scope:
                scope[name] = value
                return
        # Si no existe, asigna en el scope actual
        self.scopes[-1][name] = value

    def declare_var(self, name, value):
        # Declara siempre en el scope actual
        self.scopes[-1][name] = value

    # ── Punto de entrada ─────────────────────────────────────
    def visitPrograma(self, ctx):
        for stmt in ctx.stmt():
            self.visit(stmt)

    # ── Statements ───────────────────────────────────────────
    def visitStmt(self, ctx):
        first = ctx.getChild(0)
        if first is not None:
            text = first.getText()
            if text == 'romper':
                raise BreakException()
            if text == 'continuar':
                raise ContinueException()
            if text == 'elegir':
                return self.visitElegir(ctx)
            if text == 'para':
                return self.visitPara(ctx)
            if text == 'si':
                return self.visitSi(ctx)
            if text == 'mientras':
                return self.visitMientras(ctx)
        return self.visitChildren(ctx)

    # ── Declaraciones ────────────────────────────────────────

    def visitDeclList(self, ctx):
        # ctx.ID() puede ser lista cuando hay 'mut a = 1, b = 2'
        for i, id_node in enumerate(ctx.ID()):
            name = id_node.getText()
            init_nodes = ctx.declInit()
            value = None
            if i < len(init_nodes):
                value = self.visit(init_nodes[i])
            self.declare_var(name, value)

    def visitDeclInit(self, ctx):
        if ctx.exprOCrear():
            return self.visit(ctx.exprOCrear())
        return None
    
    def visitExprOCrear(self, ctx):
        return self.visit(ctx.expr())

    # ── Expresiones ──────────────────────────────────────────
    def visitExprAritmetica(self, ctx):
        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        if op == '+':
            if isinstance(left, str) or isinstance(right, str):
                return js_str(left) + js_str(right)
            return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left / right
        if op == '%': return left % right

    def visitExprIgualdad(self, ctx):
        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        if op == '==':   return self._js_eq(left, right)
        if op == '===':  return left is right if (left is NULO or left is INDEFINIDO) else left == right and type(left) == type(right)
        if op == '!=':   return not self._js_eq(left, right)
        if op == '!==':  return not (left == right and type(left) == type(right))

    def visitExprRelacional(self, ctx):
        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        if op == '<':  return left < right
        if op == '>':  return left > right
        if op == '<=': return left <= right
        if op == '>=': return left >= right

    def visitExprLogica(self, ctx):
        left = self.visit(ctx.expr(0))
        op   = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        if op == '&&': return left and right
        if op == '||': return left or right

    def visitExprFactor(self, ctx):
        return self.visit(ctx.factor())

    def visitFactorId(self, ctx):
        return self.get_var(ctx.ID().getText())

    def visitFactorNumero(self, ctx):
        text = ctx.NUMBER().getText()
        return float(text) if '.' in text else int(text)

    def visitFactorString(self, ctx):
        return ctx.STRING().getText()[1:-1]

    def visitFactorVerdadero(self, ctx):  return True
    def visitFactorFalso(self, ctx):      return False
    def visitFactorNulo(self, ctx):       return NULO
    def visitFactorIndefinido(self, ctx): return INDEFINIDO
    def visitFactorInfinito(self, ctx):   return float('inf')
    def visitFactorNan(self, ctx):        return float('nan')

    def visitFactorAsignacion(self, ctx):
        # ctx.factor(0) es el lado izquierdo
        # ctx.exprOCrear() es el valor
        op    = ctx.getChild(1).getText()
        value = self.visit(ctx.exprOCrear())
        name  = ctx.getChild(0).getText()  # simplificado por ahora
        if op == '=':   self.set_var(name, value)
        if op == '+=':
            current = self.get_var(name)
            value = str(current) + str(value) if isinstance(current, str) else current + value
            self.set_var(name, value)
        return value

    # ── Consola ──────────────────────────────────────────────
    def visitConsolaCall(self, ctx):
        method = ctx.consolaMethod().getText()
        args = []
        if ctx.argsOpt():
            args = self.visit(ctx.argsOpt())

        if method == 'escribir':
            print(*args)
        elif method == 'error':
            print("ERROR:", *args, file=sys.stderr)
        elif method == 'limpiar':
            pass  # ignorar por ahora

    def visitArgsOpt(self, ctx):
        return [self.visit(e) for e in ctx.expr()]

    # ── Reglas auxiliares ────────────────────────────────────
    def visitDeclKeyword(self, ctx): pass
    def visitConsolaMethod(self, ctx): pass
    def visitSinoOpt(self, ctx): pass
    def visitParamsOpt(self, ctx): pass
    def visitElegir(self, ctx):
        # stmt children: elegir ( expr ) { casoList }
        value = self.visit(ctx.getChild(2))  # the switch expr, not ctx.expr()
        caso_list = ctx.casoList()
        children = [caso_list.getChild(i) for i in range(caso_list.getChildCount())]

        matched = False
        i = 0
        while i < len(children):
            text = children[i].getText()
            if text == 'caso':
                i += 1
                case_val = self.visit(children[i])  # expr
                i += 1  # skip expr
                i += 1  # skip ':'
                if case_val == value:
                    matched = True
                while i < len(children) and children[i].getText() not in ('caso', 'porDefecto'):
                    if matched:
                        try:
                            self.visit(children[i])
                        except BreakException:
                            return
                    i += 1
            elif text == 'porDefecto':
                i += 1  # skip ':'
                if not matched:
                    while i < len(children):
                        try:
                            self.visit(children[i])
                        except BreakException:
                            return
                        i += 1
                return
            else:
                i += 1

    def visitCasoList(self, ctx):
        pass  # handled entirely by visitElegir

    def visitPara(self, ctx):
        self.push_scope()
        self.visit(ctx.getChild(2))      # paraInit
        cond_expr   = ctx.getChild(4)
        update_expr = ctx.getChild(6)
        block       = ctx.getChild(8)
        while True:
            cond = self.visit(cond_expr)
            if not cond:
                break
            try:
                self.visit(block)
            except BreakException:
                break
            except ContinueException:
                pass
            self.visit(update_expr)
        self.pop_scope()

    def visitParaInit(self, ctx):
        if ctx.declKeyword() and ctx.declList():
            self.visit(ctx.declList())   # declares i=0 in pushed scope
        elif ctx.expr():
            self.visit(ctx.expr())
            
    def visitRomper(self, ctx):    # if you have a labeled rule; otherwise handle in visitStmt
        raise BreakException()

    def visitContinuar(self, ctx):
        raise ContinueException()
    
    def visitSi(self, ctx):
        cond = self.visit(ctx.getChild(2))
        if cond:
            self.visit(ctx.getChild(4))
        else:
            self.visit(ctx.sinoOpt())

    def visitSino(self, ctx):
        self.visit(ctx.getChild(2))
    
    def visitMientras(self, ctx):
        # stmt children: mientras ( expr ) blockStmt
        while True:
            cond = self.visit(ctx.getChild(2))
            if not cond:
                break
            try:
                self.visit(ctx.getChild(4))
            except BreakException:
                break
            except ContinueException:
                pass    
    
    def visitFactorPrefijo(self, ctx):
        op  = ctx.getChild(0).getText()
        val = self.visit(ctx.factor())
        if op == '!':  return not val
        if op == '-':  return -val
        if op == '+':  return +val
    
    def visitFactorGrupo(self, ctx):
        # ( argsOpt ) — but used as grouping, single expr inside
        args = self.visit(ctx.argsOpt())
        return args[0] if args else None

    def _js_eq(self, left, right):
        if (left is NULO or left is INDEFINIDO) and (right is NULO or right is INDEFINIDO):
            return True
        return left == right

def js_str(val):
    if val is True:       return 'true'
    if val is False:      return 'false'
    if val is NULO:       return 'nulo'
    if val is INDEFINIDO: return 'indefinido'
    if val == float('inf'): return 'Infinito'
    return str(val)

