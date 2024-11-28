from lark import Tree, Token

"""
Tree:
    Representa una regla no terminal como:
    - function_definition.
    - basic_instruction.

    Procesamos los Tree recursivamente leyendo `data` y `children`.
"""
"""
Token:
    Representa una regla terminal como:
    - CNAME
    - INTNUM

    Token es leído directamente usando `type` y `value`.
"""

def translate_program(ast, out, indent=0):
    """
    Genera código Python a partir del árbol sintáctico de High-LOGO.

    translate_program(ast, out, indent=0)

    ast "Abstract Syntax Tree" (Árbol de Sintaxis Abstracta): 
        - Representa la estructura jerárquica del código según la gramática analizada por el parser.
        - Los nodos del árbol corresponden a un Token o un Tree (Una regla terminal o no terminal).

        Estructura de Tree:
            - data: Nombre de la regla de la gramática representada por el nodo actual. Ej: `ast.data == "basic_instruction"`.
            - children: Lista de nodos hijos, que pueden ser otros Tree (reglas no terminales) o Token (símbolos terminales).
        
        Estructura de Token:
            - type: Tipo del Token (Ej: INTNUM, CNAME).
            - value: Valor del Token (Ej: 100, size).
        
        Ejemplo de acceso:
        ```
        if isinstance(ast, Tree):
            print(ast.data)  # Regla no terminal
            for child in ast.children:
                ...
        elif isinstance(ast, Token):
            print(ast.type)  # Tipo del Token
            print(ast.value)  # Valor del Token
        ```

    out: Archivo de salida donde se escribe el código traducido.
    
    indent: Nivel de indentación utilizado para el código Python generado. Default = 0.
    """
    indentation = "    " * indent  # Define el nivel de indentación actual

    if ast.data == "start":
        # Nodo raíz: configura el programa inicial
        out.write("import turtle\n")
        out.write("t = turtle.Turtle()\n")
        for child in ast.children:
            translate_program(child, out, indent)
        out.write("turtle.mainloop()\n")

    elif ast.data == "basic_instruction":
        # Procesa una instrucción básica
        for child in ast.children:
            translate_program(child, out, indent)

    elif ast.data == "arg_instruction":
        # Instrucción con argumento (ej: FD, BK, LT, RT, WIDTH)
        instruction = ast.children[0].value  # Nombre de la instrucción
        operand_node = ast.children[1]  # Operando (puede ser INTNUM o expresión)
        value = evaluate_operand(operand_node)
        out.write(f"{indentation}t.{instruction_map(instruction)}({value})\n")

    elif ast.data == "no_arg_instruction":
        # Instrucción sin argumento (ej: PU, PD)
        instruction = ast.children[0].value  # Nombre de la instrucción
        out.write(f"{indentation}t.{instruction_map(instruction)}()\n")

    elif ast.data == "repeat_instruction":
        # Estructura REPEAT (repetición de un bloque de instrucciones)
        repeat_count = evaluate_operand(ast.children[0])  # Número de repeticiones
        block = ast.children[1]  # Bloque de instrucciones a repetir
        out.write(f"{indentation}for _ in range({repeat_count}):\n")
        translate_block(block, out, indent + 1)

    elif ast.data == "block":
        # Procesa un bloque de instrucciones
        for child in ast.children:
            translate_program(child, out, indent)

    elif ast.data == "conditional_instruction":
        # Instrucción condicional (IF / ELSE)
        condition_node = ast.children[0]
        condition = evaluate_condition(condition_node)
        out.write(f"{indentation}if {condition}:\n")
        translate_block(ast.children[1], out, indent + 1)
        if len(ast.children) > 2 and ast.children[2] is not None:
            out.write(f"{indentation}else:\n")
            translate_block(ast.children[2], out, indent + 1)

    elif ast.data == "function_definition":
        # Definición de funciones
        function_name = ast.children[0].value  # Nombre de la función

        # Lista de parámetros (puede estar vacía)
        parameters = [param.value for param in ast.children[1].children] if ast.children[1] else []
        out.write(f"{indentation}def {function_name}({', '.join(parameters)}):\n")
        translate_block(ast.children[2], out, indent + 1)

    elif ast.data == "function_call":
        # Llamado a funciones
        function_name = ast.children[0].value  # Nombre de la función
        arguments = [evaluate_operand(argument) for argument in ast.children[1].children] if ast.children[1] else []
        out.write(f"{indentation}{function_name}({', '.join(arguments)})\n")

    elif ast.data == "for_loop":
        # Ciclo FOR (con range o zip)
        loop_vars = [child.value for child in ast.children[:-2]]  # Variables del bucle
        iterable_node = ast.children[-2]

        if iterable_node.data == "range":
            # Genera un rango
            values = [evaluate_operand(child) for child in iterable_node.children]
            if len(values) == 1:
                out.write(f"{indentation}for {loop_vars[0]} in range({values[0]}):\n")
            elif len(values) == 2:
                out.write(f"{indentation}for {loop_vars[0]} in range({values[0]}, {values[1]}):\n")
            elif len(values) == 3:
                out.write(f"{indentation}for {loop_vars[0]} in range({values[0]}, {values[1]}, {values[2]}):\n")
            translate_block(ast.children[-1], out, indent + 1)

        elif iterable_node.data == "zip_call":
            # Genera un bucle con zip
            ranges = [
                f"range({evaluate_operand(range_node.children[0])}, {evaluate_operand(range_node.children[1])}, {evaluate_operand(range_node.children[2])})"
                for range_node in iterable_node.children
            ]
            out.write(f"{indentation}for {', '.join(loop_vars)} in zip({', '.join(ranges)}):\n")
            translate_block(ast.children[-1], out, indent + 1)

    else:
        print(f"Nodo no manejado: {ast.data}")


