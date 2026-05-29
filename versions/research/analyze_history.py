
def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if n == 0: return "zero"
    
    base_str = ""
    if n >= 1000:
        k = n // 1000
        rem = n % 1000
        base_str += num_to_english(k) + "thousand"
        if rem > 0: base_str += num_to_english(rem)
        return base_str
        
    if n >= 100:
        h = n // 100
        rem = n % 100
        base_str += ones[h] + "hundred"
        if rem > 0: base_str += num_to_english(rem)
        return base_str
        
    if n < 20: return ones[n]
    if n < 100: return tens[n // 10] + ones[n % 10]
    
    return ""

def get_len(n):
    name = num_to_english(n)
    return len(name.replace(" ", "").replace("-", ""))

def get_next(n):
    return n + get_len(n)

# 1. Generate Main Trunk up to 2030
trunk = [0]
curr = 0
while curr < 2030:
    curr = get_next(curr)
    trunk.append(curr)

trunk_set = set(trunk)

# 2. Key Historical Dates (War, Peace, Crashes, Growth)
# Mixed global/US major events
events = {
    1776: "US Independence",
    1789: "French Revolution",
    1815: "Napoleonic Wars End",
    1861: "US Civil War Start",
    1865: "US Civil War End",
    1914: "WWI Start",
    1918: "WWI End",
    1929: "Great Depression Crash",
    1939: "WWII Start",
    1941: "Pearl Harbor",
    1945: "WWII End",
    1969: "Moon Landing",
    1989: "Berlin Wall Fall",
    1991: "USSR Collapse",
    2001: "9/11 Attacks",
    2008: "Financial Crisis",
    2020: "COVID-19 Pandemic"
}

print(f"--- Historical 'Main Trunk' Analysis ---")
print(f"Checking if major historical years fall on the 'Erik Convergence' Line...\n")

hits = []
misses = []

for year, name in sorted(events.items()):
    if year in trunk_set:
        hits.append(f"{year}: {name}")
    else:
        # Find distance to nearest trunk year
        # Find closest val in trunk
        closest = min(trunk, key=lambda x:abs(x-year))
        dist = year - closest
        misses.append(f"{year}: {name} (Missed by {dist:+d} -> Trunk hit {closest})")

print("--- DIRECT HITS (Years on the Trunk) ---")
for h in hits: print(h)

print("\n--- MISSES (Years in the Void) ---")
for m in misses: print(m)

# 3. Waveform Analysis of the 20th Century
# Check if the "Letter Count" of years creates a wave matching eras
print("\n--- Linguistic Density Waveform (1900-2025) ---")
# Calculate length for every year
years = range(1900, 2026)
lengths = [get_len(y) for y in years]

# A simple visualization of "Density" (High letter count vs Low)
# We look for "Eras" of high density
print("Years with PEAK Linguistic Density (>23 letters):")
peaks = [y for y in years if get_len(y) >= 24]
print(peaks)

print("\nYears with LOW Linguistic Density (<20 letters):")
valleys = [y for y in years if get_len(y) <= 19]
print(valleys)
