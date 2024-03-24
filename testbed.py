# OCA - Offensive Cybersecurity Assistant
from openai import OpenAI
import os
import subprocess
import sys
import re

class Oca:
    def __init__(self):
        self.client = OpenAI()

    def generate_personality(self):
        messages=[
            {
                "role": "system", "content": 'Create an actor. Return a random json object with their attributes in the format: \
                {"user":{"first_name":"","last_name":"","age":"", "religion":"", "date of birth":"", "starsign":"", "email":"@pointlessai.com","address":{"city":"","country":""},"occupation":"","interests":[""],"dislikes":[""], "personality":{"traits":[""],"strengths":[""],"weaknesses":[""]}}} \
                First generate city and country, then choose a random first and last name used in this location. \
                Generate a random demographic, male or female, age 18 - 80. Match date of birth to starsign \
                Assign an occupation in the context of the actors location, sex and age \
                Assign a religion based on the previous information \
                Generate a personality based on all of this information. \
                Please return raw json object without using code block formatting or markdown syntax." '
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            max_tokens=550,
            n=1,
            stop=None,
            top_p=0.4,
        )
  
        actor_response = response.choices[0].message.content
        cleaned_response = re.sub(r'^```json\s*', '', actor_response, flags=re.MULTILINE)
        cleaned_response = cleaned_response.replace('```', '')

        # Write cleaned response to a file
        with open("cleaned_response.json", "w") as file:
            file.write(cleaned_response)
        return cleaned_response

    def start_chat(self):
        personality = self.generate_personality()
        print(personality)


if __name__ == "__main__":
    oca = Oca()
    oca.start_chat()