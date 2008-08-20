from Products.ATContentTypes.interfaces import IATNewsItem

# This is a marker interface. By having PressRelease declare that it implements
# IPressRelease, we are asserting that it also supports IATNewsItem and 
# everything that interface declares

class IPressRelease(IATNewsItem):
    """Press release marker interface
    """
    
    pass