import re

def check_set_promo(set:str,id):
    if re.search("^p", set) and len(set) == 4:
        set = set.upper()
        if re.search("$s", id):
            return f"{set} (Date-stamped Promo)"
        elif re.search("$a",id):
            return f"{set} (Ampersand Promo)"
        else:
            return f"{set} (Planeswalker-stamped Promo)"
    else:
        return f"{set.upper()}"