from zope.interface import Interface

class IPressRoom(Interface):
    """Interface for functionality in the PressRoom CT view"""

    def getContacts():
        """Return a list of Press Contacts for this Press Room only if they should be shown.
        """
    
    def canAddPressContacts():
        """Return True only if current user can add Press Contacts in the current context"""

    def getReleases():
        """Return  a list of Press Releases for this Press Room only if they should be shown
        """

    def canAddPressReleases():
        """Returns True if the current user has permission to add Press Releases"""
    
    def getClips():
        """Return  a list of Press Clips for this Press Room only if they should be shown
        """
        
    def canAddPressClips():
        """Returns True if the current user has permission to add Press Clips"""

    def showTwoStatePrivateWarning():
        """Returns True if we're in Plone 3.0, the press room's supporting folders are private,
           and the current user is someone who can do something about it."""
    
    def publishPressRoomInfrastructure():
        """Publish the 3 content folders (clips, releases, contacts) and the Collections
        that are their home folders"""
    
    