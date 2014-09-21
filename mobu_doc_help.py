import pyfbsdk
import webbrowser

def doc_help():
    base_url = 'http://docs.autodesk.com/MB/2015/ENU/MotionBuilder-Developer-Help/index.html#!/url=./py_ref/class_o_r_s_d_k2015_1_1'
    selection = _get_selection()
    
    #Ensure something is selected
    if not selection:
        return False
        
    # Convert the selection to type string for documentation
    type_string = _mobu_to_typestr( selection[0] )
    
    # If type string couldn't be generated, return False
    if not type_string:
        print( help( selection[0] ) )
        return False
    
    # Open the documentation for the class of the selected object
    webbrowser.open( base_url + type_string + ".html" )
    
def _mobu_to_typestr( obj ):
    # Get the passed object's type and convert from type object to a string
    object_type = type(obj)
    object_string = str(object_type)
    
    # Remove the class wrapper from the string
    if object_string.startswith("<class 'pyfbsdk."):
        object_string = object_string[len("<class 'pyfbsdk."):]
        object_string = object_string[:-2]
        
    # If no class wrapper exists return False
    else:
        return False
    
    # Convert class name to url
    string = ""
    for letter in object_string:
        if letter.isupper():
            string = string + "_"
            
        string = string + letter.lower()
        
    return string
    
def _get_selection():
    selection = []
    
    # Check every component in the scene and see if they are selected.
    # As long as that compoenent is not the BaseAnimation node.
    for comp in pyfbsdk.FBSystem().Scene.Components:
        if comp.Name == 'BaseAnimation':
            continue
            
        if comp.Selected == True:
            selection.append(comp)
            
    return selection
    
doc_help()
