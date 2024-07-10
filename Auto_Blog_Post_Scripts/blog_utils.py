from pathlib import Path
import shutil
import os
from bs4 import BeautifulSoup as Soup
from git import Repo

#blog utils summary = defines git push func, creating blog func, duplicate check, index writing

#cover_image - how is it linked to img_filename?

def create_new_blog(path_to_content, title, content, cover_image):
    #converts the img_filename into a path instead of a string
    cover_image = Path(cover_image)

    files = len(list(path_to_content.glob("*.html")))     #grab all html files and counts them
    new_title = f"{files+1}.html" #creates file and folder name by counting up by 1
    path_to_new_content = path_to_content/new_title #getting the file and making sure in correct dir
    
    shutil.copy(cover_image, path_to_content) #checks to make sure file name does not exist - prevents error or overwriting existing files
    if not os.path.exists(path_to_new_content):
        #write a new html file
        with open(path_to_new_content,"w") as f:
            #write commands for each line of the blog
            #write head of html open and close
            f.write("<!DOCTYPE HTML>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title>{title}</title>\n")
            f.write("</head>\n")
            #write body open and close with title, image and content
            f.write("<body>\n")
            f.write(f"<img src='{cover_image.name}' alt='Cover Image'> <br />\n")
            f.write(f"<h1> {title} </h1>")
            #open ai provides \n but we also want to replace that to include break statements
            #none type has no attribute replace
            f.write(content.replace("\n", "<br />\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print('Blog Created')
            return path_to_new_content
    else:
            raise FileExistsError("File name already exists")
    
#check for duplicate links, using href (the anchor tag for index.html)
def check_for_duplicate_links(path_to_new_content, links):
    urls = [str(link.get("href")) for link in links] #1.html,2.html,3.html
    content_path=str(Path(*path_to_new_content.parts[-2:])) # checks for index of 2 until the end ... would look like C:/UIsers/marci/file.../1.html
    return content_path in urls

def write_to_index(path_to_blog, path_to_new_content):
    with open(path_to_blog/'index.html') as index:
        soup = Soup(index.read()) #looks for all anchor tags then finds the last link
        
    links = soup.find_all('a')
    last_link = links[-1]

    if check_for_duplicate_links(path_to_new_content,links):
        raise ValueError("Link already exists!")
        # a lot of this takes advantage of what beautiful soup already has, need to familiarize what is has if you're working with html and the web
        #finds the path to the new content
    link_to_new_blog = soup.new_tag("a",href=Path(*path_to_new_content.parts[-2:]))
        #convert the path into a string and instert into a new blog
    link_to_new_blog.string = path_to_new_content.name.split('.')[0]
    last_link.insert_after(link_to_new_blog)

    with open(path_to_blog/'index.html','w') as f:
        f.write(str(soup.prettify(formatter='html'))) #prettify will separate long string into new lines

def update_blog(path_to_blog_repo, commit_message='Updates blog - rewrote code and gpt call to work in py modules'):
    #tells GitPython the Repo Location
    repo = Repo(path_to_blog_repo)
    #git add . (everything)
    repo.git.add(all=True)
    #git commit with some message (-m) "updates blog"
    repo.index.commit(commit_message)
    #git push
    origin = repo.remote(name='origin')
    print('successful push to github')
    origin.push()