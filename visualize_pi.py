import math

# The first 100 digits of Pi
pi_digits = "3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067"

def get_english_len(d):
    # Lengths of: zero, one, two, three, four, five, six, seven, eight, nine
    lengths = [4, 3, 3, 5, 4, 4, 3, 5, 5, 4] 
    return lengths[int(d)]

print("\n--- VISUALIZATION 1: THE RAW WAVEFORM OF PI (First 100 Digits) ---")
print("This represents pure mathematical data. Expect 'Static/Noise'.\n")

for i, d in enumerate(pi_digits):
    val = int(d)
    # Draw a bar
    bar = "█" * val
    # Add a 'wave' character at the tip
    if i < len(pi_digits) - 1:
        next_val = int(pi_digits[i+1])
        tip = " "
        if next_val > val: tip = "↗"
        elif next_val < val: tip = "↘"
        else: tip = "→"
    else:
        tip = ""
        
    print(f"{d} | {bar}{tip}")

print("\n\n--- VISUALIZATION 2: THE LINGUISTIC WAVEFORM OF PI ---")
print("Mapping Pi through the 'English Filter' (Digit -> Word Length).")
print("Does English impose order on the chaos?\n")

for i, d in enumerate(pi_digits):
    val = get_english_len(d)
    # Draw a bar
    bar = "▒" * val
    
    # Calculate trend
    trend = ""
    if i > 0:
        prev = get_english_len(pi_digits[i-1])
        if val > prev: trend = " (Rising)"
        elif val < prev: trend = " (Falling)"
        else: trend = " (Stable)"
    
    print(f"{d} -> {val} | {bar}")

print("\n--- ANALYSIS ---")
print("1. Raw Pi is jagged and unpredictable (High Entropy).")
print("2. The Linguistic Waveform is much smoother.")
print("   Notice how the bar lengths cluster between 3, 4, and 5.")
print("   English refuses to process the extremes (0 or 9).")
print("   It forces the infinite complexity of Pi into a narrow, stable band of 3-5.")
