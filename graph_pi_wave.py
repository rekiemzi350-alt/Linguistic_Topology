# The first 100 digits of Pi
pi_digits = "3141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067"

# Create a 2D grid (10 rows for 0-9, columns for digits)
rows = 10
cols = len(pi_digits)
grid = [[" " for _ in range(cols)] for _ in range(rows)]

# Fill the grid
for x, d in enumerate(pi_digits):
    y = 9 - int(d) # Invert so 9 is at the top
    grid[y][x] = "•"

print("\n--- PI DIGIT WAVEFORM (0-9) ---")
print("Top line is 9, bottom line is 0.\n")

# Print the grid with y-axis labels
for y in range(rows):
    label = 9 - y
    line = "".join(grid[y])
    print(f"{label} | {line}")

print("  " + "-" * (cols + 3))
print("  " + "Position in Pi (1-100) ->")
