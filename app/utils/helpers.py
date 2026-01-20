def format_number(num: int):
    if num >= 1_000_000:
        return f"{num//1_000_000}M"
    if num >= 1_000:
        return f"{num//1_000}K"
    return str(num)
