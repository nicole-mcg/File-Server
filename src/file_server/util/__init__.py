
#Attributes should be a dict: {"attr_name": "attr_value"}
def create_object(attributes):
    new_object = lambda: None #Used to create an object that we can apply attributes to
    for key in attributes.keys():
        setattr(new_object, key, attributes[key])
    return new_object