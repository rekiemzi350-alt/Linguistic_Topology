import math

def plot_fibonacci_convergence():
    print("\n--- 1. THE CONVERGENCE WAVE (Mathematical 'Spiraling In') ---")
    print("The ratio of Fibonacci numbers swings High/Low around 1.618...")
    print("Notice how the wave gets tighter and tighter (Damping).\n")
    
    phi = 1.61803398875
    a, b = 1, 1
    
    # We'll plot the first 15 steps
    for i in range(1, 16):
        ratio = b / a
        diff = ratio - phi
        
        # Scale for visualization
        bar_len = int(abs(diff) * 100)
        
        if diff > 0:
            # Over-shoot (Right side)
            print(f"{i:2} ({ratio:5.3f}) | 1.618 {'+' * bar_len}")
        else:
            # Under-shoot (Left side)
            print(f"{i:2} ({ratio:5.3f}) | {'-' * bar_len} 1.618")
        
        # Next Fibonacci number
        a, b = b, a + b

def plot_golden_spiral():
    print("\n\n--- 2. THE GEOMETRIC SPIRAL (Phyllotaxis) ---")
    print("Plotting points separated by the Golden Angle (137.5 degrees).")
    print("This is how nature 'spirals' leaves to maximize sun exposure.\n")
    
    width = 60
    height = 30
    grid = [[" " for _ in range(width)] for _ in range(height)]
    
    center_x = width // 2
    center_y = height // 2
    
    # Golden Angle in radians
    golden_angle = math.pi * (3 - math.sqrt(5)) 
    
    for i in range(150):
        # Distance from center grows with square root of index (to keep density even)
        r = 1.2 * math.sqrt(i)
        theta = i * golden_angle
        
        # Polar to Cartesian
        x = r * math.cos(theta)
        y = r * math.sin(theta) * 0.5 # Scale y for terminal aspect ratio
        
        # Map to grid
        plot_x = int(center_x + x)
        plot_y = int(center_y + y)
        
        if 0 <= plot_x < width and 0 <= plot_y < height:
            grid[plot_y][plot_x] = "•"
            
    # Print grid
    for row in grid:
        print("".join(row))

if __name__ == "__main__":
    plot_fibonacci_convergence()
    plot_golden_spiral()
