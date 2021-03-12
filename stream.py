import streamlit as st
import streamlit.components.v1 as stc
from datetime import date, datetime
from dateutil import relativedelta
import pickle
import codecs
import pathlib


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
            background-image: url("https://pimmedia.egger.com/l/decor/U775_9/s/Detail/f/881x513/8803438034974");
            background-size: cover;
        }
    </style>
    '''
    # fname = pathlib.Path('pipeline/model/clas.pkl')
    update = open('pipeline/model/update.txt', 'r')
    update_lines = update.readlines()
    # last_update = datetime.fromtimestamp(fname.stat().st_mtime)
    update_html = "<h4 style=\"text-align: right; color: green;\">{}<br><br>{}</h4>".format(update_lines[0], update_lines[1])
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.markdown(update_html, unsafe_allow_html=True)
    st.title("Partena CLA Monitor")
    st.markdown("###")
    st.header("Legal document")

    categories = ()
    for category in category_dict:
        category_name = str(category) + "- " + category_dict[category]
        categories = categories + (category_name, )
    st.markdown("###")

    selection = st.multiselect("Select sectors", list(categories))
    keys = [sector.split("-")[0].lstrip() for sector in selection]
    st.markdown("###")

    chosen_date = st.date_input("Choose date", date.today())
    effective_date = chosen_date + relativedelta.relativedelta(months=1, day=1)
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

    html_message = ""
    number = 1

    for row in clas.iterrows():
        check = 0

        if str(row[1][6]) == "nan" and str(row[1][10]) == "nan":
            pass
        elif str(row[1][6]) == "nan":
            if row[1][10] <= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1
        elif str(row[1][10]) == "nan":
            if row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1
        else:
            if row[1][10] <= date and row[1][6] >= date and row[1][1] in sectors and keyword_search(row[1][8], keywords):
                number += 1
                check += 1

        if check == 1:
            html_message += get_row_details(row, number)
    if len(html_message) > 0:
        get_html_page(html_message)
    else:
        html_no_result = "<p style=\"size=50px; color: red;\">No results found</p>"
        st.markdown(html_no_result, unsafe_allow_html=True)


def get_row_details(row, number):
    publi_date = get_nice_date(date_format(row[1][4]))
    start_date = get_nice_date(row[1][10])
    end_date = get_nice_date(row[1][6])
    scope = str(row[1][5])[0:50] + '...'
    url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"
    file_link = url + row[0].replace("-", "/", 1)
    # column1 = "width: 260px;"
    # column2 = "width: 160px;"
    # column3 = "width: 245px;"
    # column4 = "width: 110px;"
    # column5 = "width: 222px;"

    html_column = "<tr>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td>{}</td>\
                        <td><a href=\"{}\">Download file</a></td>\
                   </tr>".format(str(row[1][0]), str(row[1][2]), publi_date, scope, str(row[1][1]), start_date, end_date, file_link)
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
    column1 = "width: 100px;text-align: left;"
    column2 = "width: 160px;text-align: left;"
    column3 = "width: 120px;text-align: left;"
    column4 = "width: 160px;text-align: left;"
    column5 = "width: 60px; text-align: right;"
    column6 = "width: 120px;text-align: left;"
    column7 = "width: 120px;text-align: left;"
    column8 = "width: 100px;text-align: left;"

    html_code = "<div>\
                    <div>\
                        <table>\
                            <thead>\
                                <tr style=\"background_color: black; font-family:courier,arial,helvetica; color: #fffdfc\">\
                                    <th style=\"{}\">Deposit Number</th>\
                                    <th style=\"{}\">Title</th>\
                                    <th style=\"{}\">Publication Date</th>\
                                    <th style=\"{}\">Scope</th>\
                                    <th style=\"{}\">JCID</th>\
                                    <th style=\"{}\">Start Date</th>\
                                    <th style=\"{}\">End Date</th>\
                                    <th style=\"{}\">Link to File</th>\
                                </tr>\
                            </thead>\
                            <tbody>\
                                {}\
                            </tbody>\
                        </table>\
                    </div>\
                </div>".format(column1, column2, column3, column4, column5, column6, column7, column8, columns)

    st.write(html_code, unsafe_allow_html=True)


def get_from_html(htmf_file):
    html_code = codecs.open(htmf_file, 'r')
    page = html_code.read()
    stc.html(page, width=700, height=500, scrolling=False)


def get_nice_date(raw_date):
    if str(raw_date) == "nan":
        return "Undefined"
    month_date = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December",
    }

    return str(month_date[raw_date.month]) + " " + str(raw_date.year)


def date_format(date_raw):
    date_parts = date_raw[0:10]
    new_date = datetime.strptime(date_parts, '%Y-%m-%d').date()

    return new_date


if __name__ == "__main__":
    main()
