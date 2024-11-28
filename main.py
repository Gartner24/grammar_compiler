from grammar.parser import parse_code, print_tree_Trees_and_Tokens
from compiler.compiler import translate_program
import os, sys
from lark import tree

input_file = sys.argv[1]
output_file = str("./examples/") + sys.argv[1] + str(".py")

if not os.path.exists(input_file):
    print(f"Error: The file '{input_file}' does not exist.")
    exit(1)

print(f"Input file: {input_file}")

"""
    Leemos el archivo .bs
"""
with open(input_file, "r") as file:
    code = file.read()

parse_tree = parse_code(code)

# print(parse_tree.pretty())
print_tree_Trees_and_Tokens(parse_tree)

"""
    Crear visualizacion del Árbol de Sintaxis Abstracta
"""
tree.pydot__tree_to_png(parse_tree, "./examples/tree_%s.png" % (input_file))
# tree.pydot__tree_to_dot(parse_tree, "./examples/tree.dot", rankdir="TD")

with open(output_file, "w") as out:
    translate_program(parse_tree, out)
