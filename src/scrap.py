check
#https://www.datacamp.com/community/tutorials/json-data-python
# https://campus.datacamp.com/courses/intermediate-importing-data-in-python/interacting-with-apis-to-import-data-from-the-web-2?ex=8
#https://campus.datacamp.com/courses/intermediate-importing-data-in-python/interacting-with-apis-to-import-data-from-the-web-2?ex=8

import requests
from flask import jsonify, Flask

app = Flask(__name__)


GET_LINK = 'https://public-search.emploi.belgique.be/website-service/joint-work-convention/search'

PLOADS = {"lang": "fr", "title": "", "superTheme": "C", "theme": 115, "textSearchTerms": "",
             "signatureDate": {"start": None, "end": None}, "depositNumber": {"start": 49933, "end": None},
             "noticeDepositMBDate": {"start": None, "end": None}, "enforced": "",
             "royalDecreeDate": {"start": None, "end": None},
             "publicationRoyalDecreeDate": {"start": None, "end": None}, "recordDate": {"start": None, "end": None},
             "correctedDate": {"start": None, "end": None}, "depositDate": {"start": None, "end": None},
             "advancedSearch": False}

#r = requests.post(LINK_HTTPS, data=PLOADS)
#print(r.text)

from flask import jsonify

@app.route(GET_LINK)
def get_current_user():
    return jsonify(username=g.user.username,
                   email=g.user.email,
                   id=g.user.id)