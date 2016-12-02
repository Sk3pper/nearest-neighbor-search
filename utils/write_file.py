OUTPUT_DIR = '/Users/andrea/Documents/workspace/nearest-neighbor-search/data/'

def put_into_file(links_recipes, name):
    """ put into the neme file the content of the list


               :param name: file where to put the content
               :param links_recipes:  list of link
               :return: Nothing(void)
    """
    # print len(links_recipes)
    #print '#size {}: {}'.format(name, len(links_recipes))

    # save into the file
    out_file = open(OUTPUT_DIR+name, "w")

    for link in links_recipes:
        # print link
        out_file.write(str(link) + '\n')
    out_file.close()


