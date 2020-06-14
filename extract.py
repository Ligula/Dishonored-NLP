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

                # Transcript Data 
                if elem.name == "p":
                    data += elem.text

                # Location Data 
                if elem.name == "h2":
                    location_dirty = elem.next_sibling.next_sibling.text
                    location_clean = location_dirty.split("mission")[1].split(".")[0].split(",")[0].strip()

                    # Fixes entry for audiograph found in both Dishonored 1 & 2
                    if location_clean == "Return to the Tower":
                        location_clean = "A Long Day in Dunwall"

                    location_clean_dir = location_clean.translate(str.maketrans({" ":"_", ".":""}))
    
                    if not os.path.exists(os.getcwd()+"/data/missions/" + location_clean_dir):
                        os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/audiographs")

                    break
            
            with open(os.getcwd()+"/data/missions/" + location_clean_dir + "/audiographs/" + name + ".txt", "a+") as audiog_file:
                audiog_file.write(data)

        except:
            print("N/A")
        

get_audiographs()

