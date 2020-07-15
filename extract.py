from bs4 import BeautifulSoup
from urllib.request import urlopen
import os 

root = "https://dishonored.fandom.com"

def get_data(url_subdirectory, data_type, filter_by_location):
    
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
        location = soup.find("h2", string = "Location")
        
        try:
            data_dirty = ""
            for elem in transcript.next_siblings:

                # Transcript Data 
                if elem.name == "p":
                    data_dirty += elem.text

                if elem.name == "h2":
                    break
            
            location_dirty = ""
            if filter_by_location == True:
                for elems in location.next_siblings:

                    # Location Data 
                    if elems.name == "p":
                        location_dirty += elems.text
                        
                    if elems.name == "ul":
                        # print("ul")
                        for li in elems:
                            location_dirty += li.text
                        
                        print(location_dirty)
                    
                    if elems.name == "noscript":
                        break
            

            # print(data_dirty)
            
            # For entries that are found in both games, sort info by Dishonored 2 only.
            if "In Dishonored" in location_dirty:
                location_dirty = location_dirty.split("2")[1]

            location_clean = location_dirty.split("mission")[1].split(".")[0].split(",")[0].strip()

            # Fixes entry for audiograph found in both Dishonored 1 & 2
            if location_clean == "Return to the Tower":
                location_clean = "A Long Day in Dunwall"
                print("here")

            # Some entries on Fandom have erroneous hyperlinks, set to unsorted folder for manual sorting.
            elif location_clean == "of the same name":
                location_clean = "Unsorted"

            print(location_clean)

            location_clean_dir = location_clean.translate(str.maketrans({" ":"_", ".":""}))
            if location_clean_dir == "A Long_Day_in_Dunwall":
                location_clean_dir = "A_Long_Day_in_Dunwall"

            # Creates mission directories
            if not os.path.exists(os.getcwd()+"/data/missions/" + location_clean_dir):
                os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/audiographs")
                os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/books") 
                os.makedirs(os.getcwd()+"/data/missions/" + location_clean_dir + "/notes")  

            # Filters data to the mission in which it is located
            if filter_by_location == True:
                with open(os.getcwd()+"/data/missions/" + location_clean_dir + "/" + data_type + "/" + name + ".txt", "a+") as file:
                    file.write(data_dirty)
            else:
                with open(os.getcwd()+"/data/" + data_type + "/" + name + ".txt", "a+") as file:
                    file.write(data_dirty)
        except:
            print("No data found")





        

get_data("/wiki/Category:Dishonored_2_Audiographs", "audiographs", True)
get_data("/wiki/Category:Dishonored_2_Books", "books", True)


