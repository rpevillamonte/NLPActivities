import nltk
import spacy

# indirect imports
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag, ne_chunk
from nltk.stem import PorterStemmer
from num2words import num2words
from spacy import displacy

# direct imports
import os
import pdfplumber
import numpy as np
import pandas as pd
import json

PDF_PATH = str(os.getcwd()) + '\\PDFs'
JSON_PATH = str(os.getcwd()) + '\\entities.json'

folders = [x[0] for x in os.walk(PDF_PATH)]


class TextProcessor():
    
    def preprocess(self, dirty_text):
        """Process raw text from a file before entity detection"""
        data = self.__convert_lower_case(dirty_text)
        data = self.__remove_punctuation(dirty_text) #remove comma seperately
        data = self.__remove_apostrophe(dirty_text)
        data = self.__remove_stop_words(dirty_text)
        data = self.__convert_numbers(dirty_text)
        #data = stemming(dirty_text)
        data = self.__remove_punctuation(dirty_text)
        data = self.__convert_numbers(dirty_text)
        #data = stemming(dirty_text) #needed again as we need to stem the words
        data = self.__remove_punctuation(dirty_text) #needed again as num2word is giving few hypens and commas fourty-one
        return data
        
    def __remove_punctuation(self, data):
        symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
        for i in range(len(symbols)):
            data = np.char.replace(data, symbols[i], ' ')
            data = np.char.replace(data, "  ", " ")
        data = np.char.replace(data, ',', '')
        return data
    
    def __remove_stop_words(self, data):
        stop_words = stopwords.words('english')
        words = word_tokenize(str(data))
        new_text = ""
        for w in words:
            if w not in stop_words and len(w) > 1:
                new_text = new_text + " " + w
        return new_text
    
    def __convert_lower_case(self, data):
        return np.char.lower(data)
    
    def __remove_apostrophe(self, data):
        return np.char.replace(data, "'", "")
    
    def __stemming(self, data):
        stemmer= PorterStemmer()
        tokens = word_tokenize(str(data))
        new_text = ""
        for w in tokens:
            new_text = new_text + " " + stemmer.stem(w)
        return new_text
    
    def __convert_numbers(self, data):
        tokens = word_tokenize(str(data))
        new_text = ""
        for w in tokens:
            try:
                w = num2words(int(w))
            except:
                a = 0
            new_text = new_text + " " + w
        new_text = np.char.replace(new_text, "-", " ")
        return new_text

class EntityDetector():
    
    def __init__(self) -> None:
        self.nlp = spacy.load('en_core_web_sm')
    
    def __get_entities(self):
        m_entities = []
        master_dict = {}
        file_tags, file_texts = self.__get_text_from_PDFs()
        for key, value in file_texts.items():
            doc = self.nlp(value)
            entity_info = []
            for ent in doc.ents:
                entity = str(ent)
                if ent not in m_entities:
                    new_dict = {}
                    m_entities.append(ent)
                    new_dict['entity'] = entity
                    new_dict['label'] = str(ent.label_)
                    new_dict['exp'] = (spacy.explain(ent.label_))
                    entity_info.append(new_dict)
            master_dict[key] = entity_info
        return master_dict
        
    def process_to_json(self):
        json_data = None
        with open(JSON_PATH) as file:
            json_data = json.load(file)
        
        metadata = self.__get_entities()
        
        json_data.update(metadata)
        with open(JSON_PATH, 'w') as file:
            json.dump(metadata, file)
    
    def __get_text_from_PDFs(self):
        file_tags = []
        file_texts = {}
        for entry in os.listdir(PDF_PATH):
            full_path = os.path.join(PDF_PATH, entry)
            if os.path.isfile(full_path):
                file_tags.append(entry)
                file_texts[entry] = self.__get_contents(full_path)
        return file_tags, file_texts
    
    def __get_contents(self, pdf_path):
        result = ''
        file = pdfplumber.open(pdf_path)
        for page in file.pages:
            result += page.extract_text()
        file.close()
        tp = TextProcessor()
        return str(tp.preprocess(result)).strip()
        
if __name__ == "__main__":
    ed = EntityDetector() 
    
    entities = ed.get_entities()
    
    print(entities)