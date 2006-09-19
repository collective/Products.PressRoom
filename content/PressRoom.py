#
# The Press Room container.
#
# A Press Room is pre-populated with the following folders:
#
# /press-contacts
# /press-clips
# /press-releases
#
# The main goals of these folders are to restrict the addable types and
# provide a sensible default view out-of-the-box, like the FAQ view.
#

# CMF/ZOPE
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Globals import package_home

# AT
try:
 from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
 from Products.Archetypes.public import *

# ATCT
from Products.ATContentTypes.content.folder import ATFolderSchema, ATFolder
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.interfaces import IATFolder

# PR
from Products.PressRoom.config import *

ATPressRoomSchema = ATFolderSchema.copy()
ATPressRoomSchema += Schema((
    BooleanField('show_releases',
            required=0,
            default=True,
            widget = BooleanWidget(
                        label = "Display Releases?",
                        label_msgid = "label_show_releases",
                        description = "If this is checked, your published releases will appear.",
                        description_msgid = "help_show_release",
                        i18n_domain = "pressroom",),
            ),
                
    IntegerField('num_releases',
            required=0,
            default=4,
            widget = IntegerWidget(
                        label = "Number of press releases",
                        label_msgid = "label_num_releases",
                        description = "What is the maximum number of press releases that should appear in the press room default view?",
                        description_msgid = "help_num_releases",
                        i18n_domain = "pressroom",),
            ),
            
    BooleanField('show_clips',
            required=0,
            default=True,
            widget = BooleanWidget(
                        label = "Display clips?",
                        label_msgid = "label_show_clips",
                        description = "If this is checked, your published clips will appear.",
                        description_msgid = "help_show_clips",
                        i18n_domain = "pressroom",),
            ),

    IntegerField('num_clips',
            required=0,
            default=4,
            widget = IntegerWidget(
                        label = "Number of press clips",
                        label_msgid = "label_num_clips",
                        description = "What is the maximum number of press clips that should appear in the press room default view?",
                        description_msgid = "help_num_clips",
                        i18n_domain = "pressroom",),
            ),

    BooleanField('show_contacts',
            required=0,
            default=True,
            widget = BooleanWidget(
                        label = "Display contacts?",
                        label_msgid = "label_show_contacts",
                        description = "If this is checked, your published contacts will appear.",
                        description_msgid = "help_show_contacts",
                        i18n_domain = "pressroom",),
            ),
    
    TextField('text',
            required=0,
            primary=1,
            searchable=1,
            default_output_type='text/x-html-safe',
            allowable_content_types=('text/restructured',
                                     'text/plain',
                                     'text/html'),
            widget = RichWidget(
                        description = "",
                        description_msgid = "help_body_text",
                        label = "Body Text",
                        label_msgid = "label_body_text",
                        rows = 25,
                        i18n_domain = "pressroom",)
            ),
    ))

finalizeATCTSchema(ATPressRoomSchema, folderish=True, moveDiscussion=False)

