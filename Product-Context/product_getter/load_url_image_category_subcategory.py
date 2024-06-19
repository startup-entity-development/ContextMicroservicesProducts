from typing import Dict


def get_dict_image_subcategory_from_csv(self) -> Dict[str, str]:
    dict_subcategory_image:Dict[str, str] = {}  
    f = open("subcategory_name_image.csv", "r")
    for line in f:
        image, name = line.split("|")
        #avoid first line with headers
        if name == "name":
            continue
        #remove \n from name
        name = name.replace("\n", "")
        dict_subcategory_image[name] = image
    f.close()
    return dict_subcategory_image

def get_image_from_dict_subcategory(self, name_subcategory:str, dict_subcategory_image:Dict[str, str]) -> str:        
    return dict_subcategory_image.get(name_subcategory)