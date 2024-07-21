from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

def ask(prompt):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a language assistant, skilled in creating enlightening examples to teach the russian language."},
        {"role": "user", "content": prompt}
    ]
    )

    return completion.choices[0].message.content


if __name__ == "__main__":

    print(ask("Translate the following sentence to Spanish: Я встретил интересного человека."))