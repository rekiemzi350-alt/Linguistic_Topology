
def num_to_english(n):
    # Basic implementation for 0-1000 to map the sequence
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n < 20:
        return ones[n]
    if n < 100:
        return tens[n // 10] + ones[n % 10]
    if n < 1000:
        return ones[n // 100] + "hundred" + (tens[(n % 100) // 10] + ones[n % 10] if n % 100 != 0 else "")
    return ""

def count_letters(word):
    # remove hyphens or spaces if any (though our function above generates simple concatenated strings)
    return len(word.replace(" ", "").replace("-", ""))

def get_sequence_path(start_num, limit=200):
    path = [start_num]
    current = start_num
    
    # We stop if we hit a number clearly beyond our interest or if it gets too large
    # For this check, we want to see if they hit 21.
    while current < limit:
        word = num_to_english(current)
        if not word and current != 0: break # Safety for out of bounds of our simple function
        
        # specific fix for 0 since our array had empty string for index 0 for math logic
        if current == 0: 
            length = 4 # "zero"
        else:
            length = count_letters(word)
            
        next_val = current + length
        path.append(next_val)
        current = next_val
        
        if current > 100 and 21 not in path: # Optimization: stop early if we pass the target zone
            break
            
    return path

# Analyze the "Rivers"
target_node = 21
hits_target = []
misses_target = []

print(f"{'Start':<10} | {'Path (truncated)'}")
print("-" * 60)

for i in range(25): # Check first 25 integers
    path = get_sequence_path(i)
    path_str = " -> ".join(map(str, path[:6])) + "..."
    
    if target_node in path:
        hits_target.append(i)
        status = "[HITS 21]"
    else:
        misses_target.append(i)
        status = "[MISS]"
        
    print(f"{i:<10} | {path_str:<40} {status}")

print("\n--- Summary ---")
print(f"Numbers 0-24 that hit 21: {hits_target}")
print(f"Numbers 0-24 that MISS 21: {misses_target}")

# Let's trace a 'Miss' to see if it has its own interesting path
if misses_target:
    example_miss = misses_target[0]
    full_path = get_sequence_path(example_miss, limit=100)
    print(f"\nDetailed path for {example_miss}: {full_path}")
