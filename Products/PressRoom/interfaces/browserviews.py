from zope.interface import Interface

class IPressRoom(Interface):
    """Interface for functionality in the PressRoom CT view"""

    def canAddPressContacts():
        """Return True only if current user can add Press Contacts in the current context"""

    def canAddPressReleases():
        """Returns True if the current user has permission to add Press Releases"""

    def canAddPressClips():
        """Returns True if the current user has permission to add Press Clips"""

    def showTwoStatePrivateWarning():
        """Returns True if we're in Plone 3.0, the press room's supporting folders are private,
           and the current user is someone who can do something about it."""

    def publishPressRoomInfrastructure():
        """Publish the 3 content folders (clips, releases, contacts) and the Collections
        that are their home folders"""

class IUpgradeFolders(Interface):
    """This browser view migrates the three main Press Room subfolders to Large Plone Folders.
    
    It's called within the context of a Press Room obj.  It assumes that the subfolders retain
    their original names.  Migration preserves:
    - all content (obviously)
    - 'default page'/'layout' settings
    - addable type constraints
    - folders' Title/descr
    - WF state of folders
    
    Note that calling this browser view might be very resource/time intensive if the
    folders have a lot of content!
    """

    def __call__(self):
        """This class is invoked directly.  See class doc string for details."""
