# import pandas as pd
# def load_dataset(path=r"C:\Users\DELL\Desktop\Projects-1\dna_visualizer\dna_dataset500.csv"):
#     df = pd.read_csv(path)
#     df['Sequence'] = df['Sequence'].astype(str).str.strip().str.upper()
#     return df 
# def analyze_sequence(seq):
#     seq = seq.upper().strip()
#     valid_bases = set("ATGC")
#     if not set(seq).issubset(valid_bases):
#         return None  
#     freq = {base: seq.count(base) for base in "ATGC"}
#     length = len(seq)
#     gc_content = round((freq['G'] + freq['C']) / length * 100, 2)
#     return {"length": length, "freq": freq, "gc_content": gc_content}

# utils.py
import pandas as pd

# Load dataset
def load_dataset(path=r"C:\Users\DELL\Desktop\Projects-1\dna_visualizer\dna_dataset500.csv"):
    df = pd.read_csv(path)
    df['Sequence'] = df['Sequence'].astype(str).str.strip().str.upper()
    return df

# Analyze sequence
def analyze_sequence(seq):
    seq = seq.upper().strip()
    valid_bases = set("ATGC")
    if not set(seq).issubset(valid_bases):
        return None
    freq = {base: seq.count(base) for base in "ATGC"}
    length = len(seq)
    gc_content = round((freq['G'] + freq['C']) / length * 100, 2)
    return {"length": length, "freq": freq, "gc_content": gc_content}

# Get reverse complement
def reverse_complement(seq):
    complement = str.maketrans("ATGC", "TACG")
    return seq.upper().translate(complement)[::-1]
 
# Calculate AT/GC skew
def calculate_skew(seq):
    seq = seq.upper()
    a_count = seq.count("A")
    t_count = seq.count("T")
    g_count = seq.count("G")
    c_count = seq.count("C")
    at_skew = (a_count - t_count) / (a_count + t_count) if (a_count + t_count) > 0 else 0
    gc_skew = (g_count - c_count) / (g_count + c_count) if (g_count + c_count) > 0 else 0
    return {"AT_Skew": at_skew, "GC_Skew": gc_skew}