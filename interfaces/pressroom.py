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
