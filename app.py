# app.py

import streamlit as st
from scanner import scan_username
from utils import save_results, export_to_pdf

st.set_page_config(page_title="AliasWolf", page_icon="🐺", layout="wide")

st.title("🐺 AliasWolf - Username Scanner")

username = st.text_input("Enter the username to scan:")

if st.button("Start Scan"):
    if username:
        with st.spinner('Scanning the web... please wait...'):
            results_df = scan_username(username)
        
        st.success('Scan completed successfully!')
        st.dataframe(results_df)
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
        st.warning("Please enter a username before scanning!")
