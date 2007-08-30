from zope.interface import implements
from Products.Five.browser import BrowserView
from Products.PressRoom.interfaces import IPressRoom
from Products.CMFCore.utils import getToolByName

class PressRoom(BrowserView):
    """Interface for functionality in the PressRoom CT view"""

    implements(IPressRoom)

    def getContacts(self):
        """Return  a list of Press Contacts for this Press Room only if they should be shown
        """
        if not self.context.getShow_contacts():
            return ()
        else:
            path = '/'.join(self.context.getPhysicalPath())
            return self.context.portal_catalog.searchResults(meta_type = 'PressContact',
                                                             review_state='published',
                                                             path=path,
                                                             )
        
    def canAddPressContacts(self):
        """Returns True if the current user has permission to add Press Contacts"""
        membership_tool = getToolByName(self.context, 'portal_membership')
        return membership_tool.checkPermission('Add_Portal_Content', self.context)
        


    def getReleases(self):
        """Return  a list of Press Releases for this Press Room only if they should be shown
        """
        if not self.context.getShow_releases():
            return ()
        else:
            path = '/'.join(self.context.getPhysicalPath())
            return self.context.portal_catalog.searchResults(meta_type = 'PressRelease',
                                                             review_state='published',
                                                             sort_order='reverse',
                                                             path=path,
                                                             sort_on='getReleaseDate',
                                                             )
        
    def canAddPressReleases(self):
        """Returns True if the current user has permission to add Press Releases"""
        membership_tool = getToolByName(self.context, 'portal_membership')
        return membership_tool.checkPermission('Add_Portal_Content', self.context)
    
    
    
    def getClips(self):
        """Return  a list of Press Clips for this Press Room only if they should be shown
        """
        if not self.context.getShow_clips():
            return ()
        else:
            path = '/'.join(self.context.getPhysicalPath())
            return self.context.portal_catalog.searchResults(meta_type = 'PressClip',
                                                             review_state='published',
                                                             sort_order='reverse',
                                                             path=path,
                                                             sort_on='getStorydate',
                                                             )
        
    def canAddPressClips(self):
        """Returns True if the current user has permission to add Press Clips"""
        membership_tool = getToolByName(self.context, 'portal_membership')
        return membership_tool.checkPermission('Add_Portal_Content', self.context)
