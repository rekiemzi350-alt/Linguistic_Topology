
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    if n == 0: return "zero"
    parts = []
    if n >= 1000:
        parts.append(num_to_english(n // 1000) + "thousand")
        n %= 1000
    if n >= 100:
        parts.append(ones[n // 100] + "hundred")
        n %= 100
    if n >= 20:
        parts.append(tens[n // 10])
        n %= 10
    if n > 0:
        parts.append(ones[n])
    return "".join(parts)

def a_seq(n_terms):
    res = []
    x = 0
    for _ in range(n_terms):
        res.append(x)
        x += len(num_to_english(x))
    return res

print(", ".join(map(str, a_seq(40))))
