def detect_gas_loops(ast):
    findings = []
    current_function = None

    def loop_contains_external_call(loop_node):
        found = False

        def inner(n):
            nonlocal found
            if not isinstance(n, dict):
                return

            if n.get("nodeType") == "MemberAccess":
                if n.get("memberName") in ("call", "delegatecall", "send", "transfer"):
                    found = True

            for v in n.values():
                if isinstance(v, dict):
                    inner(v)
                elif isinstance(v, list):
                    for i in v:
                        inner(i)

        inner(loop_node)
        return found

    def walk(node):
        nonlocal current_function

        if not isinstance(node, dict):
            return

        if node.get("nodeType") == "FunctionDefinition":
            current_function = node.get("name")

        if node.get("nodeType") in ("ForStatement", "WhileStatement"):
            findings.append({
                "function": current_function,
                "loop_type": node.get("nodeType"),
                "external_call_inside": loop_contains_external_call(node),
                "src": node.get("src")
            })

        for value in node.values():
            if isinstance(value, dict):
                walk(value)
            elif isinstance(value, list):
                for item in value:
                    walk(item)

    walk(ast)
    return findings
