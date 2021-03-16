# A monitor of Collective Labour Agreements

As a team of 5 we rose to the challenge from KPMG to extract knowledge from publicly published collective labour agreements. We learned about the client's process of manually watching for new publications and the subsequent tracking of key changes in sector labour rules.  
We found 2 key search functions were not available on the government website; the ability to filter more than 1 sector, and the ability to see just the agreements currently in effect, regardless of their publication date. As a consequence, we crystallized our objective into building a webapp for the discovery and first interpretation of new agreements. 


    1) Checking documents for topic hierarchy (chapters, sections, articles, paragraphs)
		    Chapters sometimes hold different topics. Article level detection seems best.

    2) Extracting unstructured French text (no hierarchy or page location metadata)
       
    3) Investigation on how to structure the text into Articles (split words, bounding box, others?)  
		    Didn't do
       
    4) Kind of succeed in detecting the lowest Paragraph hierarchy  
		    targeted removal of newline characters inside paragraphs with regex
       
    5) This was enough to extract applicable to and CLA durations reliably
       
    6) Enough to extract related CLA info or specific topic key figures?
		    Under study

    7) Choose additional unemployment payments due to corona as key figure for extraction  
		    automatic labeling found 24 documents across committees
       
    8) Set up text span annotation tool for this topic (future training of NER and sequence classifier)
		    * start/end dates/daily amounts/max yearly amount labels ==> for key figure extraction
		    * whole paragraphs ==> to detect switch of topic in documents

    9) Themes tagging. Agreed to not assign enough time and resources to tackle all the following challenges:
       a) Some theme only present with other themes. Filtering by presence of a theme among the document themes.
       b) Some documents missing tags. Using only documents having at least one tag.
       c) Lack of enough samples for some themes. Acceptance of different accuracy per theme.
       d) Lack of reliable true negatives (e.g. chomage temporaire). Use of multilabel classification checking similarities with corpus of theme docs.
       e) Selection of keywords per theme to be used avoding too many unecessary overlaps. Not enoug time for it.
