'''pdf distinction:
we have to distinguish the format of the pdf and then we need to choose the French one
there are three different formats already detected
1) two coulumn documents (one column for French one column for Dutch)  
1.a) there is a line between them  
1.b) there is no line between them  
2) one language after the other format  
3) These texts start as two column for very first pages then continued like the other'''


from pathlib import Path
from PIL import Image
import os
import random
import re
import requests
import shutil
import sys
import time
import threading
from typing import List

import fasttext
import numpy as np
import pandas as pd
from pdf2image import convert_from_path
import pytesseract



# set folder for pdf file downloads:
scraping_folder = Path('src/scraping/outputnew')
if not scraping_folder.exists():
    os.makedirs(scraping_folder)

# set folder to fasttext model
fasttext_model = Path('src/text_extraction/lid.176.bin')

class LanguageIdentification:

    def __init__(self):
        pretrained_lang_model =  str(fasttext_model) #large more accurate model
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=10) #returns top 10 matching languages
        return predictions        


def clean_language(detector, textpart, dominance = 4, threshold = 0.55):
    '''This function takes tesseract output and returns a cleaned string and nl/fr/inconclusive language info.
    Cleaning merges alineas on 1 line and removes empty lines, it is good for language detection and for later classification.
    ::detector:: an instance of the fasttext language detector
    ::textpart:: the whole or part of a page
    ::dominance:: how much more a language needs to be present over the other before awarding it
    ::threshold:: language score required before detecting presence'''
    
    # first clean the text
    # Delete word-break-ups at the end of a line
    text = textpart.replace('-\n', '')
    
    # Replace form feed (new page) character with normal new line
    text = re.sub(r'\f', r'\n', text)
    
    # Delete line breaks that don't look like section breaks
    text = re.sub(r'([^;.:])\n+([a-z0-9éèô(\s])', r'\1 \2', text)
    
    # # Delete the separation between Art* and the following line.
    # text = re.sub(r'(A(r|ï)t[^ ]* +[^ \n]+) *\n( |\n)*', r'\1 ', text)
        
    # Delete empty lines
    cleantext = ""
    for line in iter(text.splitlines(True)):
        if re.match(r' *\n$', line) is None:
            cleantext += line
    
    # initiate counters to detect the dominant language
    fr_count = 0
    nl_count = 0
    
    for alinea in iter(cleantext.splitlines(False)):
        prediction = detector.predict_lang(alinea.lower())
        
        try:
            fr_index = prediction[0].index('__label__fr')
            fr_score = prediction[1][fr_index]
        except:
            fr_score = 0
        try:
            nl_index = prediction[0].index('__label__nl')
            nl_score = prediction[1][nl_index]
        except:
            nl_score = 0
        
        # We give the alinea to the language with the highest score if it is higher than threshold
        if fr_score > threshold and fr_score > nl_score:
            fr_count += 1
        elif nl_score > threshold and nl_score > fr_score:
            nl_count += 1
    
    # compare the counts on the whole textpart
    if fr_count == 0 and nl_count == 0:
        language = 'inconclusive'
    else:
        try:
            french_dominance = fr_count/nl_count > dominance
        except:
            french_dominance = True
        finally:
            if french_dominance:
                language = 'fr'
        try:
            dutch_dominance = nl_count/fr_count > dominance
        except:
            dutch_dominance = True
        finally:
            if dutch_dominance:
                language = 'nl'
        
        if not french_dominance and not dutch_dominance:
            language = 'inconclusive' 
    
    return (language, cleantext)


