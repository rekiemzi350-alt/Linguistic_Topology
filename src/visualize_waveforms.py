import sys
import os

try:
    import pandas as pd
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ImportError:
    print("Error: Required libraries 'pandas' and 'plotly' are missing.")
    sys.exit(1)

def visualize_csv(csv_path):
    print(f"Visualizing {csv_path}...")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error: {e}")
        return

    base_name = os.path.basename(csv_path)
    output_html = f"graph_{base_name}.html"
    
    # ---------------------------------------------------------
    # TYPE 1: ATOMIC (LETTERS)
    # ---------------------------------------------------------
    if 'Char' in df.columns:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['Sequence'], y=df['Plot_Y'],
            mode='lines', fill='tozeroy',
            name='Atomic Value',
            line=dict(color='#00FFFF', width=1)
        ))
        fig.update_layout(
            title=f"Atomic Waveform (Letters): {base_name}",
            template="plotly_dark",
            yaxis_title="Odd (+)/Even (-)"
        )

    # ---------------------------------------------------------
    # TYPE 2: MOLECULAR (WORDS - Master & Categories)
    # ---------------------------------------------------------
    elif 'Word' in df.columns:
        # Dual Plot: Track 1 (Sum Parts) vs Track 2 (Weighted)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=("Track 1: Sum of Parts (Atomic Sum)", 
                                            "Track 2: Weighted Sum (Rarity Factor)"))
        
        # Track 1
        fig.add_trace(go.Scatter(
            x=df['Sequence'], y=df['T1_Plot'],
            mode='markers+lines', name='Track 1',
            marker=dict(size=6, color=df['T1_Plot'], colorscale='Cividis'),
            line=dict(width=1, color='rgba(255,255,255,0.3)'),
            text=df['Word'], hovertemplate="<b>%{text}</b><br>Val: %{y}<extra></extra>"
        ), row=1, col=1)

        # Track 2
        fig.add_trace(go.Scatter(
            x=df['Sequence'], y=df['T2_Plot'],
            mode='markers+lines', name='Track 2',
            marker=dict(size=6, color=df['T2_Plot'], colorscale='Viridis'),
            line=dict(width=1, color='rgba(255,255,255,0.3)'),
            text=df['Word'], hovertemplate="<b>%{text}</b><br>Val: %{y:.2f}<extra></extra>"
        ), row=2, col=1)

        fig.update_layout(
            title=f"Molecular Waveform (Words): {base_name}",
            template="plotly_dark",
            height=800
        )

    # ---------------------------------------------------------
    # TYPE 3: STRUCTURAL (SENTENCES)
    # ---------------------------------------------------------
    elif 'Complexity' in df.columns:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            subplot_titles=("Structure Track 1", "Structure Track 2"))
        
        # Color by Mode (Conversation = Gold, Narrative = Blue)
        colors = df['Mode'].map({'Conversation': '#FFD700', 'Narrative': '#1E90FF'})

        fig.add_trace(go.Bar(
            x=df['Sequence'], y=df['T1_Plot'],
            name='Track 1', marker_color=colors
        ), row=1, col=1)

        fig.add_trace(go.Bar(
            x=df['Sequence'], y=df['T2_Plot'],
            name='Track 2', marker_color=colors
        ), row=2, col=1)

        fig.update_layout(
            title=f"Structural Waveform (Sentences): {base_name}<br><span style='font-size:12px;color:#FFD700'>Yellow=Conversation</span>, <span style='font-size:12px;color:#1E90FF'>Blue=Narrative</span>",
            template="plotly_dark",
            height=800
        )

    else:
        print("Unknown CSV format.")
        return

    fig.write_html(output_html)
    print(f"  > Graph Saved: {output_html}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize_waveforms.py <csv_file1> ...")
    else:
        for f in sys.argv[1:]:
            visualize_csv(f)