from scrapers.wikitionary import *
from flashcardCreator import *
from chatGPTapi import *
import random
import json
import os
import re


class Word:
    def __init__(self, top, file_name='data/cards.json'):

        self._top = str(top)
        self.file_name = file_name

        if not os.path.exists(self.file_name):
            with open(self.file_name, 'w', encoding='utf-8') as file:
                json.dump({}, file)

        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(self._top, str) and self._top in data:
                    self._word_t = data[self._top].get("word_t", "")
                    self.word_a = data[self._top].get("word_a", "")
                    self.word_b = data[self._top].get("word_b", "")
                    self.example_t_1 = data[self._top].get("example_t_1", "")
                    self.example_t_2 = data[self._top].get("example_t_2", "")
                    self.example_t_3 = data[self._top].get("example_t_3", "")
                    self.example_a_1 = data[self._top].get("example_a_1", "")
                    self.example_a_2 = data[self._top].get("example_a_2", "")
                    self.example_a_3 = data[self._top].get("example_a_3", "")
                    self.example_b_1 = data[self._top].get("example_b_1", "")
                    self.example_b_2 = data[self._top].get("example_b_2", "")
                    self.example_b_3 = data[self._top].get("example_b_3", "")
                    self._tag = data[self._top].get("tag", "")
                else:
                    self.clear()
        except FileNotFoundError:
            self.clear()
        except json.JSONDecodeError:
            self.clear()

    def initialize(self, word_t, language_t):
        self._word_t = word_t
        category = categorize(word_t, language_t)
        self._tag = category
    
    def clear(self):
        self._word_t = ""
        self.word_a = ""
        self.word_b = ""
        self.example_t_1 = ""
        self.example_t_2 = ""
        self.example_t_3 = ""
        self.example_a_1 = ""
        self.example_a_2 = ""
        self.example_a_3 = ""
        self.example_b_1 = ""
        self.example_b_2 = ""
        self.example_b_3 = ""
        self._tag = ""

    @property
    def top(self):
        return self._top
    
    @property
    def word_t(self):
        return self._word_t
    
    @property
    def tag(self):
        return self._tag

    def update(self):
        try:
            with open(self.file_name, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        data[self._top] = {
            "word_t": self.word_t,
            "word_a": self.word_a,
            "word_b": self.word_b,
            "example_t_1": self.example_t_1,
            "example_t_2": self.example_t_2,
            "example_t_3": self.example_t_3,
            "example_a_1": self.example_a_1,
            "example_a_2": self.example_a_2,
            "example_a_3": self.example_a_3,
            "example_b_1": self.example_b_1,
            "example_b_2": self.example_b_2,
            "example_b_3": self.example_b_3,
            "tag": self.tag
        }

        with open(self.file_name, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


def get_prompt(word, language_t, language_a, language_b):

    if language_b != "":

        prompt = f"""Task: Create one entry of this table with translations for the word {word} in {language_t} to {language_a} and {language_b}. Provide examples, which should have a focus on giving a good context and intuition for the word that is being learned. In the examples, highlight the word, for example **{word}**. Do not highlight it outside of the examples. Paste only the final table.

Table: 
| {language_t}   | {language_a}  | {language_b}  | Example {language_t} 1                        | Example {language_t} 2                    | Example {language_t} 3                      | Example {language_a} 1                    | Example {language_a} 2                    | Example {language_a} 3                      | Example {language_b} 1                    | Example {language_b} 2                    | Example {language_b} 3                      |
|-----------|----------|----------|----------------------------------|------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------|-----------------------------|------------------------------|--------------------------------|
"""
    else:

        prompt = f"""Task: Create one entry of this table with translations for the word {word} in {language_t} to {language_a}. Provide examples, which should have a focus on giving a good context and intuition for the word that is being learned. In the examples, highlight the word, for example **{word}**. Do not highlight it outside of the examples. Paste only the final table.

Table: 
| {language_t}   | {language_a}  | Example {language_t} 1                        | Example {language_t} 2                    | Example {language_t} 3                      | Example {language_a} 1                    | Example {language_a} 2                    | Example {language_a} 3                      |
|-----------|----------|----------------------------------|------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------|
"""
    return prompt 


def normalize_input(input_string):
    elements = re.split(r'[,\s]+', input_string)
    elements = [elem.strip('"') for elem in elements if elem]
    return elements


if __name__ == "__main__":


    # INPUT

    with open('input.txt', 'r', encoding='utf-8') as file:
        read_words = file.read()

    normalized_words = normalize_input(read_words)
    words = [word for word in normalized_words if word]
    length = len(words)

#     proceed = input(f"""
# The following words will be processed: {normalized_words}
# Do you want to proceed? (y/n): """)
    
    # if proceed.lower() != "y":
    #     exit()

    # name = input("Enter the name of the deck: ")
    # if name == "":
    #     name = "deck"
    name = "deck"
    file_name = f'data/{name}.json'
    
    # language_t = ""
    # while language_t == "":
    #     language_t = input("Enter the target language: ")
    #     if language_t == "":
    #         print("Target language is required.")
    #     if language_t.lower() == "exit":
    #         exit()
    # language_t = language_t[0].upper() + language_t[1:].lower()

    # language_a = ""
    # while language_a == "":
    #     language_a = input("Enter the first language: ")
    #     if language_a == "":
    #         print("First language is required.")
    #     if language_a.lower() == "exit":
    #         exit()
    # language_a = language_a[0].upper() + language_a[1:].lower()
    
    # language_b = input("Enter the second language: ")
    # if language_b.lower() == "exit":
    #     exit()
    # if language_b != "":
    #     language_b = language_b[0].upper() + language_b[1:].lower()
    
    language_t = "Spanish"
    language_a = "English"
    language_b = "French"


    # INITIALIZATION

    for i in range(length):
        word = Word(i+1, file_name)
        word.initialize(words[i], language_t)
        word.update()
        if i % 50 == 0 and i != 0:
            print(f"{i} words initialized")


    # CREATION

    for i in range(length):

        word = Word(i+1, file_name)
        prompt = get_prompt(word.word_t, language_t, language_a, language_b)
        response = ask(prompt)
        print(response+"\n"*3)

        if language_b != "":
            data_row = response.split("-|")[-1].strip()
            
            data_array = data_row.split("|")

            word.word_a = data_array[2].strip()
            word.word_b = data_array[3].strip()
            word.example_t_1 = data_array[4].strip()
            word.example_t_2 = data_array[5].strip()
            word.example_t_3 = data_array[6].strip()
            word.example_a_1 = data_array[7].strip()
            word.example_a_2 = data_array[8].strip()
            word.example_a_3 = data_array[9].strip()
            word.example_b_1 = data_array[10].strip()
            word.example_b_2 = data_array[11].strip()
            word.example_b_3 = data_array[12].strip()

        else: 
            data_row = response.split("-|")[-1].strip()
            
            data_array = data_row.split("|")

            word.word_a = data_array[2].strip()
            word.example_t_1 = data_array[3].strip()
            word.example_t_2 = data_array[4].strip()
            word.example_t_3 = data_array[5].strip()
            word.example_a_1 = data_array[6].strip()
            word.example_a_2 = data_array[7].strip()
            word.example_a_3 = data_array[8].strip()
        
        word.update()

        if i % 50 == 0 and i != 0:
            print(f"{i} words created")


    # CONVERSION

    if language_b != "":
        header = ["Top", {language_t}, "Audio", {language_a}, {language_b}, f"Example {language_t} 1", f"Example {language_t} 2", f"Example {language_t} 3", "Audio 1", "Audio 2", "Audio 3", f"Example {language_a} 1", f"Example {language_a} 2", f"Example {language_a} 3", f"Example {language_b} 1", f"Example {language_b} 2", f"Example {language_b} 3", "Tag"]
    else:
        header = ["Top", {language_t}, "Audio", {language_a}, "", f"Example {language_t} 1", f"Example {language_t} 2", f"Example {language_t} 3", "Audio 1", "Audio 2", "Audio 3", f"Example {language_a} 1", f"Example {language_a} 2", f"Example {language_a} 3", "", "", "", "Tag"]

    
    content = []

    for i in range(length):
        word = Word(i+1, file_name)

        row = [word.top, word.word_t, "", word.word_a, word.word_b, word.example_t_1, word.example_t_2, word.example_t_3, "", "", "", word.example_a_1, word.example_a_2, word.example_a_3, word.example_b_1, word.example_b_2, word.example_b_3, word.tag]

        content.append(row)
    
    create_flashcards(header, content)
