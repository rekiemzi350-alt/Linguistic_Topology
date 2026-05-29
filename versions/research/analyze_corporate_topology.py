
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    return "" # Simplified for speed

def get_english_len(n):
    # Average length ~ 7-10 letters
    if n == 0: return 4
    return len(num_to_english(n).replace(" ", ""))

def get_mandarin_len(n):
    # 0: 零 (1)
    # 1-10: 1 char
    # 11-19: 2 chars (Ten-One)
    # 20-99: 2 or 3 chars (Two-Ten or Two-Ten-One)
    if n == 0: return 1
    if n <= 10: return 1
    if n < 20: return 2
    if n < 100:
        if n % 10 == 0: return 2
        return 3
    return 3 # Approx for > 100

# Compare Trajectories
# English: n -> n + EnglishLen
# Mandarin: n -> n + MandarinLen

print("--- Corporate Topology Analysis ---")
print("Comparing the 'Operating Speed' of the Linguistic Substrate\n")

eng_curr = 0
man_curr = 0

print(f"{ 'Step':<5} | { 'English Value':<15} | { 'Mandarin Value':<15} | {'Ratio (Eng/Man)'}")
print("-" * 60)

for step in range(21): # First 20 steps
    ratio = eng_curr / man_curr if man_curr > 0 else 0
    print(f"{step:<5} | {eng_curr:<15} | {man_curr:<15} | {ratio:.2f}")
    
    eng_curr = eng_curr + get_english_len(eng_curr)
    man_curr = man_curr + get_mandarin_len(man_curr)

print("-" * 60)
print("\nAnalysis:")
print(f"After 20 steps, English has reached: {eng_curr}")
print(f"After 20 steps, Mandarin has reached: {man_curr}")
print(f"Speed Multiplier: {eng_curr / man_curr:.2f}x")
