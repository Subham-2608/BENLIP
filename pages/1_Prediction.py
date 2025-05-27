import streamlit as st
import itertools
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from Bio.SeqIO import parse
import io
import pickle as pkl
import joblib
import wget

st.set_page_config( page_title="BENLiP", initial_sidebar_state="expanded", layout="wide")
col1, col2, col3 = st.columns([1.5, 20, 2])

with col1:
    st.image("static/images/icarlogo.png", width=150)

with col2:
    st.markdown("<h1 style='text-align:center;'> BENLiP: Bagging based Ensemble model to identify Nucleosome and Linker Positioning</h1>", unsafe_allow_html=True)

with col3:
    st.image("static/images/iasri-logo.png", width=150)

st.markdown("---")
st.text("")

@st.cache_resource
def load_model(model_url, model_name):
    if not os.path.exists(model_name):
        #st.info("Downloading model, please wait...")
        wget.download(model_url, model_name + ".pkl")
    model =  joblib.load(model_name + ".pkl")
    retrun model

def process_and_extract(fasta_file, feature_csv, output_csv):
    def one_hot_encode(seq):
        "One-hot encoding of DNA sequences."
        map = {'A': [1, 0, 0, 0], 'T': [0, 1, 0, 0], 'C': [0, 0, 1, 0], 'G': [0, 0, 0, 1], 'N': [0, 0, 0, 0]}
        return np.array([map.get(base, [0, 0, 0, 0]) for base in seq]).flatten()

    def calculate_gc_content(seq):
        "Calculate GC content of a DNA sequence."
        g_count = seq.count('G')
        c_count = seq.count('C')
        return 100 * (g_count + c_count) / len(seq)

    def calculate_tetra_nucleotide_frequency(seq, k_mer_set):
        "Calculate tetra-nucleotide frequency for a DNA sequence."
        k = 4
        freq_dict = {k_mer: 0 for k_mer in k_mer_set}  # Initialize with all possible k-mers
        for i in range(len(seq) - k + 1):
            k_mer = seq[i:i+k]
            if k_mer in freq_dict:
                freq_dict[k_mer] += 1
        return freq_dict

    # Generate universal k-mer set (all possible k-mers of length 4)
    bases = ['A', 'T', 'C', 'G']
    k_mer_set = ["".join(p) for p in itertools.product(bases, repeat=4)]

    data = []
    tetra_nucleotide_data = []
    gc_content_data = []
    for record in parse(io.StringIO(fasta_file.read().decode('UTF-8')), "fasta"):
        accession = record.id
        sequence = str(record.seq).upper()

        # One-hot encoding
        encoded_sequence = one_hot_encode(sequence)

        # Tetra-nucleotide frequency
        tetra_nuc_freq = calculate_tetra_nucleotide_frequency(sequence, k_mer_set)
        tetra_nucleotide_data.append([accession] + list(tetra_nuc_freq.values()))

        # GC content
        gc_content = calculate_gc_content(sequence)
        gc_content_data.append([accession, gc_content])

        # Combine accession and one-hot encoding
        data.append([accession] + encoded_sequence.tolist())

    one_hot_df = pd.DataFrame(data)
    one_hot_df.columns = ['Accession'] + [f'one_hot_encoding_{i+1}' for i in range(one_hot_df.shape[1] - 1)]

    tetra_nuc_df = pd.DataFrame(tetra_nucleotide_data)
    tetra_nuc_df.columns = ['Accession'] + k_mer_set  # Use k-mer names as column names

    gc_df = pd.DataFrame(gc_content_data, columns=['Accession', 'GC'])

    merged_df = pd.merge(one_hot_df, tetra_nuc_df, on='Accession')
    merged_df = pd.merge(merged_df, gc_df, on='Accession')

    scaler = MinMaxScaler()
    scaled_columns = [col for col in merged_df.columns if col in k_mer_set or col == 'GC']
    merged_df[scaled_columns] = scaler.fit_transform(merged_df[scaled_columns])

    # Read the feature CSV to filter columns
    feature_df = pd.read_csv(feature_csv)
    if 'Feature' not in feature_df.columns:
        raise ValueError("The CSV file must contain a column named 'feature'.")

    # Extract specified features
    feature_list = feature_df['Feature'].tolist()
    columns_to_extract = ['Accession'] + [col for col in feature_list if col in merged_df.columns]
    extracted_df = merged_df[columns_to_extract]

    #extracted_df.to_csv(output_csv, index=False)

    return extracted_df

st.markdown("**Instructions for Users:**")
st.markdown('''**1. File Format:** Provide the input file in .fasta format and the sequences should be of 147 bp length.  
            **2. Choose Species:** User should choose the relevant species for a sequence.  
            **3. Number of Inputs:** Users can provide multiple sequences from a particular species in a multifasta file at a time.  
            **4. Accession Name:** Accession name must be different for each sequence in the multifasta file.''')

class_names = {0: "linker", 1: "nucleosome"}

col1_1, col2_1 = st.columns([0.5, 1])

with col1_1:
    
    selected_feature = st.selectbox("Select Feature", ("C elegans", "Human", "Human 5' UTR", "Human Long Chromosome", "Human Promoter", "Melanogaster", "Melanogaster 5' UTR", "Melanogaster Long Chromosome", "Melanogaster Promoter", "Yeast Promoter", "Yeast Whole Genome"))
    upload_fasta = st.file_uploader("Upload Fasta File for Feature Extraction", type=["fasta"])

with col2_1:
    if upload_fasta is not None:
        result_df = process_and_extract(upload_fasta, "static/feature_lists/" + selected_feature + ".csv", "filtered_important_feature.csv")

        #with st.container:
        st.text("Extracted Features:")
        st.dataframe(result_df)
        #st.text(result_df)
        
        st.download_button("Download Extracted Features", data=result_df.to_csv(index=False).encode("utf-8"), file_name="extracted features.csv", mime="text/csv", icon=":material/download:")
        with st.spinner("Processing...", show_time=False):
            model = load_model("https://github.com/Subham-2608/BENLIP/raw/refs/heads/main/static/models/" + selected_feature.replace(" ", "%20") + ".pkl?download=", selected_feature)
            result_df['prediction'] = model.predict(result_df.loc[:,result_df.columns[1:]])
            result_df['pred_class'] = result_df['prediction'].map(class_names)
        predict_button = st.download_button("Prediction & Download", data=result_df.to_csv(columns=['Accession', 'pred_class'], index=False), file_name="prediction.csv", mime="text/csv", icon=":material/download:")

            


# print(result_df)

st.text("")
st.markdown("<div style='background-color:#32CD32; text-align:center'><p style='color:white'>Copyright © 2025 ICAR-Indian Agricultural Statistics Research Institute, New Delhi-110012. All rights reserved.</p></div>", unsafe_allow_html=True)
