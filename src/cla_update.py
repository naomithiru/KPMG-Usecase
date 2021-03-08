import pandas as pd
from pathlib import Path
# from Pickle import load
from pickle import dump
# import requests
# import time
# import random
# import requests
# import json
# from datetime import date

from scraping.scrape import scrape_new
import text_extraction.ocr
import information_extraction.regex

clas_location = Path('pipeline/model/clas_new.pkl')

# get meta-DataFrame of new documents
new = scrape_new()

# for debugging
with open(Path('src/scraping/newitems.pkl'), 'wb') as f:
        dump(new, f)

# download and ocr new pdfs
if type(new) != type(None):
    new = text_extraction.ocr.extract(new)

    # merge the new text extractions into the current DataFrame and start
    # information extraction
    # overwrite old extractions if needed
    with open(clas_location, 'rb') as f:
        current = load(f)
    current = current[~current.index.isin(new.index.tolist())]
    current = pd.concat([current, new], join = "outer", verify_integrity = True)

    # for debugging 
    with open(Path('pipeline/model/clas_intermediate.pkl'), 'wb') as f:
        dump(current, f)

    # add information


    # write new pkl file


        