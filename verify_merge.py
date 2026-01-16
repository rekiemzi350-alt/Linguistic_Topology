
def get_english_name(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    if n >= 1000: 
        # minimal support for >1000 just in case
        k = n // 1000
        rem = n % 1000
        base = get_english_name(k) + "thousand"
        if rem == 0: return base
        return base + get_english_name(rem)

    if n >= 100:
        h = n // 100
        rem = n % 100
        base = ones[h] + "hundred"
        if rem == 0: return base
        return base + get_english_name(rem)

    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    return ""

def get_next(n):
    name = get_english_name(n)
    length = len(name.replace(" ", "").replace("-", ""))
    return n + length

# Generate Trunk
trunk = [0]
curr = 0
while curr < 500:
    curr = get_next(curr)
    trunk.append(curr)

# Generate Rebel
rebel = [83]
curr = 83
merge_val = -1
while curr < 500:
    curr = get_next(curr)
    rebel.append(curr)
    if curr in trunk:
        merge_val = curr
        break

print(f"Trunk Sequence: {trunk}")
print(f"Rebel Sequence: {rebel}")
print(f"Merge Point: {merge_val}")
