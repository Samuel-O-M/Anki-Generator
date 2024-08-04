from flashcardCreator import *
from chatGPTapi import *
import random
import json
import os
import re


class Word:
    def __init__(self, top):

        self._top = str(top)

        if not os.path.exists('data/cards.json'):
            with open('data/cards.json', 'w', encoding='utf-8') as file:
                json.dump({}, file)

        try:
            with open('data/cards.json', 'r', encoding='utf-8') as file:
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

    def initialize(self, driver):
        word, category = rank(self.top)
        self._tlang = stress_mark(word, driver)

        if category == "other" and (categorize(word) == "pronoun" or categorize(word) == "error"):
            self._tag = "error"
        else:
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
            with open('data/cards.json', 'r', encoding='utf-8') as file:
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

        with open('data/cards.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


def get_prompt(word, tag):

    criteria = ""
    indication1 = ""
    indication2 = ""
    indication3 = ""

    if tag == "noun" or tag == "adjective":
        criteria = "\nCriteria:\n"
        criteria += "Ensure using a different declension for each sentence or expression. Always use the singular form."
        indication1 = "using a declension"
        indication2 = "using another declension"
        indication3 = "using a different declension"

    if tag == "pronoun":
        criteria = "\nCriteria:\n"
        criteria += "Ensure using different variations for each sentence or expression. which can include gender or case. None of the examples can be nominative."
        indication1 = "using a variation"
        indication2 = "using another variation"
        indication3 = "using a different variation"

    if tag == "verb":
        choice1 = random.choice(['я', 'ты', random.choice(['он', 'она'])])
        choice2 = random.choice(['мы', 'вы', 'они'])
        criteria = "\nCriteria:\n"
        criteria += f"Ensure using different conjugations for each sentence or expression. Include one example conjugation with {choice1} in present tense, one example conjugation with {choice2}, and one example conjugation in past tense."
        indication1 = "using a conjugation in present tense with " + choice1
        indication2 = "using a conjugation in present tense with " + choice2
        indication3 = "using a conjugation in past tense"

    if tag == "adverb" or tag == "numeral":
        criteria = "\nCriteria:\n"
        criteria += "Ensure using the original form for the first example and two different variations for the other examples."
        indication1 = "using the original form"
        indication2 = "using another variation"
        indication3 = "using a different variation"

    prompt = f"""Task: Create one entry of this table with examples and translations for the word {word} to english and spanish. The examples should have a focus on giving a good context and intuition for the word that is being learned. Paste only the final table.
{criteria}

Header:
- Russian: {word} in its original or primitive form
- English: Translation to English
- Spanish: Translation to Spanish
- Russian 1: First sentence or expression {indication1} 
- Russian 2: Second sentence or expression {indication2}
- Russian 3: Third sentence or expression {indication3}
- English 1: Translation of Russian 1
- English 2: Translation of Russian 2
- English 3: Translation of Russian 3
- Spanish 1: Translation of Russian 1
- Spanish 2: Translation of Russian 2
- Spanish 3: Translation of Russian 3
    
Example:
| Russian   | English  | Spanish   | Russian 1                        | Russian 2                    | Russian 3                      | English 1                    | English 2                    | English 3                      | Spanish 1                      | Spanish 2                    | Spanish 3                      |
|-----------|----------|-----------|----------------------------------|------------------------------|--------------------------------|------------------------------|------------------------------|--------------------------------|--------------------------------|------------------------------|--------------------------------|
| человек   | person   | persona    | Я встретил интересного человека. | Он стал хорошим человеком.   | Человеку свойственно ошибаться. | I met an interesting person. | He became a good person.     | It's human to make mistakes.  | Conocí a una persona interesante. | Él se convirtió en una buena persona. | Es humano equivocarse.       |"""

    return prompt

def normalize_input(input_string):
    elements = re.split(r'[,\s]+', input_string)
    elements = [elem.strip('"') for elem in elements if elem]
    return elements




if __name__ == "__main__":

    # INPUT
    words = normalize_input(input("Enter the words to process: "))
    proceed = input(f"""
The following words will be processed: {words}
Do you want to proceed? (y/n): """)
    
    if proceed.lower() != "y":
        exit()

    name = input("Enter the name of the deck: ")
    if name == "":
        name = "deck"
    
    tlang = ""
    while tlang == "":
        tlang = input("Enter the target language: ")
        if tlang == "":
            print("Target language is required.")
        if tlang.lower() == "exit":
            exit()
    tlang = tlang[0].upper() + tlang[1:].lower()

    langa = ""
    while langa == "":
        langa = input("Enter the first language: ")
        if langa == "":
            print("First language is required.")
        if langa.lower() == "exit":
            exit()
    langa = langa[0].upper() + langa[1:].lower()
    
    langb = input("Enter the second language: ")
    if langb.lower() == "exit":
        exit()
    langb = langb[0].upper() + langb[1:].lower()
    


    # for i in range(1,501):
    #     word = Word(i)
    #     word.initialize(driver)
    #     word.update()
    #     if i % 20 == 0:
    #         print(f"{i} words processed")

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

    # STRESS MARKS
#     driver = setup_driver()
#     for i in range(1,501):

#         word = Word(i)
#         word.xtlang1 = stress_mark(word.xtlang1, driver)
#         word.xtlang2 = stress_mark(word.xtlang2, driver)
#         word.xtlang3 = stress_mark(word.xtlang3, driver)
        
#         if "|" in word.xtlang1:
#             prompt = f"""Task: Correct the stress mark in the sentence {word.xtlang1} and paste the corrected sentence.
# Provide only the requested answer

# Example: 
# Она́ сто́ит|стои́т на по́диуме и выступа́ет.
# returns
# Она́ стои́т на по́диуме и выступа́ет."""
#             word.xtlang1 = ask(prompt)
#         if "|" in word.xtlang2:
#             prompt = f"""Task: Correct the stress mark in the sentence {word.xtlang2} and paste the corrected sentence.
# Provide only the requested answer

# Example: 
# Она́ сто́ит|стои́т на по́диуме и выступа́ет.
# returns
# Она́ стои́т на по́диуме и выступа́ет."""
#             word.xtlang2 = ask(prompt)
#         if "|" in word.xtlang3:
#             prompt = f"""Task: Correct the stress mark in the sentence {word.xtlang3} and paste the corrected sentence.
# Provide only the requested answer

# Example: 
# Она́ сто́ит|стои́т на по́диуме и выступа́ет.
# returns
# Она́ стои́т на по́диуме и выступа́ет."""
#             word.xtlang3 = ask(prompt)
        
#         word.update()
#         print(word.xtlang1)

#     close_driver(driver)


    