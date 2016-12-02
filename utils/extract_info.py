from utils import unicode_ascii_decoder


def extract_string_recipe(recipe):
    process_order = ["name", "title", "descr", "prep_time", "cook_time", "serves",
                     "dietary", "chef", "show", "ingredients", "methods", "img_url"]
    rec = ''

    for key in process_order:
        #print 'key : '+key
        value = recipe[key]

        if value == "":
            continue
        elif key == "name":
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '
        elif key == "img_url":
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '
        elif key == "ingredients":
            i = 0
            for val in value:
                if val == '':
                    continue
                rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(val)) + ' '

            #print len(value)

        elif key == "methods":
            for val in value:
                if val == '':
                    continue
                rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(val)) + ' '


        elif key == "title":
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '

        elif key == "descr":
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '

        elif key == "dietary" and value == "Vegetarian":
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '

        else:
            rec = rec + str(unicode_ascii_decoder.unicode_to_ascii(value)) + ' '

    return rec