class PressRoom(ATFolder):
    """A folder where all the press related materials in the site live"""
    schema = ATPressRoomSchema

    content_icon = 'pressroom_icon.gif'

    archetype_name = 'Press Room'
    meta_type = portal_type = 'PressRoom'
    _at_rename_after_creation = True
    default_view = 'pressroom_view'
    immediate_view = 'pressroom_view'
    typeDescription= """A folder where all the press related materials in the site live"""
    typeDescMsgId  = 'description_edit_press_room'
    assocMimetypes = ()
    assocFileExt   = ()
    cmf_edit_kws   = ()
    
    allowed_content_types = ['Document', 'File', 'Folder', 'Image', 'Large Plone Folder', 'Link', 'Topic',]

    __implements__ = (IATFolder,)

    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    def initializeArchetype(self, **kwargs):
        """Pre-populate the press room folder with its basic folders.
        """
        ATFolder.initializeArchetype(self,**kwargs)

        if 'press-releases' not in self.objectIds():
            self.invokeFactory('Folder','press-releases') # XXX Make large plone folder
            obj = self['press-releases']
            obj.setConstrainTypesMode(1)
            obj.setImmediatelyAddableTypes(["PressRelease",])
            obj.setLocallyAllowedTypes(["Topic","PressRelease",])
            
            obj.setTitle(self.translate(
                    msgid='pr_press_releases_title',
                    domain='pressroom',
                    default='Press Releases'))
            obj.setDescription(self.translate(
                    msgid='pr_press_releases_description',
                    domain='pressroom',
                    default='These are our press releases'))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory('Topic','all-press-releases')
            obj.setDefaultPage('all-press-releases')
            
            smart_obj = obj['all-press-releases']
            smart_obj.setTitle(self.translate(
                    msgid='pr_press_releases_title',
                    domain='pressroom',
                    default='Press Releases'))
            smart_obj.setDescription(self.translate(
                    msgid='pr_press_releases_description',
                    domain='pressroom',
                    default='These are our press releases'))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()
            
            state_crit = smart_obj.addCriterion('review_state',
                                          'ATSimpleStringCriterion')
            state_crit.setValue('published')

            type_crit = smart_obj.addCriterion('Type',
                                         'ATPortalTypeCriterion')
            type_crit.setValue('Press Release')

            path_crit = smart_obj.addCriterion('path',
                                         'ATPathCriterion')
            path_crit.setValue(self.UID())
            path_crit.setRecurse(True)

            sort_crit = smart_obj.addCriterion('getReleaseDate','ATSortCriterion')
            smart_obj.getSortCriterion().setReversed(True)

            # Update Smart Folder settings  
            smart_folder_tool = getToolByName(self, 'portal_atct') 
            if 'getReleaseDate' not in smart_folder_tool.getIndexes(enabledOnly=True):     
             smart_folder_tool.addIndex("getReleaseDate", "Release Date", "The date of the press release", enabled=True) 
            elif 'getReleaseDate' not in smart_folder_tool.getIndexes():
             # index exists, but is disabled 
             smart_folder_tool.updateIndex('getReleaseDate', enabled=True)
            if 'getReleaseDate' not in smart_folder_tool.getAllMetadata(enabledOnly=True):
             smart_folder_tool.addMetadata("getReleaseDate", "Release Date", "The date of the press release", enabled=True)
            elif 'getReleaseDate' not in smart_folder_tool.getAllMetadata():     
             # metadata exist, but are disabled     
             smart_folder_tool.updateMetadata('getReleaseDate', enabled=True) 

        if 'press-clips' not in self.objectIds():
            self.invokeFactory('Folder','press-clips') # XXX Make large plone folder
            obj = self['press-clips']
            obj.setConstrainTypesMode(1)
            obj.setImmediatelyAddableTypes(["PressClip",])
            obj.setLocallyAllowedTypes(["Topic","PressClip",])

            obj.setTitle(self.translate(
                    msgid='pr_press_clip_title',
                    domain='pressroom',
                    default='Press Clips'))
            obj.setDescription(self.translate(
                    msgid='pr_press_clip_description',
                    domain='pressroom',
                    default='See us in the news!'))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory('Topic','all-press-clips')
            obj.setDefaultPage('all-press-clips')

            smart_obj = obj['all-press-clips']
            smart_obj.setTitle(self.translate(
                    msgid='pr_press_clips_title',
                    domain='pressroom',
                    default='Press Clips'))
            smart_obj.setDescription(self.translate(
                    msgid='pr_press_clips_description',
                    domain='pressroom',
                    default='See us in the news!'))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()
            
            state_crit = smart_obj.addCriterion('review_state',
                                          'ATSimpleStringCriterion')
            state_crit.setValue('published')
            type_crit = smart_obj.addCriterion('Type',
                                         'ATPortalTypeCriterion')
            type_crit.setValue('Press Clip')
            sort_crit = smart_obj.addCriterion('getStorydate','ATSortCriterion')
            path_crit = smart_obj.addCriterion('path',
                                         'ATPathCriterion')
            path_crit.setValue(self.UID())
            path_crit.setRecurse(True)
            smart_obj.getSortCriterion().setReversed(True)

            # Update Smart Folder settings  
            if 'getStorydate' not in smart_folder_tool.getIndexes(enabledOnly=True):     
             smart_folder_tool.addIndex("getStorydate", "Story Date", "The date of the press clip", enabled=True) 
            elif 'getStorydate' not in smart_folder_tool.getIndexes():
             # index exists, but is disabled 
             smart_folder_tool.updateIndex('getStorydate', enabled=True)
            if 'getStorydate' not in smart_folder_tool.getAllMetadata(enabledOnly=True):
             smart_folder_tool.addMetadata("getStorydate", "Release Date", "The date of the press clip", enabled=True)
            elif 'getStorydate' not in smart_folder_tool.getAllMetadata(): 
             # metadata exist, but are disabled     
             smart_folder_tool.updateMetadata('getStorydate', enabled=True)     



        if 'press-contacts' not in self.objectIds():
            self.invokeFactory('Folder','press-contacts')
            obj = self['press-contacts']
            obj.setConstrainTypesMode(1)
            obj.setImmediatelyAddableTypes(["PressContact",])
            obj.setLocallyAllowedTypes(["Topic","PressContact",])
            obj.setTitle(self.translate(
                    msgid='pr_press_contacts_title',
                    domain='pressroom',
                    default='Press Contacts'))
            obj.setDescription(self.translate(
                    msgid='pr_press_contacts_description',
                    domain='pressroom',
                    default='Contact these people for more information'))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory('Topic','roster')
            obj.setDefaultPage('roster')

            smart_obj = obj['roster']
            smart_obj.setTitle(self.translate(
                    msgid='pr_press_contacts_title',
                    domain='pressroom',
                    default='Press Contacts'))
            smart_obj.setDescription(self.translate(
                    msgid='pr_press_contacts_description',
                    domain='pressroom',
                    default='Contact these people for more information'))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()

            # set the criteria published, type, public, and ordering
            state_crit = smart_obj.addCriterion('review_state',
                                          'ATSimpleStringCriterion')
            state_crit.setValue('published')
            type_crit = smart_obj.addCriterion('Type',
                                         'ATPortalTypeCriterion')
            type_crit.setValue('Press Contact')
            path_crit = smart_obj.addCriterion('path',
                                         'ATPathCriterion')
            path_crit.setValue(self.UID())
            path_crit.setRecurse(True)
            sort_crit = smart_obj.addCriterion('getObjPositionInParent','ATSortCriterion')
            
        get_transaction().commit(1)

    def manage_afterAdd(self, item, container):
        ATFolder.manage_afterAdd(self, item, container)
        ATFolder.manage_afterAdd(self, item, container)

    security = ClassSecurityInfo()

registerType(PressRoom)
