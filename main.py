import xml.etree.ElementTree as ET
import io
import pathlib
import webbrowser

def theme(title,content,date,catrgotie):
    return f'''
    <html>
        <head>
            <title>{title}</title>
            <meta charset="utf-8" />
            <link rel="stylesheet" href="../statics/main.css">
        </head>
        <body>
        <div id="wrp">
                <h2 id="title">{title}</h2>
                در تاریخ : <span id="date">{date}</span><br>
                با موضوع : <span id="catrgotie">{catrgotie}</span>
                <br><br>
                {content}
        </div>
        </body>
    </html>
    '''

files_posts = pathlib.Path('posts')
files_statics = pathlib.Path('statics')
try:
    files_posts.mkdir()
except FileExistsError:
    print("CoreMessage: Posts dir exists,Skipping ...")

try:
    files_statics.mkdir()
except FileExistsError:
    print("CoreMessage: Satatics dir exists,Skipping ... \n")

with io.open("./statics/main.css",'w',encoding='utf8') as file:
    file.write('''
        body {
          background-color: lightgray;
          font-weight: normal;
          font-size: 16px;
          font-family: Sahel,Vazir,Tahoma,Noto sans;
          direction: rtl;
        }
        pre {
            font-size: 12px;
            font-family: Monospace;
            direction: ltr;
        }
        #title {
            text-align: center;
        }
        #date {
            font-size: 15px;
        }
        #catrgotie {
            color:gray;
            font-size: 15px;
        }
        #wrp {
          background-color: white;
          margin: 10px;
          padding: 10px;
          box-shadow: 0 1px 6px 0 rgba(32, 33, 36, .78);
        }
    ''')


path = input("Enter path for blog.ir export of xml :")

try:
    tree = ET.parse(path)
    BLOG = tree.getroot()
except FileNotFoundError:
    print("File not found")
    exit()

log = True if input("Type log for to see the logs :").lower() == "log" else False

#INFO
BLOG_INFO = BLOG.findall('BLOG_INFO')
for BLOG_INFO_cur in BLOG_INFO:

    #GenInfo
    if log:
        print("Address :",BLOG_INFO_cur.find('DOMAIN').text.strip())
        print("Title :",BLOG_INFO_cur.find('TITLE').text.strip())
        print("Title :",BLOG_INFO_cur.find('TITLE').text.strip())
        print('')
        print('-' * 60)

    #Owner
    if log:
        print("Owner :",end=' ')
        OWNER = BLOG_INFO_cur.findall('OWNER')
        for OWNER_cur in OWNER:
            USER = OWNER_cur.findall('USER')
            for USER_cur in USER:
                print(USER_cur.find('FIRST_NAME').text.strip(),end=' ')
                print(USER_cur.find('LAST_NAME').text.strip(),end=' ')
        print('')
        print('-' * 60)

    #Authors
    if log:
        print("\nAuthors :",end='\n')
        AUTHORS = BLOG_INFO_cur.findall('AUTHORS')
        for AUTHORS_cur in AUTHORS:
            USER = AUTHORS_cur.findall('USER')
            for USER_cur in USER:
                print(USER_cur.find('FIRST_NAME').text.strip(),end=' ')
                print(USER_cur.find('LAST_NAME').text.strip(),end=' ')
        print('')
        print('-' * 60)

#POSTS
POSTS = BLOG.findall('POSTS')
for POSTS_cur in POSTS:
    POST = POSTS_cur.findall('POST')
    for POST_cur in POST:
        if log:
            #INFO
            print('Post number :',POST_cur.find('NUMBER').text.strip())
            print('\tTitle of post :',POST_cur.find('TITLE').text.strip())
            print('\tAt :',POST_cur.find('CREATED_DATE').text.strip())

        #CATEGORIES
        CATEGORY_text = ""
        CATEGORIES = POST_cur.findall('CATEGORIES')
        for CATEGORIES_cur in CATEGORIES:
            CATEGORY = CATEGORIES_cur.findall('CATEGORY')
            for CATEGORY_cur in CATEGORY:
                if log:
                    print('\tCATEGORIE :',CATEGORY_cur.find('NAME').text.strip())
                CATEGORY_text += CATEGORY_cur.find('NAME').text.strip() + ' ' 
        if log:
            print('-' * 60)

        with io.open("./posts/" + POST_cur.find('NUMBER').text.strip() + ".html",'w',encoding='utf8') as file:
            file.write(theme(POST_cur.find('TITLE').text.strip(),POST_cur.find('CONTENT').text,POST_cur.find('CREATED_DATE').text.strip(),CATEGORY_text))

print('Backup files as html are in :',str(files_posts.cwd()))
webbrowser.open_new_tab(str(files_posts.cwd()) + r'/posts')
