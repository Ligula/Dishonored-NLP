from bs4 import BeautifulSoup
from urllib.request import urlopen
import os 

root = "https://dishonored.fandom.com"

def get_data(url_subdirectory, data_type, filter):
    
    url = root + url_subdirectory
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

                    # Creates mission directories
                    if not os.path.exists(os.getcwd()+"/data/missions/" + location_clean_dir):
                        os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/audiographs")
                        os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/books") 
                        os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/notes")  

                    break
            
            # Filters data to the mission in which it is located
            if filter == True:
                with open(os.getcwd()+"/data/missions/" + location_clean_dir + "/" + data_type + "/" + name + ".txt", "a+") as file:
                    file.write(data)
            else:
                with open(os.getcwd()+"/data/" + data_type + "/" + name + ".txt", "a+") as file:
                    file.write(data)

        except:
            print("N/A")
        

# get_data("/wiki/Category:Dishonored_2_Audiographs", "audiograph", True)
get_data("/wiki/Category:Dishonored_2_Books", "books", True)


