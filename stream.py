import streamlit as st
import streamlit.components.v1 as stc
import pandas as pd
from datetime import date, datetime
from dateutil import relativedelta
import pickle
import codecs


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

    chosen_date = st.date_input("Effective date", date.today())
    effective_date = chosen_date + relativedelta.relativedelta(months=1, day=1)
    st.write(effective_date)
    st.markdown("###")

    keywords = [x.strip() for x in st.text_input("Add keywords or phrases (Separate words, by comma)").split(",")]
    # st.multiselect(None, options = keywords, default = keywords)
    st.markdown("###")

    if st.button("Generate"):
        st.markdown("###")
        # st.write("check out this [ link ]( https://share.streamlit.io/mesmith027/streamlit_webapps/main/MC_pi/streamlit_app.py)")
        generate_links(effective_date, keys, keywords)
        # get_html()
        # get_from_html('pipeline/html/index.html')


def generate_links(date, sectors, keywords):
    with open('pipeline/model/clas.pkl', 'rb') as f:
        clas = pickle.load(f)
    
    st.write(clas)

    html_message = ""
    number = 1

    for row in clas.iterrows():
        check = 0
        if str(row[1][6]) == "nan" and str(row[1][9]) == "nan":
            pass
        elif str(row[1][6]) == "nan":
            if row[1][9] <= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1
        elif str(row[1][9]) == "nan":
            if row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1
        else:
            if row[1][9] <= date and row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1
        
        if check == 1:
            html_message += get_row_details(row, number)
    get_html_page(html_message)
    

def get_row_details(row, number):
    deposit = str(row[1][0])
    start_date = str(row[1][9])
    end_date = str(row[1][6])
    jcid = str(row[1][1])
    url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"
    file_link = url + row[0].replace("-", "/", 1)
    # column1 = "width: 260px;"
    # column2 = "width: 160px;"
    # column3 = "width: 245px;"
    # column4 = "width: 110px;"
    # column5 = "width: 222px;"

    html_column = "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td><a href=\"{}\">Download file</a></td></tr>".format(deposit, start_date, end_date, jcid, file_link)
    # html_code = '<h4>'+ str(number) + ". " + str(deposit)+ '</h4>'
    # st.markdown(html_code, unsafe_allow_html=True)
    # hyperlink = "["+ row[0] + "]" + "(" + file_link + ")"
    # st.write(deposit, start_date, end_date, hyperlink)

    return html_column


def keyword_search(text, keyword_list):
    if len(keyword_list) == 0:
        return True
    elif all(word.lower() in text.lower() for word in keyword_list):
        return True
    else:
        return False


def get_html_page(columns):
    column1 = "width: 260px;padding-left: 40px;"
    column2 = "width: 160px;"
    column3 = "width: 245px;"
    column4 = "width: 110px;text-align: right;"
    column5 = "width: 222px;text-align: right;padding-right: 62px;"

    html_code = "<div>\
                    <div>\
                        <table>\
                            <thead>\
                                <tr>\
                                    <th style=\"{}\">Deposit Number</th>\
                                    <th style=\"{}\">Start Date</th>\
                                    <th style=\"{}\">End Date</th>\
                                    <th style=\"{}\">JCID</th>\
                                    <th style=\"{}\">Link to File</th>\
                                </tr>\
                            </thead>\
                            <tbody>\
                                {}\
                            </tbody>\
                        </table>\
                    </div>\
                </div>".format(column1, column2, column3, column4, column5, columns)
    
    st.write(html_code, unsafe_allow_html=True)


def get_from_html(htmf_file):
     html_code = codecs.open(htmf_file, 'r')
     page = html_code.read()
     stc.html(page, width=700, height=500, scrolling=False)


def get_nice_date(raw_date):
    month_date = {
        1: "January",
        2: ""
    }


if __name__ == "__main__":
    main()
