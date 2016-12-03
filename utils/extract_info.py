import unicodedata

from utils import unicode_ascii_decoder


# title, ingredients, chef, prep_time, cook_time, serves, dietary, methods
# all: ["name", "title", "descr", "prep_time", "cook_time", "serves","dietary", "chef", "show", "ingredients", "methods", "img_url"]
# major: ["title", "ingredients", "chef", "prep_time", "cook_time", "serves","dietary", "methods", "descr"]

# sara: ["ingredients", "chef", "prep_time", "cook_time","serves",  "title","methods", "dietary"]
# come sara ma ordine diverso: ["title", "chef", "prep_time", "cook_time", "serves","dietary", "ingredients","methods"]

def extract_string_recipe(recipe):
    process_order = ["title","ingredients", "chef", "prep_time", "cook_time", "serves", "methods", "dietary", "descr"]
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
                rec = rec + val + '\n'

        elif key == "methods":
            for val in value:
                if val == '':
                    continue
                rec = rec + val + '\n'

        elif key == "title":
            rec = rec + value + '\n'

        elif key == "descr":
            rec = rec + value + '\n'

        elif key == "dietary":
            rec = rec + value+ '\n'

        else:
            rec = rec + value + '\n'

    rec = unicodedata.normalize('NFKD', rec).encode('ASCII', 'ignore')
    # print rec

    return rec
