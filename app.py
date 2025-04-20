import streamlit as st
import pandas as pd
from io import BytesIO

# --- Utils (inlined) -------------------------------------------

def match_by_similarity(urls1, urls2, threshold=0.8):
    # placeholder: implement fuzzy matching or whatever you need
    from difflib import SequenceMatcher
    def similar(a, b):
        return SequenceMatcher(None, a, b).ratio()
    matches = []
    for u1 in urls1:
        best = max(urls2, key=lambda u2: similar(u1, u2))
        score = similar(u1, best)
        if score >= threshold:
            matches.append((u1, best, score))
    return matches


def align_by_sku(df1, df2, how="outer"):
    # basic merge on SKU
    df1 = df1.copy()
    df2 = df2.copy()
    df1['SKU'] = df1['SKU'].astype(str).str.strip()
    df2['SKU'] = df2['SKU'].astype(str).str.strip()
    return pd.merge(df1, df2, on='SKU', how=how, suffixes=('_sheet1','_sheet2'))

# SIM_AVAILABLE flag
try:
    from rapidfuzz import fuzz
    SIM_AVAILABLE = True
except ImportError:
    SIM_AVAILABLE = False

# --- Streamlit app --------------------------------------------

st.set_page_config(page_title="CSV Aligner", page_icon="🗂️", layout="centered")
st.title("🗂️ Align two CSVs by SKU")
st.write(
    "Upload two CSV files that each contain **`URL`** and **`SKU`** columns. "
    "The app will merge them on **SKU** and let you download the result."
)

# File upload
file1 = st.file_uploader("Sheet 1 CSV", type="csv", key="file1")
file2 = st.file_uploader("Sheet 2 CSV", type="csv", key="file2")
merge_type = st.radio(
    "Merge behavior for SKUs not found in both files",
    options=["outer","inner"],
    format_func=lambda x: "Keep all SKUs (outer merge)" if x=="outer" else "Only SKUs in both files (inner merge)",
    horizontal=True,
)
run_btn = st.button("🔄 Align CSVs", disabled=not (file1 and file2))

# Alignment logic
if run_btn:
    try:
        df1 = pd.read_csv(file1)[['URL','SKU']]
        df2 = pd.read_csv(file2)[['URL','SKU']]
        result = align_by_sku(df1, df2, how=merge_type)

        st.success(f"Merge complete – {len(result):,} rows")
        st.subheader("Preview")
        st.dataframe(result.head(50), use_container_width=True)

        # Download
        csv_bytes = result.to_csv(index=False).encode('utf-8')
        st.download_button(
            "⬇️ Download aligned CSV",
            data=csv_bytes,
            file_name="aligned_data.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error: {e}")

