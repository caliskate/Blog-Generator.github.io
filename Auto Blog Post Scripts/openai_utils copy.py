from ast import main
import shutil
import os
import requests
import openai
from openai import OpenAI
from datetime import datetime as dt
from PIL import Image 

from getpass import getpass


import openai #aiutils
from openai import OpenAI #aiutils
import os #aiutils
from git import Repo #blog utils
#used for setting up paths and parent dir to github repository
from pathlib import Path #main and blogutil
import shutil
from bs4 import BeautifulSoup as Soup #blogutils
from PIL import Image #aiutils
from datetime import datetime as dt #aiutils -  for formatting date returned with images
import requests #aiutils - for downloading images from URLs

#openai utils = login,api calls, text, title and image saving



#user login
inputuser=input('enter your OpenAI username: ')
os.environ["OPENAI_API_KEY"] = getpass('Paste your OpenAI API key and press enter (no text will show) : ')



#gpt api call
client = OpenAI()














#gpt prompt creation
def create_prompt(title):
    prompt="""
Biography:
My name is Darin and I am a Python student.

Blog
Title: Python and the Future of AI
tags: tech, python, coding, AI, machine learning
Summary: I learn about what Python can hold for the future of AI. Please do not exceed 2 paragraphs in total response length.
Full text: """.format(title) #070224 added 'Do not exceed 2 paragraphs.' based on max token length of 250
    return prompt


def get_blog_from_openai(blog_title):
    completion=client.completions.create(
                model='gpt-3.5-turbo-instruct',
                prompt=create_prompt(blog_title),
                max_tokens=250, #length of output
                temperature=0.7, # 0 to 1, only change top p or temperature , 0 is the most probable, 1 takes more risks
                top_p = 1.0, #only change top p or temperature, 1 is default, 0.1 is top 10% most probable
                frequency_penalty=0, #-2 to 2, positive value penalizes new tokens if they exist, decreaseing probabiolity of repeating text
                presence_penalty=0, #-2 to 2, positive penalize new tokens if they appear, but thinks about tokens, value too high creates low probability
                n = 1, #number or results to be returned, 1 is default, use when temp is zero to min repeating results
                # stop = ['/n'],
)     

    print(completion.choices[0].text)




#image title
def dalle3_prompt(title):
    prompt=f"Sci-fi art showing a movie scene with '{title}'. Extremely detailed and mesmerizing."
    return prompt #added extremely detailed and mesmerizing 070224








def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream = True)
    
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
    return image_res.status_code, file_name



#dalle image api call
def get_cover_image(title, save_path):
    images_response = client.images.generate(
                    model= "dall-e-3", 
                    n= 1,               # Between 2 and 10 is only for DALL-E 2
                    size= "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper - 1024x1024, 1024x1792 or 1792x1024 available for DALL-E 3
                    prompt=dalle3_prompt(title),     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
                    user= inputuser,      # pass a customer ID to OpenAI for abuse monitoring
                    quality="standard"
                    )
    image_url = images_response.data[0].url
    status_code, file_name = save_image(image_url, save_path)
    return status_code, file_name







