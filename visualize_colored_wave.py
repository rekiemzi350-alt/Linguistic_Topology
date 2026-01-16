import sys
import time

# --- Configuration ---
STEPS = 40
WIDTH = 60
CENTER = WIDTH // 2
OFFSET_SCALE = 2  # How far from center to push

# ANSI Colors
COLORS = [
    "\033[94m", # Blue (Seed 0 - Main Trunk)
    "\033[91m", # Red
    "\033[92m", # Green
    "\033[93m", # Yellow
    "\033[95m", # Magenta
    "\033[96m", # Cyan
    "\033[33m", # Orange/Brown
    "\033[97m"  # White
]
RESET = "\033[0m"
BOLD = "\033[1m"

# --- Logic ---

def num_to_english(n):
    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", 
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    if n == 0: return "zero"
    parts = []
    if n >= 1000:
        k = n // 1000; n %= 1000; parts.append(num_to_english(k) + "thousand")
    if n >= 100:
        h = n // 100; n %= 100; parts.append(ones[h] + "hundred")
    if n >= 20:
        t = n // 10; n %= 10; parts.append(tens[t])
    if n > 0:
        parts.append(ones[n])
    return "".join(parts)

def get_len(n):
    return len(num_to_english(n))

def run_visualization():
    # State
    active_seeds = {} # {seed_id: current_value}
    
    # Initialize specific seeds
    # Seed 0: Main Trunk (Blue)
    # Seed 93: Rebel Stream (Red)
    active_seeds[0] = 0
    active_seeds[93] = 93
    
    print(f"{'EVEN (Downswing/Left)':>{CENTER-2}} | {'ODD (Upswing/Right)':<{CENTER-2}}")
    print("-" * WIDTH)

    # We iterate enough steps to see the parallel flow
    # The Rebel Stream merges much later (at 2827), so 200 steps shows the parallel behavior well.
    for t in range(200):
        # Buffer for this line's output
        line_chars = [" "] * WIDTH
        line_chars[CENTER] = "|"
        
        # Process seeds
        seeds_to_remove = []
        
        for seed_id, val in active_seeds.items():
            # Color assignment
            if seed_id == 0:
                color = "\033[94m" # Blue
                symbol = "0"
            else:
                color = "\033[91m" # Red
                symbol = "R" # Rebel

            # --- Plotting ---
            is_odd = (val % 2 != 0)
            
            # Position logic
            if is_odd:
                # Right side
                base_idx = CENTER + 2
                jitter = (val % 20) 
                idx = base_idx + jitter
            else:
                # Left side
                base_idx = CENTER - 3
                jitter = (val % 20)
                idx = base_idx - jitter

            # Bounds check
            if idx < 0: idx = 0
            if idx >= WIDTH: idx = WIDTH - 1
            
            # Place marker
            if line_chars[idx] == " " or line_chars[idx] == "|":
                line_chars[idx] = f"{color}{symbol}{RESET}"
            else:
                # Collision: If they land on the SAME spot, it's a merge visually
                line_chars[idx] = f"\033[95mX{RESET}" # Magenta X for collision

            # Advance the seed
            length = get_len(val)
            active_seeds[seed_id] = val + length
            
            # Optional: Stop if val gets too huge for visualization
            if val > 4000:
                seeds_to_remove.append(seed_id)

        # Remove finished seeds
        for s in seeds_to_remove:
            del active_seeds[s]

        # Print the constructed line
        print("".join(line_chars))
        
        # Check if they have merged (values are equal)
        vals = list(active_seeds.values())
        if len(vals) > 1 and vals[0] == vals[1]:
             print(f"{'MERGE DETECTED!':^{WIDTH}}")
             break

if __name__ == "__main__":
    run_visualization()
