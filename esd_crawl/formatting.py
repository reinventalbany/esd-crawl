Number = int | float


def format_num(num: int):
    return "{:,}".format(num)


def format_pct(numerator: Number, denominator: Number):
    pct = numerator / denominator * 100
    return f"{pct:.1f}%"
