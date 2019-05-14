import requests
import process as process
from bs4 import BeautifulSoup

urls=[
   "training_data/urls/ar_training_urls.txt",
   "training_data/urls/eg_training_urls.txt",
]

contents=[
   "training_data/content/ar_training_content/",
   "training_data/content/eg_training_content/",
]


def extract_content(WebUrl):
    url = WebUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    for script in s(["script", "style", "input", "select"]):
        script.extract()    # rip it out
    return process.normalize(s.get_text(" "))


def read_file(file_name):
    urls = []
    with open(file_name) as f:
        urls = f.read().splitlines()
    f.close()
    return urls

def write_file(folder, file_name, content):
    f = open(folder + file_name, "w")
    f.write(content)
    f.close()


for url_path, content_path in zip(urls, contents):
    print("-----------------------")
    print("Reading Urls list from this file:")
    print(url_path)
    urls = read_file(url_path)
    print(f"{str(len(urls))} Urls found...")
    for url in urls:        
        uarr = url.split(',') #to split line 0:index, 1:url
        if int(uarr[0]) > 0 :            
            print(f"Scrapping, preprocessing and saving content of url index {uarr[0]}")
            try:
                content = extract_content(uarr[1])
                write_file(content_path,uarr[0],content)
            except:
                print("Caught it!")

print("Finished :)")


