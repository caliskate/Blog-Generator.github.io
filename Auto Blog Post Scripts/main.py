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
from getpass import getpass

#Define your paths here



#git repo folder - the folder that holds the changes and commits
#PATH_TO_BLOG_REPO = Path('C/path/to/.git')
PATH_TO_BLOG_REPO = Path('C:\\Users\\DARiN\\Documents\\Python-JL\\Github\\caliskate.github.io\\.git')
#main folder to inject the index.html files
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
#content subfolder where we will put the blog content
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
#creates content folder
PATH_TO_CONTENT.mkdir(exist_ok=True,parents=True)
###

#Define your title here
title = "Python and the Future of AI" #fixed format 070224
print(openai_utils.create_prompt(title))

#Get Blog Content from openai
blog_content = openai_utils.get_blog_from_openai(title)

#Get the cover image and create the blog
_, cover_image_save_path = openai_utils.get_cover_image(title, "cover_image.png")
path_to_new_content = blog_utils.create_new_blog(PATH_TO_CONTENT, title, blog_content, cover_image_save_path)
blog_utils.write_to_index(PATH_TO_BLOG, path_to_new_content)

#Update the blog
blog_utils.update_blog(PATH_TO_BLOG_REPO)

