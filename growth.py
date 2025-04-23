import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page config
st.set_page_config(page_title="📊 Data Sweeper", layout='wide')

# Custom CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }
    .css-18e3th9 {
        padding: 2rem;
    }
    .stButton > button {
        background-color: #00BFFF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    .stDownloadButton > button {
        background-color: #28a745;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and description
st.title("📁 Datasweeper Sterling Integrator")
st.markdown("**🔄 Transform your files between CSV and Excel formats with built-in data cleaning and visualization.**<br>🚀 *Created by Amna Rehmani for Quarter 3 project*", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📂 Upload your file (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.write(f"### 👀 Preview of `{file.name}`")
        st.dataframe(df.head())

        # Data cleaning
        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean data for `{file.name}`"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🧼 Remove Duplicates from `{file.name}`"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")

            with col2:
                if st.button(f"🧮 Fill Missing Values for `{file.name}`"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled with column mean!")

        # Column selector
        st.subheader("📌 Select Columns to Keep")
        columns = st.multiselect(f"🗂 Choose columns for `{file.name}`", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"📉 Show bar chart for `{file.name}`"):
            numeric_cols = df.select_dtypes(include='number')
            if not numeric_cols.empty:
                st.bar_chart(numeric_cols.iloc[:, :2])
            else:
                st.warning("⚠️ No numeric columns to display!")

        # File conversion
        st.subheader("📁 Convert & Download")
        conversion_type = st.radio(f"📤 Convert `{file.name}` to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert and Download `{file.name}`"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                new_filename = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                new_filename = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"⬇️ Download `{new_filename}`",
                data=buffer,
                file_name=new_filename,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")
