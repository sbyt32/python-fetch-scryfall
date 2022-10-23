def parse_list(list):
    list_qty = list['total_cards']
    if list_qty == 1:
        pass # This needs to go and fetch a specific card and ask you which set you want it from.
             # ? Maybe go do this in another script?
    elif list_qty > 1:
        pass # Use pick to maybe run a script that gives out a list of cards?
    else:
        pass # ! Error, in case that it gives me something that has ZERO cards (idk if possible)
             # ? Would this not give a 400 error, if the case?