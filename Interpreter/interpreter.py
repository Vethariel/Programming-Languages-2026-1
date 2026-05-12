from EsJSVisitor import EsJSVisitor
import sys

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
        return self.visitChildren(ctx)

    # ── Declaraciones ────────────────────────────────────────
    def visitDeclKeyword(self, ctx):
        return self.visitChildren(ctx)

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
                return str(left) + str(right)
            return left + right
        if op == '-': return left - right
        if op == '*': return left * right
        if op == '/': return left / right
        if op == '%': return left % right

    def visitExprIgualdad(self, ctx):
        left  = self.visit(ctx.expr(0))
        op    = ctx.getChild(1).getText()
        right = self.visit(ctx.expr(1))
        if op == '==':  return left == right
        if op == '===': return left == right and type(left) == type(right)
        if op == '!=':  return left != right
        if op == '!==': return left != right or type(left) != type(right)

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

    def visitFactorLiteral(self, ctx):
        if ctx.VERDADERO(): return True
        if ctx.FALSO():     return False
        if ctx.NULO():      return None
        if ctx.INDEFINIDO():return None
        if ctx.INFINITO():  return float('inf')

    def visitFactorAsignacion(self, ctx):
        # ctx.factor(0) es el lado izquierdo
        # ctx.exprOCrear() es el valor
        op    = ctx.getChild(1).getText()
        value = self.visit(ctx.exprOCrear())
        name  = ctx.factor(0).getText()  # simplificado por ahora
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