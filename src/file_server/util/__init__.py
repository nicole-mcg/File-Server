
#Attributes should be a dict: {"attr_name": "attr_value"}
def createObject(attributes):
    new_object = lambda: None #Used to create an object that we can apply attributes to
    for key in attributes.keys():
        setattr(new_object, key, attributes[key])