import argparse
from ast import (
    AST,
    Assign,
    ClassDef,
    Constant,
    Dict,
    Load,
    Name,
    NodeTransformer,
    Store,
    copy_location,
    fix_missing_locations,
    parse,
    unparse,
)
from io import StringIO
import logging
import re


class DictTransformer(NodeTransformer):
    def visit_Assign(self, node):
        if isinstance(node.value, Dict):
            new_node = node
            if not all(isinstance(key, Constant) for key in node.value.keys):
                logging.warning("Dict keys must be constants.")
            if not all(isinstance(value, Constant) for value in node.value.values):
                logging.warning("Dict values must be constants.")
            else:
                class_name = "".join(
                    map(
                        str.title,
                        re.sub(r"([A-Z])", r" \1", node.targets[0].id).split(),
                    )
                )
                body = [
                    Assign(
                        targets=[Name(id=k.value.upper(), ctx=Store())],
                        value=Constant(value=v.value),
                    )
                    for k, v in zip(node.value.keys, node.value.values)
                ]
                new_node = ClassDef(
                    name=class_name,
                    bases=[Name(id="Enum", ctx=Load())],
                    keywords=[],
                    body=body,
                    decorator_list=[],
                )

            copy_location(new_node, node)
            fix_missing_locations(new_node)
            self.generic_visit(node)

            return new_node
        return node


def load_ast_from_file(filename: str):
    with open(filename) as f:
        return parse(f.read())


def load_ast_from_stringIO(f: StringIO):
    return parse(f.read())


def transform_ast(ast: AST):
    transformer = DictTransformer()
    transformed_ast = transformer.visit(ast)
    return transformed_ast


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    args = parser.parse_args()
    filename = args.input
    ast = load_ast_from_file(filename)
    transformed_ast = transform_ast(ast)
    with open(filename, "w") as py_file:
        py_file.write(unparse(transformed_ast))
