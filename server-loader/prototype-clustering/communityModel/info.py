# Current executed file
https://www.geeksforgeeks.org/how-to-get-directory-of-current-script-in-python/
https://stackoverflow.com/questions/2632199/how-do-i-get-the-path-of-the-current-executed-file-in-python

https://stackoverflow.com/questions/1296501/find-path-to-currently-running-file

# adding relative to absolute path
https://stackoverflow.com/questions/52878999/adding-a-relative-path-to-an-absolute-path-in-python


"""
        abspath = os.path.dirname(__file__)
        relpath = "/../../communityModel/data/GAM_Catalogue_plus.json"
        route = os.path.normpath(os.path.join(abspath, relpath))
        
                
        
        print("interactionObject file route")
        print(route)
        
        """