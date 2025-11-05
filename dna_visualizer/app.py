# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# from utils import load_dataset, analyze_sequence
# st.set_page_config(page_title="DNA Sequence Visualizer", layout="centered")
# st.title("🧬 DNA Sequence Visualizer & Analyzer")
# st.subheader("Loading DNA Dataset")
# try: 
#     dataset = load_dataset() 
#     st.dataframe(dataset)
#     st.success("Dataset loaded successfully!")
# except Exception as e:
#     st.error(f"Could not load dataset: {e}")
#     dataset = None

# #Single sequence
# st.subheader("Single Sequence Analysis")
# if dataset is not None and not dataset.empty:
#     seq_id = st.selectbox("Select a sequence ID", dataset["Sequence_ID"])
#     dna_seq = dataset.loc[dataset["Sequence_ID"] == seq_id, "Sequence"].values[0]
#     analysis = analyze_sequence(dna_seq)    
#     if analysis is None:
#         st.error("Invalid DNA sequence! Only A, T, G, C allowed.")
#     else:
#         st.success("DNA sequence is valid.")
#         st.markdown(f"Sequence: {dna_seq[:80]}{'...' if analysis['length'] > 80 else ''}")
#         st.write(f"Length: {analysis['length']}")
#         st.write(f"GC Content: {analysis['gc_content']}%")
#         st.write(f"Base counts: {analysis['freq']}")

# #Multiple sequence
# st.subheader("Multiple Sequence Analysis")
# if dataset is not None and not dataset.empty:
#     if st.checkbox("Analyze all sequences"):
#         summary_data = []
#         for _, row in dataset.iterrows():
#             res = analyze_sequence(row["Sequence"])
#             if res:
#                 summary_data.append({
#                     "Sequence_ID": row["Sequence_ID"],
#                     "Length": res["length"],
#                     "GC_Content": res["gc_content"],
#                     "A_Count": res["freq"]["A"],
#                     "T_Count": res["freq"]["T"],
#                     "G_Count": res["freq"]["G"],
#                     "C_Count": res["freq"]["C"]
#                 })
#         summary_df = pd.DataFrame(summary_data)
#         st.dataframe(summary_df)

#         st.subheader("Visualizations")
#         avg_counts = summary_df[["A_Count","T_Count","G_Count","C_Count"]].mean()
#         fig, ax = plt.subplots()
#         avg_counts.plot(kind="bar", ax=ax, color=["skyblue","orange","green","red"])
#         ax.set_ylabel("Average Base Count")
#         ax.set_title("Average Base Composition")
#         st.pyplot(fig)

#         fig2, ax2 = plt.subplots()
#         ax2.hist(summary_df["GC_Content"], bins=10, color="purple", alpha=0.7)
#         ax2.set_xlabel("GC Content (%)")
#         ax2.set_ylabel("Number of Sequences")
#         st.pyplot(fig2)

#         st.download_button(
#             "Download CSV",
#             data=summary_df.to_csv(index=False),
#             file_name="dna_analysis.csv",
#             mime="text/csv"
#         )

# #Motif 
# st.subheader("Motif/Subsequence Search")
# if dataset is not None and not dataset.empty:
#     motif = st.text_input("Enter a DNA motif (e.g., ATG)")
#     if motif:
#         motif_results = []
#         motif = motif.upper()
#         for _, row in dataset.iterrows():
#             count = row["Sequence"].count(motif)
#             if count > 0:
#                 motif_results.append({"Sequence_ID": row["Sequence_ID"], "Motif_Count": count})
#         if motif_results:
#             st.dataframe(pd.DataFrame(motif_results))
#         else:
#             st.warning("Motif not found in any sequence")





import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import load_dataset, analyze_sequence, reverse_complement, calculate_skew
st.set_page_config(page_title="DNA Sequence Visualizer", layout="centered")
st.title("🧬 DNA Sequence Visualizer & Analyzer")

#LoadING Dataset
st.subheader("Loading DNA Dataset")
try:
    dataset = load_dataset()
    st.dataframe(dataset)
    st.success("Dataset loaded successfully!")
except Exception as e:
    st.error(f"Could not load dataset: {e}")
    dataset = None

#Single Sequence Analysis
st.subheader("Single Sequence Analysis")
if dataset is not None and not dataset.empty:
    seq_id = st.selectbox("Select a sequence ID", dataset["Sequence_ID"])
    dna_seq = dataset.loc[dataset["Sequence_ID"] == seq_id, "Sequence"].values[0]
    analysis = analyze_sequence(dna_seq)   
    if analysis is None:
        st.error("Invalid DNA sequence! Only A, T, G, C allowed.")
    else:
        st.success("DNA sequence is valid.")
        st.markdown(f"Sequence: {dna_seq[:80]}{'...' if analysis['length'] > 80 else ''}")
        st.write(f"Length: {analysis['length']}")
        st.write(f"GC Content: {analysis['gc_content']}%")
        st.write(f"Base counts: {analysis['freq']}")

