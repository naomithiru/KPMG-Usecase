"""This script regex-extracts information from the document bodies to new DataFrame columns"""

import datetime
from pickle import load
import re

import numpy as np
import pandas as pd

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


def add_effective_date(df):
    """A function that searches the document bodies for fromDate and endDates
    and extracts datetime objects into new columns"""
    
    def get_dates(df_row):
        
        def get_month_digit(month):
            dictionary = {
                'janvier': 1,
                'février': 2,
                'mars': 3,
                'avril': 4,
                'mai': 5,
                'juin': 6,
                'juillet': 7,
                'août': 8,
                'septembre': 9,
                'octobre': 10,
                'novembre': 11,
                'décembre': 12
            }
            
            return dictionary[month]
        
        #start date matches ~46 out of 48 test cases
        #group 6 = month
        #group 7 = year
        pattern = r"((cette|la présente) (convention collective de travail|CCT)|elle).+(entre en vigueur|à partir|produit ses effets|s'étend|sort ses effets|prend cours|\bdéterminée|allant).{1,19}(le\b|du\b|de\b|au\b).{1,5}(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) ([0-9]{4})"
        # finds the first instance of the regex in the body
        match = re.search(pattern, df_row['docBodyFr'], flags=re.IGNORECASE)
        if match:
            try:
                df_row['fromDate'] = datetime.date(int(match[7]), get_month_digit(match[6]), 1)
            except:
            	df_row['fromDate'] = np.nan
        else:
            df_row['fromDate'] = np.nan
        
        #end date matches 47 of 48
        #group 6 = month
        #group 7 = year
        pattern = r"((cette|la présente) (convention collective de travail|CCT)|elle).+([0-9]{4}|cesse de produire ses effets|cesse d'être en vigueur|cesse ses effets|prend fin|expire|conclue jusq|prend.{1,25}fin).+(le\b|au\b).{1,5}(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) ([0-9]{4})"
        match = re.search(pattern, df_row['docBodyFr'], flags=re.IGNORECASE)
        if match:
            try:
                df_row['endDate'] = datetime.date(int(match[7]), get_month_digit(match[6]), 28)
            except:
            	df_row['endDate'] = np.nan
        else:
            df_row['endDate'] = np.nan
        
        #there might have been an erroneous match of endDate
        #which should be overwritten by None when durée idéterminée is detected
        pattern = r"((cette|la présente) (convention collective de travail|CCT)|elle).+(durée indéterminée|([0-9]{4}.+à l'exception))"
        match = re.search(pattern, df_row['docBodyFr'], flags=re.IGNORECASE)
        if match:
            df_row['endDate'] = np.nan
        
        return df_row
    
    df = df.apply(get_dates, axis=1)

    return df

def extract(df):
	'''overall regex extraction functioin'''

	df = add_scope(df)

	df = add_effective_date(df)

	return df

