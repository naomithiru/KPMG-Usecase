import pandas as pd
from pathlib import Path
from pickle import dump, load
# import requests
# import time
# import random
# import requests
# import json
from datetime import date, datetime
import time

from scraping.scrape import scrape_new
import text_extraction.ocr
import information_extraction.regex

current_clas_location = Path('pipeline/model')

# get meta-DataFrame of new documents
new = scrape_new(current_clas_location)
check_time = datetime.fromtimestamp(time.time())

# for debugging
with open(Path('src/scraping/newitems.pkl'), 'wb') as f:
        dump(new, f)

# ocr new pdfs, if there are new ones
if type(new) != type(None):
    new = text_extraction.ocr.extract(new)


    with open(current_clas_location / 'clas.pkl', 'rb') as f:
        current = load(f)

    # add the new texts to the current DataFrame and start
    # information extraction
    # sometimes the same filename will have it's recordDate updated, causing it to reappear in our scraping
    # in those cases we drop the previous record
    current = current[~current.index.isin(new.index.tolist())]
    # we do an outer join of columns, making NaN values for the not-yet-extracted new information
    current = pd.concat([current, new], join = "outer", verify_integrity = True)
    # sort all so that latest publications are on top
    current.sort_values(by = 'depositNumber', inplace = True, ascending = False)

    # information extraction is actually done on the whole dataframe (redone for old clas)
    current = information_extraction.regex.extract(current)

    # overwrite pkl file with the new version and
    # save update information for display
    with open(current_clas_location / 'clas.pkl', 'wb') as f:
        dump(current, f)
    with open(current_clas_location / 'update.txt', 'w') as f:
        f.write(f"Last check: {check_time.strftime('%a %b %d - %H:%M')}\n")

        last_publication = current[['depositNumber', 'publicationDate']].iloc[0,1][:10]
        last_publication = date.fromisoformat(last_publication)
        f.write(f"Latest pub: {last_publication.strftime('%a %b %d')}\n")





        