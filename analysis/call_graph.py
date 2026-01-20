IGNORED_FUNCTIONS = {
    "require",
    "assert",
    "revert",
    "emit",
    "keccak256",
    "sha256",
    "ripemd160",
    "addmod",
    "mulmod"
}

LOW_LEVEL_CALLS = {
    "call",
    "delegatecall",
    "staticcall",
    "callcode",
    "send",
    "transfer"
}


def build_call_graph(ast):
    call_graph = {}
    current_function = None

    def walk(node):
        nonlocal current_function

        if not isinstance(node, dict):
            return

        # Track current function
        if node.get("nodeType") == "FunctionDefinition":
            current_function = node.get("name")
            if current_function:
                call_graph.setdefault(current_function, set())

        # Detect function calls
        if node.get("nodeType") == "FunctionCall":
            expression = node.get("expression", {})

            # Direct call: foo()
            # if expression.get("nodeType") == "Identifier":
            #     callee = expression.get("name")
            #     if current_function and callee:
            #         call_graph[current_function].add(callee)
            if expression.get("nodeType") == "Identifier":
                callee = expression.get("name")
                if (
                    current_function
                    and callee
                    and callee not in IGNORED_FUNCTIONS
                ):
                    call_graph[current_function].add(callee)
            
            # Member call: this.foo()
            if expression.get("nodeType") == "MemberAccess":
                callee = expression.get("memberName")
                if (
                    current_function
                    and callee
                    and callee not in LOW_LEVEL_CALLS
                ):
                    call_graph[current_function].add(callee)


        for value in node.values():
            if isinstance(value, dict):
                walk(value)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

    walk(ast)
    return call_graph
