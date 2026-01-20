def detect_reentrancy(call_graph, external_calls, function_visibility):
    """
    Flag only public/external functions that can reach an external call.
    """

    external_funcs = set()
    for c in external_calls:
        if c["function"]:
            external_funcs.add(c["function"])

    vulnerable = set()

    def dfs(current, visited):
        if current in visited:
            return False
        visited.add(current)

        if current in external_funcs:
            return True

        for callee in call_graph.get(current, []):
            if dfs(callee, visited):
                return True

        return False

    for function, visibility in function_visibility.items():
        if visibility in ("public", "external"):
            if dfs(function, set()):
                vulnerable.add(function)

    return vulnerable
