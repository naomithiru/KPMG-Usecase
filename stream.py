import streamlit as st
import pandas as pd
from datetime import date, datetime
from dateutil import relativedelta
import pickle


category_dict = {
    111: "COMMISSION PARITAIRE DES CONSTRUCTIONS METALLIQUE, MECANIQUE ET ELECTRIQUE",
    116: "COMMISSION PARITAIRE DE L'INDUSTRIE CHIMIQUE",
    118: "COMMISSION PARITAIRE DE L'INDUSTRIE ALIMENTAIRE",
    121: "COMMISSION PARITAIRE POUR LE NETTOYAGE",
    124: "COMMISSION PARITAIRE DE LA CONSTRUCTION",
    140: "COMMISSION PARITAIRE DU TRANSPORT ET DE LA LOGISTIQUE",
    140.01: "SOUS COMMISSION PARITAIRE POUR LES AUTOBUS ET AUTOCARS",
    140.02: "SOUS COMMISSION PARITAIRE POUR LES TAXIS",
    140.03: "SOUS COMMISSION PARITAIRE POUR LE TRANSPORT ROUTIER ET LA LOGISTIQUE POUR COMPTE DE TIERS",
    140.04: "SOUS COMMISSION PARITAIRE POUR L'ASSISTANCE EN ESCALE DANS LES AEROPORTS",
    140.05: "SOUS COMMISSION PARITAIRE POUR LE DEMENAGEMENT",
    200: "COMMISSION PARITAIRE AUXILIAIRE POUR EMPLOYES",
    207: "COMMISSION PARITAIRE POUR EMPLOYES DE L'INDUSTRIE CHIMIQUE",  
    209: "COMMISSION PARITAIRE POUR EMPLOYES DES FABRICATIONS METALLIQUES", 
    220: "COMMISSION PARITAIRE POUR LES EMPLOYES DE L'INDUSTRIE ALIMENTAIRE", 
    310: "COMMISSION PARITAIRE POUR LES BANQUES", 
    310.01: "SOUS COMMISSION PARITAIRE DE L'EMPLOI DANS LE SECTEUR BANCAIRE (ABROGEE DEPUIS LE 28/12/2001)",
    311: "COMMISSION PARITAIRE DES GRANDES ENTREPRISES DE VENTE AU DETAIL"
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
        category_name = str(category) + "- " + category_dict[category]
        categories = categories + (category_name, )
    st.markdown("###")

    selection = st.multiselect("Select sectors", list(categories))
    keys = [sector.split("-")[0].lstrip() for sector in selection]
    st.markdown("###")

    chosen_date = st.date_input("Effective date", date(2021, 4, 10))
    effective_date = chosen_date + relativedelta.relativedelta(months=1, day=1)
    st.write(effective_date)
    st.markdown("###")

    keywords = [x.strip() for x in st.text_input("Add keywords or phrases (Separate words, by comma)").split(",")]
    # st.multiselect(None, options = keywords, default = keywords)
    st.markdown("###")

    if st.button("Generate"):
        # st.write("check out this [ link ]( https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
        generate_links(effective_date, keys, keywords)


def valid_date(start_date):
    st.write(start_date[0:10])


def generate_links(date, sectors, keywords):
    with open('pipeline/model/clas_newer.pkl', 'rb') as f:
        clas = pickle.load(f)

    for row in clas.iterrows():
        if str(row[1][6]) == "nan" and str(row[1][9]) == "nan":
            pass
        elif str(row[1][6]) == "nan":
            if row[1][9] <= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                print_details(row)
        elif str(row[1][9]) == "nan":
            if row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                print_details(row)
        else:
            if row[1][9] <= date and row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                print_details(row)


def print_details(row):
    deposit = row[1][0]
    start_date = row[1][9]
    end_date = row[1][6]
    url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"
    file_link = url + row[0].replace("-", "/", 1)
    hyperlink = "["+ row[0] + "]" + "(" + file_link + ")"
    st.write(deposit, start_date, end_date, hyperlink)



def date_format(date):
    pass


def keyword_search(text, keyword_list):
    if len(keyword_list) == 0:
        return True
    elif all(word.lower() in text.lower() for word in keyword_list):
        return True
    else:
        return False


if __name__ == "__main__":
    main()