def translate_block(block, out, indent):
    """
    Traduce un bloque de instrucciones.
    """
    for child in block.children:
        translate_program(child, out, indent)

def evaluate_operand(node):
    """
    Evalúa un operando (constantes, variables o expresiones aritméticas).
    """
    if isinstance(node, Tree) and node.data == "operand":
        child = node.children[0]
        if isinstance(child, Token) and child.type == "INTNUM":
            return child.value
        elif isinstance(child, Token) and child.type == "CNAME":
            return child.value
        elif isinstance(child, Tree) and child.data == "arithmetic_expression":
            return evaluate_operand(child)

    elif isinstance(node, Tree) and node.data == "arithmetic_expression":
        left = evaluate_operand(node.children[0])
        operator = node.children[1].children[0].value
        right = evaluate_operand(node.children[2])
        return f"({left} {operator} {right})"

    raise ValueError(f"Operando no soportado: {node}")

def evaluate_condition(node):
    if isinstance(node, Token):
        raise ValueError(f"Unexpected token in condition: {node}")

    if node.data == "condition":
        return evaluate_condition(node.children[0])

    elif node.data == "comparison":
        left = evaluate_operand(node.children[0])
        operator_node = node.children[1]
        operator = (
            operator_node.children[0].value if isinstance(operator_node, Tree) else operator_node.value
        )
        right = evaluate_operand(node.children[2])
        return f"{left} {operator} {right}"

    elif node.data == "negation":
        return f"not ({evaluate_condition(node.children[1])})"

    elif node.data == "grouped_condition":
        return f"({evaluate_condition(node.children[0])})"

    elif node.data == "conjunction":
        left = evaluate_condition(node.children[0])
        right = evaluate_condition(node.children[2])
        return f"({left} and {right})"

    elif node.data == "disjunction":
        left = evaluate_condition(node.children[0])
        right = evaluate_condition(node.children[2])
        return f"({left} or {right})"

    raise ValueError(f"Unsupported condition node: {node}")

def instruction_map(instruction):
    """
    Mapea las instrucciones de High-LOGO a los métodos de Turtle.
    """
    return {
        "FD": "forward",
        "BK": "backward",
        "LT": "left",
        "RT": "right",
        "WIDTH": "width",
        "PU": "penup",
        "PD": "pendown"
    }.get(instruction, instruction)

