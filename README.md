# A monitor of Collective Labour Agreements

As a team of 5 we rose to the challenge from KPMG to extract knowledge from publicly published collective labour agreements. We learned about the client's process of manually watching for new publications and the subsequent tracking of key changes in sector labour rules.  
We found 2 key search functions were not available on the government website; the ability to filter more than 1 sector, and the ability to see just the agreements currently in effect, regardless of their publication date. By consequence, we crystallized our objective around making the searching and browsing of agreements more efficient, so that legal subject matter experts could spend more time reading what matters.
The extra task of extracting and reporting key figure changes was daunting, and we chose to select a specific subtopic that was a significant source or recent change; extra compensations alotted for temporary unemployment due to the corona epidemic.

Our journey is documented below:

1) We saw there were different topic categorisations possible.  
		a) A list of ~10 main categories like remuneration or training
		b) A list of 57 specific themes
		c) A list of 35 topics + a 'rest' category as used by the client, which seemed to be mappable to the themes in b)  
		A key observation was that theme attributes in b) were not available for brand new publications, so the value in making a classifier that attributes them automatically was clear. Also, the government website did not allow the collection of main category (a) labels, so we focused on modeling the themes in b). 

2) Themes tagging. We couldn't find the right approach in time. More detail below:  
	a) We studied on which level in a document's hierarchy we needed to predict topics.  
		capters/sections -> articles -> paragraphs
		Chapters sometimes hold different topics, so topic labels should apply on the Article level, with a list of belonging paragraphs.
		We thought it best to detect Article boundaries using regex, but didn't complete that.
	b) Some themes only present with other themes. Filtering by presence of a theme among the document themes.  
	c) We could limit ourselves to modeling just the themes for which there were documents where the theme applied exclusively. 
	d) Lack of enough samples for some themes. Acceptance of different accuracy per theme.  
	e) Lack of reliable true negatives (e.g. chomage temporaire). Use of multilabel classification checking similarities with corpus of theme docs.  
	f) Ultimately we concluded that we needed to curate our own list of keywords per theme, perhaps after a TF-IDF run on the documents in c).  

3) Extracting unstructured French text (without hierarchy or page location metadata)  
		We customised our own dynamic layout detection algorithm that coped with changes in orientation and column layouts inside documents. We used fasttext language detection to find the segments of the page with Dutch language and avoided extracting those parts.

4) We kind of succeeded in stitching lines together that belonged to the same Paragraph (lowest step in the document hierarchy)  
		- We did targeted removal of newline characters for this with regex  
		- We found a method later on that would allow us to execute OCR paragraph by paragraph, using tunable OpenCV image contouring  
		- We learned from other teams that the dictionary output of tesseract could also provide help here

5) The paragraph sequences created this way allowed us to more reliably extract the from and to dates that stipulate a CLA's duration. And we also used it to extract the key information describing the field of application of the agreement. 
		We used regexex that operated line by line, to avoid inaccurate matches across lines.
		We capture most of the specific language variations preluding from- or to- dates.  
		We achieved 75% accuracy, and avoided extracting wrong dates in 20% of cases, leaving only 5% to be wrong.

6) Automatic labeling through regex of corona compensation texts found 24 documents across committees. We set up a text span annotation tool for manually weeding out this topic and accompanying key figures with specific labels (for future training of NER and a sequence classifier)  
		* start/end dates/daily amounts/max yearly amount labels ==> for key figure extraction  
		* whole Article/sequence labeling ==> to use as a condition for extracting only the key firgures mentioned in the right context  
		* We think that we may have been able to complete this task in time had we focused on regex extraction instead  

In the end we presented our webApp to the client. It is afvailale at:  
[cla-monitor.herokuapp.com](https://cla-monitor.herokuapp.com/)
