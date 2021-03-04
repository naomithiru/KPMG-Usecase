import streamlit as st
import pandas as pd
import datetime
import pickle


def main():
    page_bg_img = '''
    <style>
        body {
            background-image: url("https://images.unsplash.com/photo-1521587760476-6c12a4b040da?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=1050&q=80");
            background-size: cover;
        }
    </style>
    '''

    st.title("KPMG")
    st.markdown("###")
    st.header("Legal document")
    # st.markdown(page_bg_img, unsafe_allow_html=True)
    category_dict = {
        "None": [],
        "Crime": ["murder", "theft", "destruction"],
        "Salary": ["starting", "increase", "commission"],
        "Contract": ["start date", "end date", "modification date"]
    }
    categories = ()
    for category in category_dict:
        categories = categories + (category, )
    mode = st.selectbox("Select Category",categories)
    st.markdown("###")
    if len(category_dict[mode]) > 0:
        st.radio("Sub Category", category_dict[mode])
    st.markdown("###")
    date = st.date_input("Effective date", datetime.date(2021,3,4))
    st.write(date)
    st.markdown("###")
    with open('pipeline/model/clas.pkl', 'rb') as f:
        clas = pickle.load(f)
    
    for row in clas.iterrows():
        start_date = row[1][6]
        end_date = row[1][7]
        valid_date(start_date)
        valid_date(end_date)
        st.write(row[1][6])
        st.write(row[1][7])
        break
    st.write(clas)

    st.button("Analyse")

def valid_date(start_date):
    st.write(start_date[0:10])

if __name__ == "__main__":
    main()
