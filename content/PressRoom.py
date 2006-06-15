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
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.lib.constraintypes import ConstrainTypesMixinSchema
from Products.ATContentTypes.lib.autosort import AutoOrderSupport
from Products.ATContentTypes.content.base import ATCTOrderedFolder
from Products.ATContentTypes.interfaces import IATFolder

# PR
from Products.PressRoom.config import *

ATPressRoomSchema = ATContentTypeSchema.copy() + ConstrainTypesMixinSchema
ATPressRoomSchema += Schema((
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
                        i18n_domain = "plone",)),
    ))

finalizeATCTSchema(ATPressRoomSchema, folderish=True, moveDiscussion=False)

class PressRoom(AutoOrderSupport, ATCTOrderedFolder):
    """A folder where all the press related materials in the site live"""
    schema = ATPressRoomSchema

    content_icon = 'folder_icon.gif'

    archetype_name = 'Press Room'
    meta_type = portal_type = 'PressRoom'
    _at_rename_after_creation = True

    default_view = 'pressroom_view'
    immediate_view = 'pressroom_view'
    suppl_views    = ('pressroom_no_contacts_view',)
    typeDescription= """A folder where all the press related materials in the site live"""
    typeDescMsgId  = 'description_edit_press_room'
    assocMimetypes = ()
    assocFileExt   = ()
    cmf_edit_kws   = ()

    __implements__ = (ATCTOrderedFolder.__implements__, IATFolder,
                     AutoOrderSupport.__implements__)

    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    def initializeArchetype(self, **kwargs):
        """Pre-populate the press room folder with its basic folders.
        """
        BaseFolder.initializeArchetype(self,**kwargs)

        if 'press-releases' not in self.objectIds():
            self.invokeFactory('Folder','press-releases') # XXX Make large plone folder
            obj = self['press-releases']
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

            sort_crit = smart_obj.addCriterion('effective','ATSortCriterion')
            smart_obj.getSortCriterion().setReversed(True)

        if 'press-clips' not in self.objectIds():
            self.invokeFactory('Folder','press-clips') # XXX Make large plone folder
            obj = self['press-clips']
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
            smart_obj.reindexObject()
            
            state_crit = smart_obj.addCriterion('review_state',
                                          'ATSimpleStringCriterion')
            state_crit.setValue('published')
            type_crit = smart_obj.addCriterion('Type',
                                         'ATPortalTypeCriterion')
            type_crit.setValue('Press Clip')
            sort_crit = smart_obj.addCriterion('effective','ATSortCriterion')
            path_crit = smart_obj.addCriterion('path',
                                         'ATPathCriterion')
            path_crit.setValue(self.UID())
            path_crit.setRecurse(True)
            smart_obj.getSortCriterion().setReversed(True)

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
        ATCTOrderedFolder.manage_afterAdd(self, item, container)
        AutoOrderSupport.manage_afterAdd(self, item, container)

    security = ClassSecurityInfo()

registerType(PressRoom, PROJECTNAME)
