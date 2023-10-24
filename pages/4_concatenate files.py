
def get_file(key_number):
    uploaded_file = st.file_uploader("Choose a file", key = key_number)
        
    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file)

        return df
    
def concat_files():
    
    df1 = get_file(1)

    if df1 is None:
        st.warning("Pick a file")
    else:
        st.dataframe(df1)

    df2 = get_file(2)

    if df2 is None:
        st.warning("Pick a file")
    else:
        st.dataframe(df2)

    if df1 is None:
        st.warning("At least one dataframe is missing")
    elif df2 is None:
        st.warning("At least one dataframe is missing")
    else:
        df3 = pd.concat([df1, df2])
        st.dataframe(df3)

        df3_csv = df3.to_csv(index=False).encode('utf-8')

        st.download_button("Press to Download Concatenated file.",
                            df3_csv,
                            "concatenated_file.csv",
                            "text/csv",
                            key='download-csv'
                            )


# pick_utility = st.radio('Select a Utility', options = ['Concatenate Files', 'Load CSV File'])

# if pick_utility == 'Concatenate Files':
#         concat_files()

# if pick_utility == 'Load CSV File':
#     st.subheader("Coming Soon!")