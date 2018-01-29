from difflib import SequenceMatcher

def string_similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def Add_QuoteWrap(str):
    return '\'' + str + '\''

def QuoteWrap_Dict(my_dict):
    for key, value in my_dict.items():
        if value == True:
            value = 'True'
        if type(value) == str:
            my_dict[key] = Add_QuoteWrap(value)
    return my_dict
