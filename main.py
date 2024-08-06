from scrappers.wikitionary import *
from flashcardCreator import *
from chatGPTapi import *
import random
import json
import os
import re


class Word:
    def __init__(self, top, filename='data/cards.json'):

        self._top = str(top)
        self.filename = filename

        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as file:
                json.dump({}, file)

        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(self._top, str) and self._top in data:
                    self._tlang = data[self._top].get("tlang", "")
                    self.langa = data[self._top].get("langa", "")
                    self.langb = data[self._top].get("langb", "")
                    self.xtlang1 = data[self._top].get("xtlang1", "")
                    self.xtlang2 = data[self._top].get("xtlang2", "")
                    self.xtlang3 = data[self._top].get("xtlang3", "")
                    self.xlanga1 = data[self._top].get("xlanga1", "")
                    self.xlanga2 = data[self._top].get("xlanga2", "")
                    self.xlanga3 = data[self._top].get("xlanga3", "")
                    self.xlangb1 = data[self._top].get("xlangb1", "")
                    self.xlangb2 = data[self._top].get("xlangb2", "")
                    self.xlangb3 = data[self._top].get("xlangb3", "")
                    self._tag = data[self._top].get("tag", "")
                else:
                    self.clear()
        except FileNotFoundError:
            self.clear()
        except json.JSONDecodeError:
            self.clear()

    def initialize(self, metadata):
        self._tlang = metadata["words"][int(self._top)-1]
        category = categorize(self._tlang, metadata["tlang"])
        self._tag = category
    
    def clear(self):
        self._tlang = ""
        self.langa = ""
        self.langb = ""
        self.xtlang1 = ""
        self.xtlang2 = ""
        self.xtlang3 = ""
        self.xlanga1 = ""
        self.xlanga2 = ""
        self.xlanga3 = ""
        self.xlangb1 = ""
        self.xlangb2 = ""
        self.xlangb3 = ""
        self._tag = ""
    
    @property
    def top(self):
        return self._top
    
    @property
    def tlang(self):
        return self._tlang
    
    @property
    def tag(self):
        return self._tag

    def update(self):
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[self._top] = {
            "tlang": self.tlang,
            "langa": self.langa,
            "langb": self.langb,
            "xtlang1": self.xtlang1,
            "xtlang2": self.xtlang2,
            "xtlang3": self.xtlang3,
            "xlanga1": self.xlanga1,
            "xlanga2": self.xlanga2,
            "xlanga3": self.xlanga3,
            "xlangb1": self.xlangb1,
            "xlangb2": self.xlangb2,
            "xlangb3": self.xlangb3,
            "tag": self.tag
        }

        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


def get_prompt(word, tlang, langa, langb):

    if langb != "":

        prompt = f"""Task: Create one entry of this table with examples and translations for the word {word} in {tlang} to {langa} and {langb}. The examples should have a focus on giving a good context and intuition for the word that is being learned. Paste only the final table.
Header:
- Russian: {word} in its original or primitive form
- English: Translation to English
- Spanish: Translation to Spanish
- Russian 1: First sentence or expression
- Russian 2: Second sentence or expression
- Russian 3: Third sentence or expression
- English 1: Translation of Russian 1
- English 2: Translation of Russian 2
- English 3: Translation of Russian 3
- Spanish 1: Translation of Russian 1
- Spanish 2: Translation of Russian 2
- Spanish 3: Translation of Russian 3

Example:
| {tlang}   | {langa}  | {langb}   | {tlang} 1                        | {tlang} 2                    | {tlang} 3                      | {langa} 1                    | {langa} 2                    | {langa} 3                      | {langb} 1                      | {langb} 2                    | {langb} 3                      |
|-----------|----------|-----------|----------------------------------|------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------|--------------------------------|------------------------------|--------------------------------|
"""
    else:

        prompt = f"""Task: Create one entry of this table with translations for the word {word} in {tlang} to {langa}. Provide examples, which should have a focus on giving a good context and intuition for the word that is being learned. Paste only the final table.

Table: 
| {tlang}   | {langa}  | {langb}   | Example {tlang} 1                        | Example {tlang} 2                    | Example {tlang} 3                      | Example {langa} 1                    | Example {langa} 2                    | Example {langa} 3                      |                   |
|-----------|----------|-----------|----------------------------------|------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------|
"""
    return prompt 


def normalize_input(input_string):
    elements = re.split(r'[,\s]+', input_string)
    elements = [elem.strip('"') for elem in elements if elem]
    return elements




if __name__ == "__main__":

    # INPUT
    with open('input.txt', 'r', encoding='utf-8') as file:
        words = file.read()

    normalized_words = normalize_input(words)

#     proceed = input(f"""
# The following words will be processed: {normalized_words}
# Do you want to proceed? (y/n): """)
    
    # if proceed.lower() != "y":
    #     exit()

    # name = input("Enter the name of the deck: ")
    # if name == "":
    #     name = "deck"
    name = "deck"
    
    # tlang = ""
    # while tlang == "":
    #     tlang = input("Enter the target language: ")
    #     if tlang == "":
    #         print("Target language is required.")
    #     if tlang.lower() == "exit":
    #         exit()
    # tlang = tlang[0].upper() + tlang[1:].lower()

    # langa = ""
    # while langa == "":
    #     langa = input("Enter the first language: ")
    #     if langa == "":
    #         print("First language is required.")
    #     if langa.lower() == "exit":
    #         exit()
    # langa = langa[0].upper() + langa[1:].lower()
    
    # langb = input("Enter the second language: ")
    # if langb.lower() == "exit":
    #     exit()
    # if langb != "":
    #     langb = langb[0].upper() + langb[1:].lower()
    
    tlang = "Spanish"
    langa = "English"
    langb = ""

    metadata = {
        "words": normalized_words,
        "length": len(normalized_words),
        "name": name,
        "filename": f'data/{name}.json',
        "tlang": tlang,
        "langa": langa,
        "langb": langb,
    }

    # INITIALIZATION
    for i in range(metadata["length"]):
        word = Word(i+1, metadata["filename"])
        word.initialize(metadata)
        word.update()
        if i % 20 == 0:
            print(f"{i} words processed")

    # CREATION
        

    # for i in range(483,484):
    #     word = Word(i)

    #     prompt = get_prompt(word.tlang, word.tag)

    #     response = ask(prompt)

    #     data_row = response.split("-|")[-1].strip()
        
    #     data_array = data_row.split("|")

    #     word.langa = data_array[2].strip()
    #     word.langb = data_array[3].strip()
    #     word.xtlang1 = data_array[4].strip()
    #     word.xtlang2 = data_array[5].strip()
    #     word.xtlang3 = data_array[6].strip()
    #     word.xlanga1 = data_array[7].strip()
    #     word.xlanga2 = data_array[8].strip()
    #     word.xlanga3 = data_array[9].strip()
    #     word.xlangb1 = data_array[10].strip()
    #     word.xlangb2 = data_array[11].strip()
    #     word.xlangb3 = data_array[12].strip()

    #     word.update()

    #     if i % 50 == 0:
    #         print(f"{i} words processed")

    # CONVERSION

    # table = []
    # for i in range(1,501):
    #     word = Word(i)
    #     row = [word.top, word.tlang, "", word.langa, word.langb, word.xtlang1, word.xtlang2, word.xtlang3, "", "", "", word.xlanga1, word.xlanga2, word.xlanga3, word.xlangb1, word.xlangb2, word.xlangb3, word.tag]
    #     table.append(row)

    # create_flashcards(table)
