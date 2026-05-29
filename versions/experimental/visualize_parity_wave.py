import sys

# English Number to Words
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    parts = []
    if n >= 1000:
        k = n // 1000
        n %= 1000
        parts.append(num_to_english(k) + "thousand")
    if n >= 100:
        h = n // 100
        n %= 100
        parts.append(ones[h] + "hundred")
    if n >= 20:
        t = n // 10
        n %= 10
        parts.append(tens[t])
    if n > 0:
        parts.append(ones[n])
        
    return "".join(parts)

def get_len(n):
    return len(num_to_english(n))

def visualize_parity_wave(steps=50):
    curr = 0
    center = 30
    amplitude = 15
    
    print(f"{'EVEN (Negative)':<30} | {'ODD (Positive)':<30}")
    print("-" * 60)
    
    prev_x = -1 # State tracker: -1 for Even, 1 for Odd
    
    for i in range(steps):
        is_odd = (curr % 2 != 0)
        length = get_len(curr)
        
        # Determine Position
        # If Odd: Positive Side (Right of center)
        # If Even: Negative Side (Left of center)
        
        # To make it look like a wave, we can try to "interpolate" visually,
        # but strictly:
        if is_odd:
            pos = center + amplitude
            # Symbol: O for Odd
            line = " " * pos + f"{curr} ({length})"
        else:
            pos = center - amplitude
            # Adjust for length of number string to align roughly right-end or left-end
            # Let's just place it at the specific column
            s = f"{curr} ({length})"
            line = " " * (pos - len(s)) + s
            
        # Draw connector (rough ASCII approximation)
        # If we switched sides, draw a slash
        connector = ""
        if i > 0:
            if is_odd and prev_x == -1:
                # Switched Even -> Odd ( / )
                # We need a line crossing the center
                pass 
            elif not is_odd and prev_x == 1:
                # Switched Odd -> Even ( \ )
                pass
        
        print(line)
        
        # Update for next step
        if is_odd: prev_x = 1
        else: prev_x = -1
        
        curr += length

if __name__ == "__main__":
    visualize_parity_wave(60)
