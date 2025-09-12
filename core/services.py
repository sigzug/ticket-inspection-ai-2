def compute(numbers: list[float], op: str) -> float:
    # O(n), enkel og effektiv
    if op == "sum":
        return float(sum(numbers))
    if op == "avg":
        return float(sum(numbers) / len(numbers))
    if op == "max":
        return float(max(numbers))
    if op == "min":
        return float(min(numbers))
    raise ValueError("Unsupported operation")
