import json
 
    
def openTree():
    ''' opens the tree file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the tree file doesn't exist, creates a new empty dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened tree
    '''
    try:
        cache_file = open('savedTree.json', 'r')
        cache_contents = cache_file.read()
        tree = json.loads(cache_contents)
        cache_file.close()
    except:
        tree = {}
    return tree
savedTree = openTree()
printOption = input("Do you want to print the tree? (yes/no): ")
if printOption == "yes":
    print(savedTree)