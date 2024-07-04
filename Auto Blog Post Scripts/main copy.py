# installs as needed
# !pip install openai
# !pip install --upgrade openai
# !pip install --upgrade pip
# !pip install GitPython
# !pip install beautifulsoup4

# image processing
# !pip install pillow
# !pip install pydantic

from pathlib import Path
import blog_utils
import openai_utils
# from openai_utils import img_filename

from getpass import getpass #main
import openai #aiutils
from openai import OpenAI #aiutils
import os #aiutilsd
from git import Repo #blog utils
#used for setting up paths and parent dir to github repository
from pathlib import Path #main and blogutil
import shutil
from bs4 import BeautifulSoup as Soup #blogutils
from PIL import Image #aiutils
from datetime import datetime as dt #aiutils -  for formatting date returned with images
import requests #aiutils - for downloading images from URLs

#main = define folder paths, combine files to create blog, push to git







#1 - Define your repo path

#git repo folder - the folder that holds the changes and commits
#PATH_TO_BLOG_REPO = Path('C/path/to/.git')
PATH_TO_BLOG_REPO = Path('C:\\Users\\DARiN\\Documents\\Python-JL\\Github\\caliskate.github.io\\.git')
#main folder to inject the index.html files
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
#content subfolder where we will put the blog content
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
#creates content folder
PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)


#2 - Define your title and get blog text
title = "Python and the Future of AI"
print(openai_utils.create_prompt(title))
blog_content = openai_utils.get_blog_from_openai(title)

#3 - Get Blog image from openai_utils using title and image name provided here
dname = dt.now().strftime('%m-%d-%Y %H:%M:%S').replace("-",'').replace(":",'').replace(' ','-')
img_filename = 'BLOG-image_' + dname +'.png'
_, cover_image_save_path = openai_utils.get_cover_image(title, img_filename)

#4 - Create the blog
path_to_new_content=blog_utils.create_new_blog(PATH_TO_CONTENT, title, blog_content, cover_image_save_path)
blog_utils.write_to_index(PATH_TO_BLOG, path_to_new_content)


#5 - Update the blog
blog_utils.update_blog(PATH_TO_BLOG_REPO)