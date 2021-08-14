# InvertedIndex
An inverted index is an index data structure storing a mapping from content, such as words or numbers, to its locations in a document or a set of documents. In simple words, it is a hashmap like data structure that directs you from a word to a document or a web page. 


## How the program works:
- it will ask for the email directory and the query string
- performs indexing
- search for the keywords in the indexed data
- returns the indexed_data that matched to the keyword


This progam is intended for showing the indexer and retriever functionalities only. This does not include parallelism.


## Running:
python InvertedIndex.py [data_dir] [string] [out_type]

where:
- data_dir is the folder containing the emails or the files/texts files
- string is the keyword/keywords to be searched
- out_type raw for json or pretty

## Examples:
```
- finding "JSKILLIN" in the emails directory
 python InvertedIndex.py "skilling-j" "JSKILLIN" "pretty"
 python InvertedIndex.py "skilling-j" "JSKILLIN" "raw"
 
- other examples:
finding the term "God: in the "bible" directory
python InvertedIndex.py bible "God" "pretty"
python InvertedIndex.py bible "God" "raw"

finding the term "document: in the "simple_data" directory
python InvertedIndex.py simple_data "document" "pretty"
python InvertedIndex.py simple_data "document" "raw"
```
