import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

def generate_graphs():
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.join(repo_dir, "baseline_results")
    graphs_dir = os.path.join(results_dir, "graphs")
    
    if not os.path.exists(graphs_dir):
        os.makedirs(graphs_dir)

    csv_files = glob.glob(os.path.join(results_dir, "*_waveform.csv"))
    print(f"Found {len(csv_files)} waveform files to plot.")

    # 1. Plot individual graphs
    print("Generating individual graphs...")
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            base_name = os.path.basename(csv_file).replace("_waveform.csv", "")
            
            plt.figure(figsize=(10, 6))
            plt.plot(df['Step'], df['WaveformValue'], marker='o', markersize=2, linestyle='-', linewidth=0.5, alpha=0.7)
            plt.title(f"Waveform: {base_name}")
            plt.xlabel("Step")
            plt.ylabel("Value (Peak/Valley)")
            plt.grid(True, alpha=0.3)
            
            output_path = os.path.join(graphs_dir, f"{base_name}.jpg")
            plt.savefig(output_path, dpi=100, format='jpg')
            plt.close()
        except Exception as e:
            print(f"Error plotting {csv_file}: {e}")

    # 2. Plot Synced Groups
    # We need to re-identify groups or parse the report, or just compare data again.
    # Comparing data is safer.
    print("Generating synced group comparison...")
    
    data_map = {} # (tail_tuple) -> list of (name, dataframe)
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            base_name = os.path.basename(csv_file).replace("_waveform.csv", "")
            
            # Get tail as signature
            if len(df) >= 10:
                tail = tuple(df['Value'].iloc[-10:].tolist())
                if tail not in data_map:
                    data_map[tail] = []
                data_map[tail].append((base_name, df))
        except:
            pass

    # Filter for groups with > 1 language
    synced_groups = {k: v for k, v in data_map.items() if len(v) > 1}
    
    if synced_groups:
        num_groups = len(synced_groups)
        fig, axes = plt.subplots(num_groups, 1, figsize=(12, 4 * num_groups), constrained_layout=True)
        if num_groups == 1:
            axes = [axes]
        
        for ax, (tail, members) in zip(axes, synced_groups.items()):
            names = [m[0] for m in members]
            display_names = ", ".join(names[:5])
            if len(names) > 5:
                display_names += f" and {len(names)-5} others"
            
            ax.set_title(f"Synced Group: {display_names}")
            ax.set_xlabel("Step")
            ax.set_ylabel("Waveform Value")
            
            colors = cm.rainbow(np.linspace(0, 1, len(members)))
            
            for (name, df), color in zip(members, colors):
                # Add a small jitter to visibility if they overlap perfectly
                # But strict overlap is the point. 
                # We'll use dashed lines for some to show underlying ones?
                # Or just plot them.
                ax.plot(df['Step'], df['WaveformValue'], label=name, alpha=0.7, linewidth=1)
            
            # If too many legends, simplify
            if len(names) <= 10:
                ax.legend()
            else:
                ax.text(0.02, 0.95, f"{len(names)} Languages Overlapping", transform=ax.transAxes, verticalalignment='top')

        output_path = os.path.join(graphs_dir, "Synced_Groups_Comparison.jpg")
        plt.savefig(output_path, dpi=150, format='jpg')
        plt.close()
        print(f"Saved Synced_Groups_Comparison.jpg")

    print("Done.")

if __name__ == "__main__":
    generate_graphs()
