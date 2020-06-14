from bs4 import BeautifulSoup
from urllib.request import urlopen
import os 

root = "https://dishonored.fandom.com"

def get_audiographs():
    
    url = root + "/wiki/Category:Dishonored_2_Audiographs"
    html = urlopen(url) 
    soup = BeautifulSoup(html, 'lxml')

    # Extract directories of audiographs
    directories = []
 
    for li in soup.find_all("li", {"class" : "category-page__member"}):
        if ".ogg" not in li.a['href']:
            directories.append(li.a['href'])

    # Extract audiograph data, including location
    print(directories)
    for directory in directories:
        print("\n\n", directory)
        name = directory.split("/")[2]

        html = urlopen(root+directory)
        soup = BeautifulSoup(html, 'lxml')

        transcript = soup.find("h2", string = "Transcript")
        
        try:
            data = ""
            for elem in transcript.next_siblings:
                if elem.name == "p":
                    data += elem.text

                # Need to fix location scrape
                if elem.name == "h2":
                    location_data = elem.next_sibling.next_sibling.text
                    location_dirty = location_data.split("mission")

                    location_clean = location_dirty[-1].translate(str.maketrans({" ":"_", ".":""}))
                    location_clean = location_clean[1:].strip()
                    print(location_clean)
    
                    if not os.path.exists(os.getcwd()+"\data\missions/" + location_clean):
                        os.makedirs(os.getcwd()+"\data\missions/" + location_clean)
                        
                        print("sicc")

                    break
            
            with open(os.getcwd()+"\data\missions/" + location_clean + "/" + name + ".txt", "a+") as audiog_file:
                audiog_file.write(data)

        except:
            print("N/A")
        

get_audiographs()

