import re, sys, os, time, json

"""
Highlights a text by changing the color
"""
def highlight_term(term, text, term_type="value"):
    replaced_text = ""
    if term_type == "value":
        replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    elif term_type == "key":
        replaced_text = text.replace(term, "\033[1;35;40m {term} \033[0;0m".format(term=term))
    elif term_type == "title":
        replaced_text = text.replace(term, "\033[1;31;40m {term} \033[0;0m".format(term=term))\

    return "{replaced}".format(replaced=replaced_text)

"""
Returns the content of a file
"""
def get_file_content(path):
    with open(path, "r", encoding='cp1252') as _file:
        return _file.read()

class Appearance:
    """
    Represents the appearance of a term in a given document
    """
    def __init__(self, _id, path, text, frequency):
        self.id = _id
        self.path = path
        self.text = text
        self.frequency = frequency 

class Database:
    """
    In memory database representing the already indexed documents.
    """
    def __init__(self):
        self.db = dict()     

    def get(self, id):
        return self.db.get(id, None) 

    def add(self, document):
        """
        Adds a document to the DB.
        """
        return self.db.update({document['id']: document})

    def remove(self, document):
        """
        Removes document from DB.
        """
        return self.db.pop(document['id'], None)

class InvertedIndex:
    """
    Inverted Index class.
    """
    def __init__(self, db):
        self.indexed = dict()
        self.db = db       

    """
    Process a given document, save it to the DB and update the index.
    """
    def index_document(self, document):
        # remove special characters (replace with space) then
        # .replace('\n', ' ')
        clean_text = re.sub('[^A-Za-z0-9]+', ' ', document['text'])
        terms =  clean_text.split(' ')

        appearances_dict = dict()        # Dictionary with each term and the frequency it appears in the text.
       
        for term in terms:
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], document['path'], document['text'], term_frequency + 1)
            
        update_dict = {}
        for (key, appearance) in appearances_dict.items():
            if key not in self.indexed:
                update_dict[key] = [appearance]
            else:
                update_dict[key] = self.indexed[key] + [appearance]

        self.indexed.update(update_dict)        
        # Add the document into the database
        self.db.add(document)
        return document

    def get_indexes(self):
        return self.indexed

class Retriever:
    def __init__(self, indexer):
        self.indexer = indexer

    def retrieve_results(self, query):
        """
        Returns the dictionary of terms with their correspondent Appearances. 
        """
        results = {}
        for term in query.split(' '): 
            if term in self.indexer.indexed:
                results[term] = self.indexer.indexed[term]

        return results

def start_indexing(indexer, data_dir, search_term):
    count = 0  # a counter for total files, as id
    # start indexing files
    for _dir in os.listdir(data_dir):              
        _child_dir = os.path.join(data_dir, _dir)       # combine the parent dir and the child dir
        for _file in os.listdir(_child_dir):            # navigate between the folders
            _path = os.path.join(_child_dir, _file)     # get the files in the folder
            if os.path.isfile(_path):                   # check if file
                print("Indexing " + _path)
                document = {                            #  create a dictionary containing the document information
                    'id': str(count),
                    'path': _path,
                    'text': get_file_content(_path)
                }   

                indexer.index_document(document)        # start indexing the file
                count += 1

def show_results(db, retriever, out="pretty"):
    # clear terminal logs
    os.system("clear")
    print("Done Indexing files....")
    time.sleep(2)
    os.system("clear")
    time.sleep(1)

    # get results from the retriever
    result = retriever.retrieve_results(search_term)

    # displaying the results by line
    for term in result:
        if out == "pretty":
            print("---------------------- " + highlight_term(term, term, "title") + " ----------------------")
        for appearance in result[term]:
            document = db.get(appearance.id)
            if out == "pretty":
                print("\n**\033[1;31;40m {} \033[0;0m".format("Appears " + str(appearance.frequency) + " times in " + document["path"]))

                # we want to display the occurrence in a list
                text_lines = document["text"].split('\n')
                for text_line in text_lines:
                    if len(text_line) < 1 or term not in text_line:
                        """
                        Here we neglect if the term is not in a text line
                        """
                        continue

                    print("{}:{}".format(highlight_term(document["path"], document["path"], "key"), 
                                            highlight_term(term, text_line)) )
            else:
                print({
                        "term": term,
                        "path":document["path"],
                        "frequency": appearance.frequency
                    })

# check if input is valid
if len(sys.argv) != 4:
    print("USAGE: python InvertedIndex.py [data_folder] [string] [out_type]")
    exit()

if __name__ == "__main__":
    # format: python InvertedIndex.py [data_folder] [string]
    data_dir = sys.argv[1]          # the directory the document files
    search_term = sys.argv[2]       # our query string
    out_type = sys.argv[3]          # output type 'raw' or 'pretty'

    if out_type != "raw" and out_type != "pretty":
        raise ValueError("out_type should be either raw or pretty")

    db = Database()                 # our indexed string storage
    indexer = InvertedIndex(db)     # indexer
    retriever = Retriever(indexer)  # the retriever

    start_indexing(indexer, data_dir, search_term) # start idnexing files
   
    show_results(db, retriever, out_type)           # show results
