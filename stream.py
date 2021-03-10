import streamlit as st
import pandas as pd
import datetime
import pickle

category_dict = {
    "COMMISSION PARITAIRE DES CONSTRUCTIONS METALLIQUE, MECANIQUE ET ELECTRIQUE": [111, []],
    "COMMISSION PARITAIRE DE L'INDUSTRIE CHIMIQUE": [116, []],
    "COMMISSION PARITAIRE DE L'INDUSTRIE ALIMENTAIRE": [118, []],
    "COMMISSION PARITAIRE POUR LE NETTOYAGE": [121, []],
    "COMMISSION PARITAIRE DE LA CONSTRUCTION": [124, []],
    "COMMISSION PARITAIRE DU TRANSPORT ET DE LA LOGISTIQUE": [140,
    ["SOUS-COMMISSION PARITAIRE POUR LES AUTOBUS ET AUTOCARS", "SOUS-COMMISSION PARITAIRE POUR LES TAXIS",
    "SOUS-COMMISSION PARITAIRE POUR LE TRANSPORT ROUTIER ET LA LOGISTIQUE POUR COMPTE DE TIERS",
    "SOUS-COMMISSION PARITAIRE POUR L'ASSISTANCE EN ESCALE DANS LES AEROPORTS",
    "SOUS-COMMISSION PARITAIRE POUR LE DEMENAGEMENT"]],
    "COMMISSION PARITAIRE AUXILIAIRE POUR EMPLOYES": [200, []],
    "COMMISSION PARITAIRE POUR EMPLOYES DE L'INDUSTRIE CHIMIQUE": [207, []],
    "COMMISSION PARITAIRE POUR EMPLOYES DES FABRICATIONS METALLIQUES": [209, []],
    "COMMISSION PARITAIRE POUR LES EMPLOYES DE L'INDUSTRIE ALIMENTAIRE": [220, []],
    "COMMISSION PARITAIRE POUR LES BANQUES": [310,
    ["SOUS-COMMISSION PARITAIRE DE L'EMPLOI DANS LE SECTEUR BANCAIRE (ABROGEE DEPUIS LE 28/12/2001)"]],
    "COMMISSION PARITAIRE DES GRANDES ENTREPRISES DE VENTE AU DETAIL": [311, []]
}

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
  
    categories = ()
    for category in category_dict:
        categories = categories + (category, )
    mode = st.selectbox("Select Category",categories)
    st.markdown("###")
    if len(category_dict[mode][1]) > 0:
        st.radio("Sub Category", category_dict[mode][1])
    else:
        st.write(mode)

    st.markdown("###")
    date = st.date_input("Effective date", datetime.date(2021,3,4))
    st.write(date)
    st.markdown("###")

    with open('pipeline/model/clas.pkl', 'rb') as f:
        clas = pickle.load(f)

    url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"
    
    for row in clas.iterrows():
        start_date = row[1][6]
        end_date = row[1][7]
        valid_date(start_date)
        valid_date(end_date)
        st.write(row[1][6])
        st.write(row[1][7])
        
        file_link = url + row[0].replace("-", "/", 1)

        st.write("["+ row[0] + "]" + "(" + file_link + ")")
        break
    st.write(clas)

    if st.button("Analyse"):
        st.write("check out this [ link ]( https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")

def valid_date(start_date):
    st.write(start_date[0:10])

if __name__ == "__main__":
    main()
