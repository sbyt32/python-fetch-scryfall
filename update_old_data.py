import csv
import re
import os

def use_regex(input_text):
    text = re.sub("\s(([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?(:([+-]?(?=\.\d|\d)(?:\d+)?(?:\.?\d*))(?:[eE]([+-]?\d+))?)+)", "", input_text)
    return text

for root, dirs, files in os.walk('Tracking'):
    for filename in files:
        old_file = os.path.join(root, filename)




        with open(old_file, newline='') as to_transform:
            read = csv.reader(to_transform, quoting=csv.QUOTE_MINIMAL)

            with open(f'new_{filename}', 'w' , newline='') as fixed_list:
                writer = csv.writer(fixed_list, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(["DATE","USD","USD_FOIL","EURO","EURO_FOIL","TIX"])
                for x in read:
                    if len(x) == 6:
                        x[0] = use_regex(x[0])
                        writer.writerow(x)