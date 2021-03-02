'''pdf distinction:
we have to distinguish the format of the pdf and then we need to choose the French one
there are three different formats already detected
1) two coulumn documents (one column for French one column for Dutch)  
1.a) there is a line between them  
1.b) there is no line between them  
2) one language after the other format  
3) These texts start as two column for very first pages then continued like the other'''


from pathlib import Path
import re

import fasttext
import numpy as np
import pandas as pd
from pdf2image import convert_from_path 
import pytesseract
from multiprocessing import Process


# set folder to pdf files:
scraping_folder = Path('src/scraping/output')

# set output txt folder:
output_folder = Path('src/text_extraction/output')

# sort scrape by commission popularity and put filename in index
scrape = pd.read_json(scraping_folder / 'responses_2018_now.json')
scrape['documentLink'] = scrape.documentLink.apply(lambda x: x.replace('/', '-'))
scrape.set_index('documentLink', inplace = True)
popularity_sort = scrape[['jcId']].groupby('jcId')['jcId'].transform('count').sort_values(ascending = False).index
scrape = scrape.loc[popularity_sort,:]


'''This block holds the text extraction by language code'''

class LanguageIdentification:

    def __init__(self):
        pretrained_lang_model = "src/text_extraction/lid.176.bin" #large more accurate model
        self.model = fasttext.load_model(pretrained_lang_model)

    def predict_lang(self, text):
        predictions = self.model.predict(text, k=10) #returns top 10 matching languages
        return predictions        


def clean_language(detector, textpart, dominance = 5, threshold = 0.4):
    '''This function takes a string and detects nl/fr/inconclusive with fasttext and returns a cleaned string.
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
    
    # Continue the same or next sentence on the same line (delete line breaks inside alinea)
    text = re.sub(r'([^\n])\n([^\n])', r'\1 \2', text)
    
    # Delete the separation between Art* and the following line.
    text = re.sub(r'(A(r|ï)t[^ ]* +[^ \n]+) *\n( |\n)*', r'\1 ', text)
        
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
        # convert the page to np array to see as image
        img = np.array(img[0])
        # splitting the array into two equal pieces vertically
        half_img_lst = np.array_split(img, 2,axis=1)
        # read the text for each half with pytessaract
        text_1 = str(((pytesseract.image_to_string(half_img_lst[0], lang="fra+nld"))))
        text_2 = str(((pytesseract.image_to_string(half_img_lst[1], lang="fra+nld"))))
        del half_img_lst
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

    f = open(output_folder / f'{str(pdf_path).split("/")[-1][:-4]}_NL.txt', "w")
    f.write('\n'.join(whole_text_nl.splitlines(True)))
    f.close()
    f = open(output_folder / f'{str(pdf_path).split("/")[-1][:-4]}_FR.txt', "w")
    f.write('\n'.join(whole_text_fr.splitlines(True)))
    f.close()

    return


# Start text extraction
job_total = len(scrape)
i = 1640
detector = LanguageIdentification()
for filename in scrape.index[1640:1800]:
    print(f'starting {i}/{job_total}', filename)
    Welcome(detector, scraping_folder / filename)
    i += 1
