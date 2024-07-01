import os
import openai
import yaml

CONTEXT_PROMPT = "Tu es un agent chargé d'écrire dans le style d'Elisabeth Moreno. On te posera une question sur un sujet auquel tu devras répondre en te considérant comme Elisabeth Moreno. Réponds à la première personne."
POST_PROMPT = "Nous allons travailler en 2 étapes. 1- D'abord, réalise-moi un résumé de la réponse en 5 phrases. 2- Ensuite, modifie ce résumé en un texte comme s'il était récité à l'oral dans le cadre d'une interview. Ce texte ne doit pas faire plus de 5 phrases. <texte> {answer} </texte>. Ressors le résumé entre tags <summary></summary>, puis le texte modifié entre tags <output></output>."

#PROJECT_CONFIG = yaml.safe_load(os.getenv("PROJECT_CONFIG"))
#with open("project_config.yml", 'r', encoding='utf-8') as stream:
#    PROJECT_CONFIG = yaml.safe_load(stream)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Your API key for authentication

def generate_answer(sentence):
    client = openai.OpenAI(api_key=openai.api_key)
    responseQ1 = client.chat.completions.create(
        model = "gpt-4o",
        messages=[
            {"role": "system", "content": CONTEXT_PROMPT + POST_PROMPT},
            {"role": "user", "content": sentence}
        ]
    )
    message = responseQ1.choices[0].message
    return message.content
