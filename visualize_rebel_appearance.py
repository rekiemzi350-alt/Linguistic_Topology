import sys

# --- Configuration ---
START_STEP = 83  # The moment the Rebel arrives
DURATION = 150   # How long to watch them
WIDTH = 70
CENTER = WIDTH // 2

# ANSI Colors
COLOR_TRUNK = "\033[94m" # Blue for Main Trunk
COLOR_REBEL = "\033[91m" # Red for Rebel
RESET = "\033[0m"

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
    # 1. Fast-Forward Main Trunk (Seed 0) to the Start Step
    val_trunk = 0
    history_trunk = [0]
    for _ in range(START_STEP):
        length = get_len(val_trunk)
        val_trunk += length
        history_trunk.append(val_trunk)
        
    # 2. Initialize State
    # Trunk is at its computed value
    # Rebel (Seed 83) enters at value 83
    active_seeds = {
        0: val_trunk,
        83: 83
    }
    
    print(f"--- Fast-Forwarding Main Trunk to Step {START_STEP} ---")
    print(f"Main Trunk Value: {val_trunk}")
    print(f"Rebel Seed Entry: 83")
    print("-" * WIDTH)
    print(f"{'EVEN (Left/Down)':>{CENTER-2}} | {'ODD (Right/Up)':<{CENTER-2}}")
    print("-" * WIDTH)

    # 3. Run Simulation
    for t in range(START_STEP, START_STEP + DURATION):
        line_chars = [" "] * WIDTH
        line_chars[CENTER] = "|"
        
        # Display Step Number on the far left (optional, but useful)
        # We'll just print it before the line or integrated? 
        # Let's keep the graph clean and just run.
        
        seeds_to_remove = []
        
        # Sort so 0 is processed before 83 (render order)
        for seed_id in sorted(active_seeds.keys()):
            val = active_seeds[seed_id]
            
            if seed_id == 0:
                color = COLOR_TRUNK
                symbol = "0"
            else:
                color = COLOR_REBEL
                symbol = "R"
                
            # --- Plotting ---
            is_odd = (val % 2 != 0)
            
            # Position Logic (Parity Wave)
            if is_odd:
                # Right Side
                base = CENTER + 2
                # Jitter helps separate them visually if they are close
                jitter = (val % 16) 
                idx = base + jitter
            else:
                # Left Side
                base = CENTER - 3
                jitter = (val % 16)
                idx = base - jitter
                
            if idx < 0: idx = 0
            if idx >= WIDTH: idx = WIDTH - 1
            
            # Place Marker
            if line_chars[idx] == " " or line_chars[idx] == "|":
                line_chars[idx] = f"{color}{symbol}{RESET}"
            else:
                # Collision
                line_chars[idx] = f"\033[95mX{RESET}"

            # Advance
            length = get_len(val)
            active_seeds[seed_id] = val + length
            
            # Determine if merged
            # Note: This checks if they *became* equal in this step
            # Real collision check requires comparing new values next frame, 
            # but comparing current values is correct for "are they at the same spot now?"
            
        # Print
        step_label = f"{t:<3}"
        print(step_label + "".join(line_chars))
        
        # Check for numerical merge
        vals = list(active_seeds.values())
        if len(vals) > 1 and vals[0] == vals[1]:
            print(f"{'!!! MERGE !!!':^{WIDTH}}")
            # Break or continue? 
            # The user wants to see them 'until they converge'.
            # They won't converge in 150 steps, but if they did, we'd see it.
            
if __name__ == "__main__":
    run_visualization()
