import shutil
import os
import requests
import openai
from openai import OpenAI
from datetime import datetime as dt
from PIL import Image 

#user login
inputuser=input('enter your OpenAI username: ')
os.environ["OPENAI_API_KEY"] = getpass('enter your OpenAI API key: ')

#gpt prompt creation
def create_prompt(title):
    prompt="""
Biography:
My name is Darin and I am a Python student.

Blog
Title: {}
tags: tech, python, coding, AI, machine learning
Summary: I learn about what Python can hold for the future of AI. Please do not exceed 2 paragraphs in total response length.
Full text: """.format(title) #070224 added 'Do not exceed 2 paragraphs.' based on max token length of 250
    return prompt

#gpt api call
client = OpenAI()

completion=client.completions.create(
                model='gpt-3.5-turbo-instruct',
                prompt=create_prompt(title),
                max_tokens=250, #length of output
                temperature=0.7, # 0 to 1, only change top p or temperature , 0 is the most probable, 1 takes more risks
                top_p = 1.0, #only change top p or temperature, 1 is default, 0.1 is top 10% most probable
                frequency_penalty=0, #-2 to 2, positive value penalizes new tokens if they exist, decreaseing probabiolity of repeating text
                presence_penalty=0, #-2 to 2, positive penalize new tokens if they appear, but thinks about tokens, value too high creates low probability
                n = 1, #number or results to be rewturned, 1 is default, use when temp is zero to min repeating results
                # stop = ['/n'],
)         
blog_content=completion.choices[0].text
print(blog_content)

#image title
def dalle3_prompt(title):
    prompt=f"Sci-fi art showing a movie scene with {title}, extremely detailed and mesmerizing."
    return prompt #added extremely detailed and mesmerizing 070224
image_prompt=dalle3_prompt(title)

#naming and saving image
dname = dt.now().strftime('%m-%d-%Y %H:%M:%S').replace("-",'').replace(":",'').replace(' ','-')
img_filename = 'BLOG-image_' + dname +'.png'

#grabs the url from the model_dump and adds it to empty list
image_url_list=[]
for item in images_response.data:
    image_url_list.append(item.model_dump()["url"])
    
#grabs string from the list
image_url=item.model_dump()["url"]

#downloading image from url
with open(img_filename,'wb') as f:
    shutil.copyfileobj(requests.get(image_url, stream=True).raw, f)
print(img_filename,'downloaded')

client = OpenAI()  # will use environment variable "OPENAI_API_KEY"

prompt = image_prompt

#dalle image api call
image_params = {
 "model": "dall-e-3",  # Defaults to dall-e-2
 "n": 1,               # Between 2 and 10 is only for DALL-E 2
 "size": "1024x1024",  # 256x256, 512x512 only for DALL-E 2 - not much cheaper - 1024x1024, 1024x1792 or 1792x1024 available for DALL-E 3
 "prompt": prompt,     # DALL-E 3: max 4000 characters, DALL-E 2: max 1000
 "user": main.inputuser,     # pass a customer ID to OpenAI for abuse monitoring
}
images_response = client.images.generate(**image_params)