#Multiple Sequence Analysis
st.subheader("Multiple Sequence Analysis")
if dataset is not None and not dataset.empty:
    if st.checkbox("Analyze all sequences"):
        summary_data = []
        for _, row in dataset.iterrows():
            res = analyze_sequence(row["Sequence"])
            if res:
                summary_data.append({
                    "Sequence_ID": row["Sequence_ID"],
                    "Length": res["length"],
                    "GC_Content": res["gc_content"],
                    "A_Count": res["freq"]["A"],
                    "T_Count": res["freq"]["T"],
                    "G_Count": res["freq"]["G"],
                    "C_Count": res["freq"]["C"]
                })
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(summary_df)
        st.subheader("Base Composition")
        avg_counts = summary_df[["A_Count","T_Count","G_Count","C_Count"]].mean()
        fig, ax = plt.subplots()
        avg_counts.plot(kind="bar", ax=ax, color=["skyblue","orange","green","red"])
        ax.set_ylabel("Average Base Count")
        ax.set_title("Average Base Composition")
        st.pyplot(fig)
        st.subheader("GC Content Distribution")
        fig2, ax2 = plt.subplots()
        ax2.hist(summary_df["GC_Content"], bins=10, color="purple", alpha=0.7)
        ax2.set_xlabel("GC Content (%)")
        ax2.set_ylabel("Number of Sequences")
        st.pyplot(fig2)
        st.download_button(
            "Download CSV",
            data=summary_df.to_csv(index=False),
            file_name="dna_analysis.csv",
            mime="text/csv"
        )

#Motif/Subsequence Search
st.subheader("Motif/Subsequence Search")
if dataset is not None and not dataset.empty:
    motif = st.text_input("Enter a DNA motif (e.g., ATG)")
    if motif:
        motif_results = []
        motif = motif.upper()
        for _, row in dataset.iterrows():
            count = row["Sequence"].count(motif)
            if count > 0:
                motif_results.append({"Sequence_ID": row["Sequence_ID"], "Motif_Count": count})
        if motif_results:
            st.dataframe(pd.DataFrame(motif_results))
        else:
            st.warning("Motif not found in any sequence")

#Reverse Complement
st.subheader("Reverse Complement")
if dataset is not None and not dataset.empty:
    seq_id_rc = st.selectbox("Select a sequence for reverse complement", dataset["Sequence_ID"], key="rc")
    dna_seq_rc = dataset.loc[dataset["Sequence_ID"] == seq_id_rc, "Sequence"].values[0]
    rc_seq = reverse_complement(dna_seq_rc)
    st.markdown(f"Original: {dna_seq_rc[:80]}{'...' if len(dna_seq_rc) > 80 else ''}")
    st.markdown(f"Reverse Complement: {rc_seq[:80]}{'...' if len(rc_seq) > 80 else ''}")

#Interactive GC Content Plot
st.subheader("Interactive GC Content Plot")
if dataset is not None and not dataset.empty:
    selected_seqs = st.multiselect("Select sequences for GC content plot", dataset["Sequence_ID"])
    if selected_seqs:
        gc_data = []
        for sid in selected_seqs:
            seq = dataset.loc[dataset["Sequence_ID"] == sid, "Sequence"].values[0]
            gc = analyze_sequence(seq)["gc_content"]
            gc_data.append({"Sequence_ID": sid, "GC_Content": gc})
        gc_df = pd.DataFrame(gc_data)
        fig, ax = plt.subplots()
        ax.bar(gc_df["Sequence_ID"], gc_df["GC_Content"], color="green")
        ax.set_ylabel("GC Content (%)")
        ax.set_title("GC Content of Selected Sequences")
        st.pyplot(fig)

#AT/GC Skew Analysis
st.subheader("AT/GC Skew Analysis")
if dataset is not None and not dataset.empty:
    skew_data = []
    for _, row in dataset.iterrows():
        skews = calculate_skew(row["Sequence"])
        skew_data.append({
            "Sequence_ID": row["Sequence_ID"],
            "AT_Skew": skews["AT_Skew"],
            "GC_Skew": skews["GC_Skew"]
        }) 
    skew_df = pd.DataFrame(skew_data)
    st.dataframe(skew_df)
    fig2, ax2 = plt.subplots()
    ax2.scatter(skew_df["AT_Skew"], skew_df["GC_Skew"], color="purple")
    ax2.set_xlabel("AT Skew")
    ax2.set_ylabel("GC Skew")
    ax2.set_title("AT/GC Skew Scatter Plot")
    st.pyplot(fig2)