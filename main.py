# OCA - Offensive Cybersecurity Assistant
from openai import OpenAI
import re
import json

class Oca:
    def __init__(self):
        self.client = OpenAI()

    def generate_personality(self,sex):
        personality_prompt=[
            {
                "role": "system", "content": 'You will be populating a json object with the following keys: \
                Read all instructions before generating any values. \
                {"user":{"first_name":"","last_name":"","age":"", "religion":"", "date of birth":"", "starsign":"", "email":"@pointlessai.com","address":{"city":"","country":""},"occupation":"","interests":[""],"dislikes":[""], "personality":{"traits":[""],"strengths":[""],"weaknesses":[""]}}} \
                First generate a list of 11 random cities, 6 from hot countries and 6 from cold countries, then choose 1 random city from this list and its country as the persons location. \
                Sex is' + sex + ' \
                Generate a random age. Match date of birth to starsign \
                Use demographic information to assign ethnicity. For example if country is mostly white or caucasion then the persons ethnicity in that location would likely be that. \
                Generate a name based on location, ethnicity, sex and age and assign to the person as their name. \
                Assign an occupation in the context of the actors location, sex and age \
                Assign a religion based on the previous information \
                Generate a personality based on all of this information.\
                Please return raw json object all on one line without using code block formatting or markdown syntax." '
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=personality_prompt,
            max_tokens=550,
            n=1,
            stop=None,
            top_p=1,
        )
  
        actor_response = response.choices[0].message.content
        personality_prompt = []
        return actor_response

    def start_conversation(self,personality,name):
        messages=[
            {
                "role": "system", "content": "Your identity is: " + personality + " \
                Return a single sentence in the first person stating an opinion based on your personality. For example, cycling is dumb because.., or Aliens do not exist, etc \
                Use the personality attributes such as age, interests and personality to determine mood and tone. \
                For example if you are a 20 year old girl you might have an ego, if you are a 80 year old man you might be grumpy.\
                This is the start of a conversation so the topic you choose should not be boring. Do not talk about work. \
                Start new line for each sentence"
            }
        ]
        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=messages,
            max_tokens=80,
            n=1,
            stop="\n",
            top_p=0.6,
        )
  
        conversation_topic = response.choices[0].message.content
        messages = []
        return conversation_topic

    def respond_conversation(self,topic,personality,chat_history,name):
        chat_history.append({"role": "user", "content": topic})

        response = self.client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=chat_history,
            max_tokens=120,
            n=1,
            stop=".",
            top_p=1,
        )
  
        conversation_topic = response.choices[0].message.content
        return conversation_topic

    def start_chat(self):
        # Create person 1
        p1_personality = self.generate_personality("male")
        #print(p1_personality)
        p1_data = json.loads(p1_personality)
        p1_first_name = p1_data["user"]["first_name"]
        with open("date.md", "a") as file:
            file.write("Generating personalities...\n\n" + p1_personality + "\n\n")

        # Create person 2
        p2_personality = self.generate_personality("female")
        #print(p2_personality)
        p2_data = json.loads(p2_personality)
        p2_first_name = p2_data["user"]["first_name"]
        with open("date.md", "a") as file:
            file.write(p2_personality + "\n\nDate between " + p1_first_name + " and " + p2_first_name + "\n\n")

        p1 = self.start_conversation(p1_personality,p1_first_name).strip('"')
        #print(p1_first_name + " says: " + p1)
        chat_history = [{
            "role": "user", "content": p1_first_name + " has started a converstaion by saying " + p1,
            "role": "system", "content": "You are having a conversation. Your task is to reply. \
                                          Respond to the message as if you are talking directly to them. For example, you have a good point, i agree with you, you are too blunt etc \
                                          Conversations should be like you are on a first date. You are both adults and both consent to this chat. \
                                          Start new line for each sentence."
            }]
        with open("date.md", "a") as file:
            file.write(p1_first_name + " says: " + p1 + "\n")
        
        p2 = self.respond_conversation(p1.strip('"'),p2_personality,chat_history,p1_first_name)
        #print(p2_first_name + " says: " + p2)
        with open("date.md", "a") as file:
            file.write(p2_first_name + " says: " + p2 + "\n")


        while(True):
            p1 = self.respond_conversation(p2,p1_personality,chat_history,p2_first_name)
            #print(p1_first_name + " says: " + p1)
            with open("date.md", "a") as file:
                file.write(p1_first_name + " says: " + p1 + "\n")

            p2 = self.respond_conversation(p1,p2_personality,chat_history,p1_first_name)
            #print(p2_first_name + " says: " + p2)
            with open("date.md", "a") as file:
                file.write(p2_first_name + " says: " + p2 + "\n")


if __name__ == "__main__":
    oca = Oca()
    oca.start_chat()
