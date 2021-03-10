from datetime import date, timedelta
import json
from pathlib import Path
from pickle import load
import requests
import time

import pandas as pd

def scrape_new(current_clas_location):
    '''
    This function gets the json formatted post request result form the web API
    for the missing documents and returns their metadata in a dataframe
    '''

    with open(current_clas_location / 'clas.pkl', 'rb') as f:
        old = load(f)

    start = old.sort_values(by = "publicationDate").iloc[-1]["publicationDate"].split("+")[0]+"Z"
    # start = str(date.today() - timedelta(days=1))+'T00:00:00.000Z'
    end = str(date.today())+'T00:00:00.000Z'

    #API details
    url = "https://public-search.emploi.belgique.be/website-service/joint-work-convention/search"
    body = json.dumps(\
        {"lang":"fr",
        "title":"",
        "superTheme":"",
        "theme":"",
        "textSearchTerms":"",
        "signatureDate":{"start":None,"end":None},
        "depositNumber":{"start":49933,"end":None},
        "noticeDepositMBDate":{"start":None,"end":None},
        "enforced":"",
        "royalDecreeDate":{"start":None,"end":None},
        "publicationRoyalDecreeDate":{"start":None,"end":None},
        "recordDate":{"start":start,"end":end},
        "correctedDate":{"start":None,"end":None},
        "depositDate":{"start":None,"end":None},
        "advancedSearch":True})
            # {"lang":"fr",
            # #"jc":"1200000",
            # "title":"",
            # "superTheme":"",
            # "theme":"",
            # "textSearchTerms":"",
            # "signatureDate":{"start":null,"end":null},
            # "depositNumber":{"start":49933,"end":null},
            # "noticeDepositMBDate":{"start":null,"end":null},
            # "enforced":"",
            # "royalDecreeDate":{"start":null,"end":null},
            # "publicationRoyalDecreeDate":{"start":null,"end":null},
            # "recordDate":{"start":null,"end":null},
            # "correctedDate":{"start":null,"end":null},
            # "depositDate":{"start":start,"end":end},
            # "advancedSearch":true})
    headers = {'Content-Type': 'application/json'}

    #Making http post request
    response = requests.post(url, headers=headers, data=body, verify=False)

    json_file = json.dumps(response.json())
    new = pd.read_json(json_file)

    # If the result is not empty
    # return a dataframe with only the info we use from the scraped json
    # & reformat to our DataFrame convention
    try:
        new['documentLink'] = new.documentLink.apply(lambda x: x.replace('/', '-'))
        new.set_index('documentLink', inplace = True)


        def display_jcid(jcid):
            """return a format of 118 or 140.01"""
            if str(jcid)[3:5] == '00':
                return str(jcid)[:3]
            else:
                return str(jcid)[:3]+'.'+str(jcid)[3:5]

        new['displayJcId'] = new.jcId.apply(lambda x: display_jcid(x))

        # only keep the ones from the committees we are interested in
        new = new.loc[new.displayJcId.astype("string").str[:3].isin(['124', '200', '111', '209', '311', '207', '116', '140', '310', '118', '220', '121']),:]

        new.rename(columns={"recordDate": "publicationDate",
                            "validityDate": "endDate"}, inplace = True)

        # set empty docBodyFr
        new['docBodyFr'] = ''
        new['docBodyFr'] = new['docBodyFr'].astype("string")

        # make a depositNumberLink column with html
        def depositNumberLink(depositNumberSeries):
            base_url = "https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/"
            appendix = depositNumberSeries.index.str.replace("-", "/", 1).tolist()
            url = [base_url + file for file in appendix]
            html = [f'<a href="{url}">{depositNumber}</a>' for url, depositNumber in zip(url, depositNumberSeries)]

            return html

        new['depositNumberLink'] = new[['depositNumber']].apply(depositNumberLink)

        # select our columns
        new = new[['depositNumber',
                    'depositNumberLink',
                    'displayJcId',
                    'titleFr',
                    'themesFr',
                    'publicationDate',
                    'scopeFr',
                    'endDate',
                    'enforced',
                    'docBodyFr']]

        return new

    except:
        return None
