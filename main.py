from scrappers.stressMark import *
from scrappers.frequencyList import *
from scrappers.wikitionary import *
from flashcardCreator import *
from chatGPTapi import *
import random
import json
import os

# def get_top(n):
#     n = str(n)    
#     with open('data/top.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     return data.get(n, "Key not found")

# def get_top_s(n):
#     n = str(n)    
#     with open('data/top_s.json', 'r', encoding='utf-8') as file:
#         data = json.load(file)
#     return data.get(n, "Key not found")

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
                    self._ru = data[self._top].get("ru", "")
                    self.en = data[self._top].get("en", "")
                    self.es = data[self._top].get("es", "")
                    self.xru1 = data[self._top].get("xru1", "")
                    self.xru2 = data[self._top].get("xru2", "")
                    self.xru3 = data[self._top].get("xru3", "")
                    self.xen1 = data[self._top].get("xen1", "")
                    self.xen2 = data[self._top].get("xen2", "")
                    self.xen3 = data[self._top].get("xen3", "")
                    self.xes1 = data[self._top].get("xes1", "")
                    self.xes2 = data[self._top].get("xes2", "")
                    self.xes3 = data[self._top].get("xes3", "")
                    self._tag = data[self._top].get("tag", "")
                else:
                    self.clear()
        except FileNotFoundError:
            self.clear()
        except json.JSONDecodeError:
            self.clear()

    def initialize(self, driver):
        word, category = rank(self.top)
        self._ru = stress_mark(word, driver)

        if category == "other" and (categorize(word) == "pronoun" or categorize(word) == "error"):
            self._tag = "error"
        else:
            self._tag = category
    
    def clear(self):
        self._ru = ""
        self.en = ""
        self.es = ""
        self.xru1 = ""
        self.xru2 = ""
        self.xru3 = ""
        self.xen1 = ""
        self.xen2 = ""
        self.xen3 = ""
        self.xes1 = ""
        self.xes2 = ""
        self.xes3 = ""
        self._tag = ""
    
    @property
    def top(self):
        return self._top
    
    @property
    def ru(self):
        return self._ru
    
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
            "ru": self.ru,
            "en": self.en,
            "es": self.es,
            "xru1": self.xru1,
            "xru2": self.xru2,
            "xru3": self.xru3,
            "xen1": self.xen1,
            "xen2": self.xen2,
            "xen3": self.xen3,
            "xes1": self.xes1,
            "xes2": self.xes2,
            "xes3": self.xes3,
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





if __name__ == "__main__":

    # INITIALIZATION
    # for i in range(1,501):
    #     word = Word(i)
    #     word.initialize(driver)
    #     word.update()
    #     if i % 20 == 0:
    #         print(f"{i} words processed")

    # CREATION
    # for i in range(483,484):
    #     word = Word(i)

    #     prompt = get_prompt(word.ru, word.tag)

    #     response = ask(prompt)

    #     data_row = response.split("-|")[-1].strip()
        
    #     data_array = data_row.split("|")

    #     word.en = data_array[2].strip()
    #     word.es = data_array[3].strip()
    #     word.xru1 = data_array[4].strip()
    #     word.xru2 = data_array[5].strip()
    #     word.xru3 = data_array[6].strip()
    #     word.xen1 = data_array[7].strip()
    #     word.xen2 = data_array[8].strip()
    #     word.xen3 = data_array[9].strip()
    #     word.xes1 = data_array[10].strip()
    #     word.xes2 = data_array[11].strip()
    #     word.xes3 = data_array[12].strip()

    #     word.update()

    #     if i % 50 == 0:
    #         print(f"{i} words processed")

    # CONVERSION
    # table = []
    # for i in range(1,501):
    #     word = Word(i)
    #     row = [word.top, word.ru, "", word.en, word.es, word.xru1, word.xru2, word.xru3, "", "", "", word.xen1, word.xen2, word.xen3, word.xes1, word.xes2, word.xes3, word.tag]
    #     table.append(row)

    # create_flashcards(table)

    # STRESS MARKS
    driver = setup_driver()
    for i in range(1,501):

        word = Word(i)
        word.xru1 = stress_mark(word.xru1, driver)
        word.xru2 = stress_mark(word.xru2, driver)
        word.xru3 = stress_mark(word.xru3, driver)
        
        if "|" in word.xru1:
            prompt = f"""Task: Correct the stress mark in the sentence {word.xru1} and paste the corrected sentence.
Provide only the requested answer

Example: 
Она́ сто́ит|стои́т на по́диуме и выступа́ет.
returns
Она́ стои́т на по́диуме и выступа́ет."""
            word.xru1 = ask(prompt)
        if "|" in word.xru2:
            prompt = f"""Task: Correct the stress mark in the sentence {word.xru2} and paste the corrected sentence.
Provide only the requested answer

Example: 
Она́ сто́ит|стои́т на по́диуме и выступа́ет.
returns
Она́ стои́т на по́диуме и выступа́ет."""
            word.xru2 = ask(prompt)
        if "|" in word.xru3:
            prompt = f"""Task: Correct the stress mark in the sentence {word.xru3} and paste the corrected sentence.
Provide only the requested answer

Example: 
Она́ сто́ит|стои́т на по́диуме и выступа́ет.
returns
Она́ стои́т на по́диуме и выступа́ет."""
            word.xru3 = ask(prompt)
        
        word.update()
        print(word.xru1)

    close_driver(driver)