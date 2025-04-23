import streamlit as st
from scanner import scan_username
from utils import save_results, export_to_pdf

st.set_page_config(
    page_title="AliasWolf",
    page_icon="photos/icon.png",
    layout="wide"
)
import base64

def get_base64_of_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


st.title("🐺 AliasWolf - Username Scanner")

# Check if scan results are already stored in session state
if "results_df" not in st.session_state:
    st.session_state.results_df = None

username = st.text_input("Enter the username to scan:")

# If user clicks the "Start Scan" button
if st.button("Start Scan"):
    if username:
        with st.spinner('Scanning the web... please wait...'):
            st.session_state.results_df = scan_username(username)  # Save results to session state
        
        st.success('Scan completed successfully!')

# Check if results are available to display
if st.session_state.results_df is not None:
    results_df = st.session_state.results_df

    # Display the dataframe
    st.dataframe(results_df, use_container_width=True)

    st.title("Download Results")
    st.download_button(
            label="Download as CSV",
            data=save_results(results_df, filetype="csv"),
            file_name=f"{username}_scan.csv",
            mime="text/csv"
        )

    st.download_button(
            label="Download as Excel",
            data=save_results(results_df, filetype="excel"),
            file_name=f"{username}_scan.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )    

    st.download_button(
            label="Download as PDF",
            data=export_to_pdf(results_df),
            file_name=f"{username}_scan.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Please enter a username and start the scan!")

# 🛠️ Custom CSS to expand column width nicely
encoded_image = get_base64_of_image('photos/icon.png')

st.markdown(
    f"""
    <style>
        div[data-testid="stDataFrame"] {{
            width: 100% !important;
        }}
        div[data-testid="stDataFrame"] table {{
            width: 100% !important;
            table-layout: fixed;
        }}
        div[data-testid="stDataFrame"] th, div[data-testid="stDataFrame"] td {{
            min-width: 150px;
            max-width: 400px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .stApp {{
            background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
                        url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
