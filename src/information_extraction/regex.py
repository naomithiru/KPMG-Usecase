"""This script extracts information from the document bodies to new DataFrame columns"""

import pandas as pd
import re

def add_scope(df):

	def split_func(text):
		texts_lst = []
		sents = text.split("\n\n")
		for sent in sents:
			texts_lst.append(sent)
		return texts_lst

	def extract_scope(lst):
		scope_lst = []
		for item in lst:
			#pattern1 = r".*\b(convention collective de travail s'applique | Champ d'application)\b.*"
			#pattern2 = r".*\b(La présente convention collective de travail\s*\S* [a-z]'appli\w*)\b.*"
			#pattern3 = r".*\b(convention collective de travail|CCT)\s*\S*[a-z]('appli\w*)\b.*"
			#pattern4 = r".*\b(convention collective de travail|CCT)\s*\S*.*('?appli\w*)\b.*"
			pattern = r".*\b(convention collective de.*travail|CCT).*('*appli\w*)\b.*"
        	if re.search(pattern, item, flags=re.IGNORECASE):
            	scope_lst.append(item)
        	else:
            	pass

         # DataFrame convention is to have scope as a string
         return '\n'.join(scope_lst)

    df['texts_lst'] = df['docBodyFr'].apply(split_func)

    df['scopeFr'] = df['texts_lst'].apply(extract_scope)
    df.drop(columns=['texts_lst'], inplace = True)

    return df

def add_from(df):
	

