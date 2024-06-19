from graphql_relay.node.node import from_global_id
import re
from os.path import exists
import random

keys_names = ['id']
# Email check
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def input_to_dictionary(input):
    """Method to convert Graphene inputs into dictionary."""
    print("input: ", input)
    dictionary = input
    for key in input:
        # Convert GraphQL global id to models id
        if key in keys_names:
            if input[key] is not None:
                dictionary[key] = (from_global_id(input[key]).id)

    print("dictionary:", dictionary)
    return dictionary


def check_email(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

def remove_symbols_white_to_lower(text:str) -> str:
    symbols = "`''' `,~,!,¡,@,#,$,%,^,&,*,(,),,=,{,[,},},|,:,;,,',<,,,>,.,?,/"
    text = text.translate(str.maketrans('', '', symbols))
    text = text.replace(" ", "")
    text = text.lower()
    text = text.strip()    
    return text

def limit_text(text:str, limit:int) -> str:
    if len(text) > limit:
        text = text[:limit]
    return text
 
 
def random_int_k(k:int =3):
    mapchapters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    result = random.choices(mapchapters, k=k)
    code = ""
    for i in result:
        code += str(i)
    code = code
    return code


def random_varchar_k(k:int =3):
    mapchapters = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9","a", "b", "c", "d", "g", "h", "i", "p", "j", "n"]
    result = random.choices(mapchapters, k=k)
    code = ""
    for i in result:
        code += str(i)
    code = code
    return code