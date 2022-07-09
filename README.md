# Document Conflation
We quantitatively compared four near-duplicate detection methods using the ground truth created from S2ORC and CiteSeerX.
* ## S2ORC   
S2ORC is one of the largest open-access scholarly big datasets with 136M+ paper nodes with 12.7M+ full-text papers connected by 467M+ citation edges by unifying data from different sources. If the paper is found in another database, the two documents are linked by adding the external database ID as a metadata field of the S2ORC paper. In S2ORC, each paper has a unique ID. If the paper is found in another database, the two documents are linked by adding the external database ID as a metadata field of the S2ORC paper.  
* ## CiteSeerX
CiteSeerX has 10 million full-text papers with 77 million citation records and it has been proven as a powerful resource in many data mining, machine learning and information retrieval applications that use rich metadata. 
The performance for each method is evaluated using precision, recall and F1-score.
A true positive (TP) is a near-duplicate paper predicted by a method and in a cluster of the ground truth. 

## Fuzzy Matching
* Fuzzy matching was performed by calculating the Jaccard index between unigrams extracted from titles (or abstracts) to find near-duplicates.  
* To find the best performance, we set four different thresholds at 80%, 85%, 90%, and 95%.  

## Key-Mapping
* Key-mapping is a conflation method used by CiteSeerX.
* In this method, several keys are generated for each paper by concatenating a portion of title and author information.  

## Locality Sensitive Hashing (LSH)
* LSH is an algorithm that breaks an input string into pieces (shingles) and hashes similar strings into the same “buckets’ with high probability.
* It has been used as an efficient method to resolve near-duplicate news articles.  

## Strict Title
* In this method, we use the full title of a paper and compare it against the titles of all other papers.  
* If two titles were identical it was determined as near-duplicate.  
