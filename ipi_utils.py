
import re
from pathlib import Path

def get_newest_cell_data(p):

    file_dict = {}
    for f in p.iterdir():
        
        #look for 8-character date string\n
        res = re.search("\d{8}",f.name)
        if res is not None:
            file_dict[res[0]] = f.name
    
    try:
        recent_date = max(file_dict.keys())
        return Path(p,file_dict[recent_date])
    except ValueError:
        return None
