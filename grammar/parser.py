from lark import Lark, Tree, Token
import os

def parse_code(code):
    """
        Parsea el código de entrada usando la gramática.
    """
    grammar_path = os.path.join(os.path.dirname(__file__), "BugScript.lark")
    with open(grammar_path, "r") as file:
        grammar = file.read()

    parser = Lark(grammar, start='start', parser='lalr', lexer='contextual')
    try:
        return parser.parse(code)
    except Exception as e:
        raise SyntaxError(f"Error parsing code: {e}")

def print_tree_Trees_and_Tokens(node, indent=0):
    """
        Imprime el árbol de sintaxis con detalles de Tree y Token.
    """
    indentation = "  " * indent
    if isinstance(node, Tree):
        print(f"{indentation}Tree('{node.data}', [")
        for child in node.children:
            print_tree_Trees_and_Tokens(child, indent + 1)
        print(f"{indentation}])")
    elif isinstance(node, Token):
        print(f"{indentation}Token('{node.type}', '{node.value}')")
    else:
        print(f"{indentation}{repr(node)}")
