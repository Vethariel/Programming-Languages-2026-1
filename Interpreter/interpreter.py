from EsJSVisitor import EsJSVisitor
import sys

class BreakException(Exception): pass
class ContinueException(Exception): pass
class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

# ── Clase para números con métodos de instancia ──────────────
class JSNumber:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return js_str(self.val)

    # Operaciones aritméticas para que funcione con + - * /
    def __add__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return JSNumber(self.val + o)
    def __radd__(self, other): return JSNumber(other + self.val)
    def __sub__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return JSNumber(self.val - o)
    def __rsub__(self, other): return JSNumber(other - self.val)
    def __mul__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return JSNumber(self.val * o)
    def __rmul__(self, other): return JSNumber(other * self.val)
    def __truediv__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return JSNumber(self.val / o)
    def __rtruediv__(self, other): return JSNumber(other / self.val)
    def __eq__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return self.val == o
    def __lt__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return self.val < o
    def __le__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return self.val <= o
    def __gt__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return self.val > o
    def __ge__(self, other):
        o = other.val if isinstance(other, JSNumber) else other
        return self.val >= o

# ── Clase JSObject para manejar ambiente ─────────────────────
class JSObject(dict):
    """Dict con soporte para 'ambiente' (this)."""
    pass

# ── Clase JSArray ─────────────────────────────────────────────
class JSArray(list):
    pass

# ── Objeto Numero builtin ────────────────────────────────────
class NumeroBuiltin:
    POSITIVE_INFINITY = float('inf')

    @staticmethod
    def esFinito(x):
        v = x.val if isinstance(x, JSNumber) else x
        return isinstance(v, (int, float)) and not (v == float('inf') or v != v)

    @staticmethod
    def esEntero(x):
        v = x.val if isinstance(x, JSNumber) else x
        return isinstance(v, (int, float)) and v == int(v)

    @staticmethod
    def esEnteroSeguro(x):
        v = x.val if isinstance(x, JSNumber) else x
        MAX = 2**53 - 1
        return isinstance(v, (int, float)) and v == int(v) and abs(v) <= MAX

    @staticmethod
    def interpretarDecimal(s):
        try:
            return JSNumber(float(str(s)))
        except:
            return JSNumber(float('nan'))

    @staticmethod
    def interpretarEntero(s, base=10):
        try:
            return JSNumber(int(str(s), base))
        except:
            return JSNumber(float('nan'))


