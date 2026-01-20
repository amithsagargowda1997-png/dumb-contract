from solcx import compile_standard, install_solc
import json

install_solc("0.8.0")


def parse_solidity(file_path):
    with open(file_path, "r") as f:
        source = f.read()

    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {
                "Contract.sol": {
                    "content": source
                }
            },
            "settings": {
                "outputSelection": {
                    "*": {
                        "": ["ast"]   # <-- IMPORTANT FIX
                    }
                }
            },
        },
        solc_version="0.8.0",
    )

    # Source-level AST
    ast = compiled["sources"]["Contract.sol"]["ast"]
    return ast


EXTERNAL_CALLS = {"call", "delegatecall", "send", "transfer"}


def find_external_calls(ast):
    results = []

    def walk(node, current_function=None):
        if not isinstance(node, dict):
            return

        # Track function context
        if node.get("nodeType") == "FunctionDefinition":
            current_function = node.get("name")

        # Detect member access like msg.sender.call
        if node.get("nodeType") == "MemberAccess":
            member = node.get("memberName")
            if member in EXTERNAL_CALLS:
                results.append({
                    "function": current_function,
                    "call_type": member,
                    "line": node["src"]
                })

        for value in node.values():
            if isinstance(value, dict):
                walk(value, current_function)
            elif isinstance(value, list):
                for item in value:
                    walk(item, current_function)

    walk(ast)
    return results

def get_function_visibility(ast):
    """
    Returns: dict {function_name: visibility}
    """
    visibility = {}

    def walk(node):
        if not isinstance(node, dict):
            return

        if node.get("nodeType") == "FunctionDefinition":
            name = node.get("name")
            vis = node.get("visibility")
            if name:
                visibility[name] = vis

        for value in node.values():
            if isinstance(value, dict):
                walk(value)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

    walk(ast)
    return visibility