def Welcome(detector, pdf_path):

    whole_text_fr = ""
    whole_text_nl = ""

    for page in range(1, 9999):
        # read pages one by one to save memory
        img = convert_from_path(pdf_path, first_page = page, last_page = page, dpi = 425)
        if len(img) == 0:
            break

        # google colab gave pytesseract image_to_osd error on some pdf files
        try:
            report = pytesseract.image_to_osd(img[0])
            
            if report.split("\n")[1].split(":")[1].replace(" ", "") == "270":
                img = np.array(img[0]) # convert PIL.PpmImagePlugin.PpmImageFile to np.array
                img_pil = Image.fromarray(np.uint8(img)).convert('RGB') # np.array to PIL image
                rotated  = img_pil.transpose(Image.ROTATE_270) #rotate the image 
                img = np.array(rotated)# convert the page to np array to see as image
            
            elif report.split("\n")[1].split(":")[1].replace(" ", "") == "90":
                img = np.array(img[0]) # convert PIL.PpmImagePlugin.PpmImageFile to np.array
                img_pil = Image.fromarray(np.uint8(img)).convert('RGB') # np.array to PIL image
                rotated  = img_pil.transpose(Image.ROTATE_90) #rotate the image 
                img = np.array(rotated)# convert the page to np array to see as image

            # convert the page to np array to see as image
            else:
                img = np.array(img[0])

            # splitting the array into 51% sliced pieces vertically
            left_side = img[:,:-(round(img.shape[1]*0.49))]
            right_side = img[:,(round(img.shape[1]*0.49)):]
            # read the text for each half with pytessaract
            text_1 = str(((pytesseract.image_to_string(left_side, lang="fra+nld"))))
            text_2 = str(((pytesseract.image_to_string(right_side, lang="fra+nld"))))
            del left_side, right_side
            # if language detection of each half is equal, or if fr/nl is not dominant
            # on either side, the page is not in two column format
            # that means we have one language follow the other or all in french text
            left_lang, left_text = clean_language(detector, text_1)
            right_lang, right_text = clean_language(detector, text_2)
            if left_lang == right_lang or right_lang == 'inconclusive' or left_lang == 'inconclusive':
                # assign the detected text from whole page as a text
                text = str(((pytesseract.image_to_string(img, lang="fra+nld"))))
                lang, text = clean_language(detector, text)
                # add the cleaned text to the correct language
                if lang == "fr":
                    whole_text_fr += text
                elif lang == "nl":
                    whole_text_nl += text
                # if no domininant language, keep the whole text for both languages
                elif lang == "inconclusive":
                    whole_text_nl += text
                    whole_text_fr += text
            # otherwise the page is two column page. We need to assign it to the correct language    
            elif left_lang == 'fr':
                whole_text_fr += left_text
                whole_text_nl += right_text
            elif left_lang == 'nl':
                whole_text_fr += right_text
                whole_text_nl += left_text

            del img

        except:
            continue



    # create strings with whitespace between alineas (easier on the eyes)
    whole_text_nl = '\n'.join(whole_text_nl.splitlines(True))
    whole_text_fr = '\n'.join(whole_text_fr.splitlines(True))

    return whole_text_nl, whole_text_fr


def download_pdf(documentLinks: List[str]):
    base_url = r'https://public-search.emploi.belgique.be/website-download-service/joint-work-convention/'
    # fetches the pdf file
    for url in documentLinks:
        r = requests.get(base_url + url.replace("-", "/", 1), allow_redirects=True)
        # replacing / with - in the filename of the pdf
        file = open(scraping_folder / url, 'wb')
        file.write(r.content)
        # puts the thread randomly to sleep from 0.1 to 1.9 seconds
        random_number = random.randint(0,10) /10 + random.randint(0,1)
        time.sleep(random_number)
        file.close()

    return


def extract(df):
    """Main text extraction function. Receiving a DataFrame
    with new agreements to extract text from.
    Output is the same dataframe with newly inserted doc bodies"""

    to_download = df.index.tolist()
    # download the first pdf file to start OCR
    download_pdf([to_download[0]])
    # download the rest of the pdf files on a thread
    if len(to_download) > 1:
        threading.Thread(target = download_pdf, args = (to_download[1:],)).start()

    job_total = len(to_download)
    i = 1
    # initiate fasttext
    detector = LanguageIdentification()

    for filename in to_download:
        print(f'starting {i}/{job_total}', filename)
        sys.stdout.flush()
        _, whole_text_fr = Welcome(detector, scraping_folder / filename)
        df.loc[filename, "docBodyFr"] = whole_text_fr
        i += 1

    del detector

    # pdf files no longer needed
    shutil.rmtree(scraping_folder)

    return df
