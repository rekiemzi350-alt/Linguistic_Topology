import pandas as pd
import numpy as np
import wave
import struct
import os
import glob

def process_soundtrack():
    # File patterns
    base_dir = "waveforms"
    files = [
        "waveform_level2_words_MASTER_Secret_Doctrine_Vol1.txt.csv",
        "waveform_level2_words_MASTER_Secret_Doctrine_Vol2.txt.csv",
        "waveform_level2_words_MASTER_Secret_Doctrine_Vol3.txt.csv",
        "waveform_level2_words_MASTER_Secret_Doctrine_Vol4.txt.csv"
    ]
    
    combined_data = []
    
    print("Reading and concatenating files...")
    for f in files:
        path = os.path.join(base_dir, f)
        if os.path.exists(path):
            print(f"Processing {f}...")
            df = pd.read_csv(path)
            # Assuming T1_Plot is the primary waveform column
            combined_data.append(df['T1_Plot'].values)
        else:
            print(f"Warning: {f} not found.")

    if not combined_data:
        print("No data found.")
        return

    # Concatenate all arrays
    full_waveform = np.concatenate(combined_data)
    
    print(f"Total data points: {len(full_waveform)}")
    
    # Save combined CSV for reference
    output_csv = "waveforms/combined_secret_doctrine_waveform.csv"
    pd.Series(full_waveform).to_csv(output_csv, header=["T1_Plot"], index_label="Index")
    print(f"Saved combined waveform to {output_csv}")

    # --- Sonification ---
    # Normalize to -1.0 to 1.0
    max_val = np.max(np.abs(full_waveform))
    if max_val == 0:
        max_val = 1
    normalized_wave = full_waveform / max_val
    
    def write_wav(filename, data, sample_rate):
        print(f"Writing {filename} at {sample_rate} Hz...")
        # Convert to 16-bit PCM
        # Clamp to -1..1 just in case
        data = np.clip(data, -1.0, 1.0)
        # Scale to 16-bit integer range
        int_data = (data * 32767).astype(np.int16)
        
        with wave.open(filename, 'w') as w:
            w.setnchannels(1) # Mono
            w.setsampwidth(2) # 2 bytes per sample (16-bit)
            w.setframerate(sample_rate)
            # Convert numpy array to bytes
            w.writeframes(int_data.tobytes())
        print(f"Saved {filename}")

    # 1. Raw Speed (Data as Samples)
    # 44100 Hz
    write_wav("waveforms/secret_doctrine_raw.wav", normalized_wave, 44100)
    
    # 2. Stretched "40 BPM Soundtrack" approximation
    # To "stretch along the axis", we can simply lower the playback sample rate 
    # OR interpolate. Standard players might not like low sample rates (e.g. 400Hz).
    # So we prefer interpolation (repetition) at 44100Hz.
    
    # Let's try a stretch factor that is significant.
    # If we want 40 "events" per minute -> 0.66 Hz frequency.
    # This implies we want to slow it down massively.
    # Let's try a 50x stretch.
    stretch_factor = 50
    print(f"Generating stretched WAV ({stretch_factor}x slow down)...")
    stretched = np.repeat(normalized_wave, stretch_factor)
    write_wav("waveforms/secret_doctrine_stretched_50x.wav", stretched, 44100)

if __name__ == "__main__":
    process_soundtrack()
