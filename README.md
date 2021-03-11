# KPMG-Usecase

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
