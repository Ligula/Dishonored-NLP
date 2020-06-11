from bs4 import BeautifulSoup
from urllib.request import urlopen

root = "https://dishonored.fandom.com"

def get_audiographs():
    url = root + "/wiki/Category:Dishonored_2_Audiographs"
    html = urlopen(url) 
    soup = BeautifulSoup(html, 'lxml')

    # Extract directories of audiographs
    directories = []
    audiographs = soup.find_all("div", {"class": "category-page__member-left"})
    for audiograph in audiographs:
        links = audiograph.find_all("a")
        for link in links:
            if ".ogg" not in link['href']:
                directories.append(link['href'])
    
    # Extract audiograph data, including location
    for directory in directories:
        print("\n\n", directory)
        html = urlopen(root+directory)
        soup = BeautifulSoup(html, 'lxml')

        transcript = soup.find("h2", string = "Transcript")
        
        try:
            # paragraphs = transcript.find_all_next()
            for elem in transcript.next_siblings:
                if elem.name == "p":
                    print(elem)
                if elem.name == "h2":
                    break
                    #Get next element and extract location 
        except:
            print("N/A")
        

get_audiographs()
