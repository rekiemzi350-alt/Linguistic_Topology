import sys

# English Number to Words (Simplified for relevant range)
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

def simulate_stepwise(max_steps=15):
    # Tracks the current position of every seed that has entered
    # Format: {seed_number: current_value}
    active_seeds = {}
    
    # History of positions to visualize tracks
    # Format: {seed_number: [path...]}
    history = {}

    print(f"{'Step':<5} | {'Active Seeds & Positions':<60} | {'New Merges'}")
    print("-" * 90)

    for t in range(max_steps):
        # 1. New Seed enters at this time step
        new_seed = t
        active_seeds[new_seed] = new_seed
        history[new_seed] = [new_seed]
        
        # 2. Move all active seeds forward
        # We need to snapshot current state to avoid updating a seed twice or using updated values
        current_positions = list(active_seeds.items())
        
        step_merges = []
        
        # Update positions
        next_positions = {}
        
        # Determine locations for this step
        # Note: In your description, "0 goes to 4 and 1 appears".
        # This implies:
        # T=0: 0 exists.
        # T=1: 0 moves to 4. 1 enters.
        # T=2: 0 moves to 8. 1 moves to 4. 2 enters.
        
        # Let's align with that:
        # at Step T, we process seeds 0 to T.
        # Seed T just entered (value T).
        # Seeds 0 to T-1 move forward.
        
        display_str = []
        
        for seed, current_val in active_seeds.items():
            if seed == t:
                # Just entered
                display_str.append(f"{seed}(start)")
                next_positions[seed] = seed
            else:
                # Move forward
                length = get_len(current_val)
                next_val = current_val + length
                next_positions[seed] = next_val
                history[seed].append(next_val)
                display_str.append(f"{seed}->{next_val}")

        active_seeds = next_positions

        # Check for merges (multiple seeds at same value)
        # Invert the map: value -> list of seeds
        location_map = {}
        for seed, val in active_seeds.items():
            if val not in location_map:
                location_map[val] = []
            location_map[val].append(seed)
            
        merge_msg = ""
        for val, seeds in location_map.items():
            if len(seeds) > 1:
                seeds.sort()
                merge_msg += f"[{', '.join(map(str, seeds))} @ {val}] "

        # Truncate display string for readability
        display_line = ", ".join(display_str)
        if len(display_line) > 60:
            display_line = display_line[:57] + "..."
            
        print(f"{t:<5} | {display_line:<60} | {merge_msg}")

simulate_stepwise(15)