# ── Objeto Mate builtin ──────────────────────────────────────
import math
class MateBuiltin:
    PI     = math.pi
    E      = math.e
    LN2    = math.log(2)
    LN10   = math.log(10)
    LOG2E  = math.log2(math.e)
    LOG10E = math.log10(math.e)

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
        # ── Hoisting: pre-scan de funciones y var ────────────────
        self._hoist(ctx.stmt())
        # ── Ejecución normal ─────────────────────────────────────
        for stmt in ctx.stmt():
            self.visit(stmt)

    def _hoist(self, stmts):
        """Pre-declara funciones y variables var en el scope actual."""
        for stmt in stmts:
            first = stmt.getChild(0)
            if first is None:
                continue
            text = first.getText()

            # Hoisting de funciones: declaración completa
            if text == 'funcion':
                self._declare_funcion(stmt)

            # Hoisting de var: declara con indefinido
            elif text == 'var':
                decl_list = stmt.declList()
                if decl_list:
                    for id_node in decl_list.ID():
                        name = id_node.getText()
                        if name not in self.scopes[-1]:
                            self.declare_var(name, INDEFINIDO)

    # ── Statements ───────────────────────────────────────────
    def visitStmt(self, ctx):
        first = ctx.getChild(0)
        if first is not None:
            text = first.getText()
            if text == 'romper':    raise BreakException()
            if text == 'continuar': raise ContinueException()
            if text == 'retornar':  return self.visitRetornar(ctx)
            if text == 'elegir':    return self.visitElegir(ctx)
            if text == 'para':      return self.visitPara(ctx)
            if text == 'si':        return self.visitSi(ctx)
            if text == 'mientras':  return self.visitMientras(ctx)
            if text == 'funcion':   return self._declare_funcion(ctx)
        return self.visitChildren(ctx)

    # ── Declaraciones ────────────────────────────────────────

    def visitDeclList(self, ctx):
        for i, id_node in enumerate(ctx.ID()):
            name = id_node.getText()
            init_nodes = ctx.declInit()
            value = INDEFINIDO
            if i < len(init_nodes):
                v = self.visit(init_nodes[i])
                if v is not None:
                    value = v
            # Si ya existe (hoisted), solo actualiza si tiene valor
            if name in self.scopes[-1] and value is INDEFINIDO:
                continue
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
        op    = ctx.getChild(1).getText()
        value = self.visit(ctx.exprOCrear())
        lhs   = ctx.factor()  # lado izquierdo

        # Caso: obj.prop = val
        if hasattr(lhs, 'PERIOD') or (lhs.getChildCount() >= 3 and lhs.getChild(1).getText() == '.'):
            obj  = self.visit(lhs.factor())
            prop = lhs.ID().getText()
            if op == '=':
                obj[prop] = value
            elif op == '+=':
                obj[prop] = obj[prop] + value
            return value

        # Caso: simple ID
        name = lhs.getText()
        if op == '=':
            self.set_var(name, value)
        elif op == '+=':
            current = self.get_var(name)
            value = js_str(current) + js_str(value) if isinstance(current, str) else current + value
            self.set_var(name, value)
        return value

    # ── Objetos literales ─────────────────────────────────────────
    def visitFactorObjeto(self, ctx):
        obj = JSObject()
        for prop in (ctx.objElements().objProp() if ctx.objElements() else []):
            name = prop.ID().getText()
            if prop.blockStmt():
                params = []
                if prop.paramsOpt() and prop.paramsOpt().ID():
                    params = [p.getText() for p in prop.paramsOpt().ID()]
                block = prop.blockStmt()
                obj[name] = self._make_method(params, block, obj)
            else:
                obj[name] = self.visit(prop.expr())
        return obj

    def _make_method(self, params, block, obj_ref):
        """Crea un callable que ejecuta block con ambiente=obj_ref."""
        captured = [dict(s) for s in self.scopes]
        def method(*args):
            saved = self.scopes
            self.scopes = [dict(s) for s in captured]
            self.push_scope()
            self.declare_var('ambiente', obj_ref)
            for p, a in zip(params, args):
                self.declare_var(p, a)
            result = None
            try:
                result = self.visit(block)
            except ReturnException as e:
                result = e.value
            self.scopes = saved
            return result
        return method

    # ── Arreglos literales ────────────────────────────────────────
    def visitFactorArreglo(self, ctx):
        items = []
        if ctx.arrayArgsOpt()and ctx.arrayArgsOpt().expr():
            for e in ctx.arrayArgsOpt().expr():
                items.append(self.visit(e))
        return JSArray(items)

    # ── Acceso por índice obj[expr] ───────────────────────────────
    def visitFactorIndice(self, ctx):
        obj = self.visit(ctx.factor())
        key = self.visit(ctx.expr())
        if isinstance(obj, (list, JSArray)):
            return obj[int(key)]
        if isinstance(obj, (dict, JSObject)):
            return obj[key]
        raise TypeError(f"No se puede indexar: {obj}")

    # ── Consola ──────────────────────────────────────────────
    def visitConsolaCall(self, ctx):
        method = ctx.consolaMethod().getText()
        args = []
        if ctx.argsOpt():
            args = self.visit(ctx.argsOpt())

        if method == 'escribir':
            print(*[js_str(a) for a in args])
        elif method == 'error':
            print("ERROR:", *[js_str(a) for a in args], file=sys.stderr)
        elif method == 'limpiar':
            pass  # ignorar por ahora

    def visitArgsOpt(self, ctx):
        return [self.visit(e) for e in ctx.expr()]

    # ── Reglas auxiliares ────────────────────────────────────
    def visitDeclKeyword(self, ctx): pass
    def visitConsolaMethod(self, ctx): pass
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
        # si ( expr ) blockStmt sinoOpt
        cond = self.visit(ctx.expr(0))
        if cond:
            self.visit(ctx.blockStmt(0))
        else:
            sino = ctx.sinoOpt()
            if sino is not None:
                self.visit(sino)

    def visitSinoOpt(self, ctx):
        # sinoOpt : SINO sinoTail | (vacío)
        if ctx.getChildCount() == 0:
            return  # rama vacía
        # hijo 0 = 'sino', hijo 1 = sinoTail
        self.visit(ctx.sinoTail())

    def visitSinoTail(self, ctx):
        # sinoTail : SI LPAREN expr RPAREN blockStmt sinoOpt
        #          | blockStmt
        first = ctx.getChild(0).getText()
        if first == 'si':
            # sino si (expr) blockStmt sinoOpt
            cond = self.visit(ctx.expr())
            if cond:
                self.visit(ctx.blockStmt())
            else:
                sino = ctx.sinoOpt()
                if sino is not None:
                    self.visit(sino)
        else:
            # sino { ... }
            self.visit(ctx.blockStmt())
    
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
    
    # ── Retornar ─────────────────────────────────────────────────
    def visitRetornar(self, ctx):
        # stmt: RETORNAR expr? ';'?
        exprs = ctx.expr()
        value = None
        if exprs:
            # expr() puede ser lista o nodo único según el parser
            e = exprs[0] if isinstance(exprs, list) else exprs
            value = self.visit(e)
        raise ReturnException(value)

    # ── Funciones flecha ─────────────────────────────────────────
    def visitFactorFlecha(self, ctx):
        # factor ARROW arrowBody
        # El factor izquierdo es los parámetros: puede ser un grupo (a, b) o un ID
        params_ctx = ctx.factor()
        params = self._extract_params(params_ctx)
        body = ctx.arrowBody()
        # Captura el scope actual (closure)
        captured = [dict(s) for s in self.scopes]

        def arrow_fn(*args):
            saved = self.scopes
            self.scopes = [dict(s) for s in captured]
            self.push_scope()
            for p, a in zip(params, args):
                self.declare_var(p, a)
            result = None
            try:
                result = self.visit(body)
            except ReturnException as e:
                result = e.value
            self.scopes = saved
            return result

        return arrow_fn

    def _extract_params(self, factor_ctx):
        """Extrae nombres de parámetros de un factor (ID o grupo)."""
        text = factor_ctx.getText()
        # Si es un grupo (a, b, c) => quita paréntesis y parte por coma
        if text.startswith('('):
            inner = text[1:-1]
            return [p.strip() for p in inner.split(',')] if inner else []
        # Si es un solo ID
        return [text]

    def visitArrowBody(self, ctx):
        if ctx.blockStmt():
            return self.visit(ctx.blockStmt())
        else:
            return self.visit(ctx.expr())

    # ── Llamadas a funciones ─────────────────────────────────────
    def visitFactorLlamada(self, ctx):
        # factor(0) es el callable, argsOpt son los args
        callee = self.visit(ctx.factor())
        args = self.visit(ctx.argsOpt()) if ctx.argsOpt() else []
        if callable(callee):
            return callee(*args)
        raise TypeError(f"No es una función: {callee}")

    # ── Acceso a propiedades (.algo) ─────────────────────────────
    # ── Acceso a propiedades — extender visitFactorAcceso ─────────
    def visitFactorAcceso(self, ctx):
        obj = self.visit(ctx.factor())
        prop = ctx.ID().getText()

        # JSObject / dict
        if isinstance(obj, (dict, JSObject)):
            if prop in obj:
                return obj[prop]
            raise AttributeError(f"Propiedad no encontrada en objeto: {prop}")

        # JSArray métodos y propiedades
        if isinstance(obj, (list, JSArray)):
            if prop == 'longitud':  return len(obj)
            if prop == 'agregar':   return lambda x: obj.append(x)
            if prop == 'quitar':    return lambda: obj.pop()
            if prop == 'quitarEn':  return lambda i: obj.pop(int(i))
            if prop == 'incluye':   return lambda x: x in obj
            if prop == 'indexOf':   return lambda x: obj.index(x) if x in obj else -1
            if prop == 'unir':      return lambda sep='': sep.join(js_str(x) for x in obj)
            if prop == 'invertir':  return lambda: obj.reverse()

        # JSNumber métodos de instancia
        if isinstance(obj, JSNumber):
            v = obj.val
            if prop == 'aExponencial':
                def fmt_exp(n):
                    s = f"{n:e}"
                    mantisa, exp = s.split('e')
                    mantisa = mantisa.rstrip('0').rstrip('.')
                    sign = exp[0]
                    num  = str(int(exp[1:]))
                    return f"{mantisa}e{sign}{num}"
                return lambda: fmt_exp(v)
            if prop == 'fijarDecimales': return lambda n: f"{v:.{n}f}"
            if prop == 'aCadena':        return lambda: js_str(v)
            if prop == 'valorDe':        return lambda: v

        # NumeroBuiltin
        if isinstance(obj, type(NumeroBuiltin)) or obj is NumeroBuiltin:
            if prop == 'esFinito':           return NumeroBuiltin.esFinito
            if prop == 'esEntero':           return NumeroBuiltin.esEntero
            if prop == 'esEnteroSeguro':     return NumeroBuiltin.esEnteroSeguro
            if prop == 'interpretarDecimal': return NumeroBuiltin.interpretarDecimal
            if prop == 'interpretarEntero':  return NumeroBuiltin.interpretarEntero
            if prop == 'POSITIVE_INFINITY':  return float('inf')

        # MateBuiltin
        if obj is MateBuiltin:
            return getattr(MateBuiltin, prop)

        raise AttributeError(f"Propiedad no encontrada: {prop}")
    
    # ── Funciones normales ────────────────────────────────────────
    def visitFuncion(self, ctx):
        # stmt: FUNCION ID LPAREN paramsOpt RPAREN blockStmt
        # visitStmt ya despacha, hay que manejarlo aquí
        pass
    
    # ── Factores builtin ─────────────────────────────────────────
    def visitFactorNumeroBuiltin(self, ctx):  return NumeroBuiltin
    def visitFactorMate(self, ctx):           return MateBuiltin
    
    def visitFactorAmbiente(self, ctx):  
        return self.get_var('ambiente')  # debe buscar en scope, no retornar None
    
    def visitFactorPostfijo(self, ctx):
        op   = ctx.getChild(1).getText()
        name = ctx.factor().getText()  # simplificado: asume ID simple
        val  = self.get_var(name)
        if op == '++':
            self.set_var(name, val + 1)
        elif op == '--':
            self.set_var(name, val - 1)
        return val  # postfijo retorna el valor ANTES de modificar

    def visitFactorPrefijo(self, ctx):
        op  = ctx.getChild(0).getText()
        val = self.visit(ctx.factor())
        if op == '!':  return not val
        if op == '-':  return -val
        if op == '+':  return +val
        if op == '++':
            name = ctx.factor().getText()
            self.set_var(name, val + 1)
            return val + 1
        if op == '--':
            name = ctx.factor().getText()
            self.set_var(name, val - 1)
            return val - 1

    def _js_eq(self, left, right):
        # nulo == indefinido (y viceversa)
        if (left is NULO or left is INDEFINIDO) and (right is NULO or right is INDEFINIDO):
            return True
        # Si uno es nulo/indefinido y el otro no, false
        if left is NULO or left is INDEFINIDO or right is NULO or right is INDEFINIDO:
            return False
        # Coerción numérica: si uno es número y el otro string, convierte el string
        if isinstance(left, (int, float)) and isinstance(right, str):
            try:
                return left == type(left)(right)
            except (ValueError, TypeError):
                return False
        if isinstance(right, (int, float)) and isinstance(left, str):
            try:
                return right == type(right)(left)
            except (ValueError, TypeError):
                return False
        # bool == número (verdadero == 1, falso == 0)
        if isinstance(left, bool) and isinstance(right, (int, float)):
            return int(left) == right
        if isinstance(right, bool) and isinstance(left, (int, float)):
            return int(right) == left
        return left == right

    def _declare_funcion(self, ctx):
        name = ctx.getChild(1).getText()
        params = []
        params_opt = ctx.paramsOpt()
        if params_opt and params_opt.ID():
            params = [p.getText() for p in params_opt.ID()]
        block = ctx.blockStmt(0)
        global_scope = self.scopes[0]  # referencia viva al scope global

        def fn(*args):
            saved = self.scopes
            self.scopes = [global_scope]
            self.push_scope()
            for p, a in zip(params, args):
                self.declare_var(p, a)
            result = None
            try:
                result = self.visit(block)
            except ReturnException as e:
                result = e.value
            self.scopes = saved
            return result

        self.declare_var(name, fn)

def js_str(val):
    if isinstance(val, JSNumber):
        v = val.val
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        return str(v)
    if val is True:         return 'verdadero'
    if val is False:        return 'falso'
    if val is NULO:         return 'nulo'
    if val is INDEFINIDO:   return 'indefinido'
    if val == float('inf'): return 'Infinito'
    if isinstance(val, float) and val.is_integer():
        return str(int(val))
    return str(val)

