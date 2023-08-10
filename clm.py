import streamlit as st
import pandas as pd
import numpy as np

def highlight_cells(val):
    return 'background-color: lightgray; text-align: center'

def apply_styles(data):
    # Create an empty style DataFrame with the same shape as the data
    style_df = pd.DataFrame('', index=data.index, columns=data.columns)
    # Fill in the cells with the desired styles
    style_df[:] = np.where((data.notnull()) & (data.applymap(np.isreal)), highlight_cells, '')
    return style_df

def main():
    st.title("CSV Data Viewer")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a pandas DataFrame
        data = pd.read_csv(uploaded_file)

        # Apply the styles to the DataFrame
        styled_data = data.style.apply(apply_styles, axis=None)

        # Display the styled DataFrame
        st.write("Displaying uploaded data:")
        st.dataframe(styled_data)

if __name__ == "__main__":
    main()
