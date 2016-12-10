import unicodedata

def extract_string_recipe(recipe):
    process_order = ["title", "ingredients", "chef", "prep_time", "cook_time", "serves", "methods", "dietary", "descr"]
    rec = ''

    for key in process_order:
        # print 'key : '+key
        value = recipe[key]

        if value == "":
            continue
        elif key == "ingredients":
            for val in value:
                if val == '':
                    continue
                val = unicodedata.normalize('NFKD', val).encode('ASCII', 'ignore')
                val = val.replace("\n", '')
                rec = rec + val
            rec = rec + '\n'

        elif key == "methods":
            for val in value:
                if val == '':
                    continue
                val = unicodedata.normalize('NFKD', val).encode('ASCII', 'ignore')
                val = val.replace("\n", '')
                rec = rec + val
            rec = rec + '\n'

        elif key == "title":
            value = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore')
            value = value.replace("\n", '')
            rec = rec + value + '\n'

        elif key == "descr":
            value = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore')
            value = value.replace("\n", '')
            rec = rec + value + '\n'

        elif key == "dietary":
            value = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore')
            value = value.replace("\n", '')
            rec = rec + value + '\n'

        else:
            value = unicodedata.normalize('NFKD', value).encode('ASCII', 'ignore')
            value = value.replace("\n", '')
            rec = rec + value + '\n'

    # rec = unicodedata.normalize('NFKD', rec).encode('ASCII', 'ignore')

    return rec
