import json
from json.decoder import JSONDecoder
import re
import datetime
from psycopg2.extras import Json



def TextSanitize(text):
    text_sanitized = str(text)

    if text_sanitized != 'None':
        text_sanitized = text_sanitized.replace("\'","\"")
        text_sanitized = text_sanitized.replace("\,"," ")
    
    return text_sanitized

def json_field(text):
    
    jsrow = str(text)
    jsrow = TextSanitize(jsrow)

    if jsrow != 'None' or jsrow != 'null':
        jsrow = jsrow.replace("\'","\"")
        jsrow = jsrow.replace("None","\"None\"")
        jsrow = jsrow.replace("False","\"False\"")
        jsrow = jsrow.replace("True","\"False\"")
    
    else:
        jsrow = json.dumps(None)
    return jsrow

def clearCatID(StringToClear):
    _clearCatID = str(StringToClear)
    _clearCatID = re.sub(r"\('", '', _clearCatID)
    _clearCatID = re.sub(r"\',", '', _clearCatID)
    _clearCatID = re.sub(r"\)", '', _clearCatID)
    return _clearCatID

def toNumb(txt):
    numb = txt
    if numb == None:
        numb = 0
    
    return numb
