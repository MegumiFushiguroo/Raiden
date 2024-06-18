import ast
import math
import operator as op

# Supported functions and operators
 Functions = {
     "abs": math.fabs,
     "all": all,
     "any": any,
     "bin": bin,
     "bool": bool,
     "divmod": divmod,
     "round": round,
     "sum": sum,
 }

Operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}

class SafeEval(ast.NodeVisitor):
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in Functions:
            return Functions[node.func.id](self.visit(arg) for arg in node.args)
        elif isinstance(node.func, ast.BinOp) and node.func.op in Operators:
            return Operators[node.func.op](self.visit(node.func.left), self.visit(node.func.right))
        raise ValueError(f"Unsupported call: {node.func}")

    def visit_Num(self, node):
        return node.n

    def visit_Str(self, node):
        return node.s

    def visit_UnaryOp(self, node):
        if isinstance(node.op, ast.USub):
            return -self.visit(node.operand)
        raise ValueError(f"Unsupported unary op: {node.op}")

@Client.on_message(filters.command("eval"))
def eval(client, message):
    try:
        code = message.text.split(" ", 1)[1]
        safe_node = ast.parse(code, mode="eval")
        safe_node = SafeEval().visit(safe_node)
        message.reply(f"**Output:** ```{safe_node}```")
    except Exception as e:
        message.reply(f"**Error:** ```{e}```")