#
# The Press Room container.
#
# A Press Room is pre-populated with the following Large Plone Folders:
#
# /press-contacts
# /press-clips
# /press-releases
#
# The main goals of these folders are to restrict the addable types and
# provide a sensible default view out-of-the-box, like the FAQ view.
#

import transaction

# CMF/ZOPE
from zope.interface import implements, Interface
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base

# AT
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

try:
    from Products.Archetypes.atapi import TinyMCEWidget
    RichTextWidget = TinyMCEWidget
except ImportError:
    RichTextWidget = RichWidget

# ATCT
from Products.ATContentTypes.content.folder import ATFolderSchema, ATFolder
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

# Plone
from Products.CMFPlone.i18nl10n import utranslate
try:
    from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
except:
    ISelectableConstrainTypes = Interface
# PR
from Products.PressRoom import HAS_PLONE40
from Products.PressRoom.config import *
from Products.PressRoom.interfaces.content import IPressRoom

try:
    from plone.app.contenttypes.behaviors import collection
    coll_type = 'Collection'
except ImportError:
    coll_type = 'Topic'


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
        widget = RichTextWidget(
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
    _at_rename_after_creation = True
    typeDescription= """A folder where all the press related materials in the site live"""
    typeDescMsgId  = 'description_edit_press_room'
    assocMimetypes = ()
    assocFileExt   = ()
    cmf_edit_kws   = ()

    implements(IPressRoom)


    # Enable marshalling via WebDAV/FTP/ExternalEditor.
    __dav_marshall__ = True

    def initializeArchetype(self, **kwargs):
        """Pre-populate the press room folder with its basic folders.
        """
        ATFolder.initializeArchetype(self,**kwargs)
        
        # create sub-folders
        self._createSubFolders()

    def _createSubFolders(self, use_large_folders=True):
        """We're splitting this out and giving the optional arg just
        to facilitate testing."""

        folder_type = "Folder"
        if HAS_PLONE40:
            use_large_folders = False
        elif use_large_folders:
            folder_type = "Large Plone Folder"
            # enable the addition of LPFs momentarily
            large_folders_addable = True
            portal_types = getToolByName(self, "portal_types")
            lpf = getattr(portal_types, folder_type)
            if not lpf.global_allow:
                large_folders_addable = False
                lpf.manage_changeProperties(global_allow = True)

        if 'press-releases' not in self.objectIds():
            self.invokeFactory(folder_type, 'press-releases')
            obj = self['press-releases']
            aspect = ISelectableConstrainTypes(obj, alternate=obj)
            if getattr(aq_base(aspect), 'canSetConstrainTypes', None):
                aspect.setConstrainTypesMode(1)
                aspect.setImmediatelyAddableTypes(["PressRelease",])
                aspect.setLocallyAllowedTypes([coll_type, "PressRelease",])

            obj.setTitle(utranslate('pressroom', 'Press Releases', context=self))
            obj.setDescription(utranslate('pressroom', 'These are our press releases', context=self))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory(coll_type, 'all-press-releases')
            obj.setDefaultPage('all-press-releases')

            smart_obj = obj['all-press-releases']
            smart_obj.setTitle(utranslate('pressroom', u'Press Releases', context=self))
            smart_obj.setDescription(utranslate('pressroom', u'These are our press releases', context=self))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()

            if coll_type == 'Topic':
                state_crit = smart_obj.addCriterion('review_state',
                                                    'ATSimpleStringCriterion')
                state_crit.setValue('published')
                type_crit = smart_obj.addCriterion('Type',
                                                   'ATPortalTypeCriterion')
                type_crit.setValue('Press Clip')
                smart_obj.addCriterion('getStorydate','ATSortCriterion')
                path_crit = smart_obj.addCriterion('path',
                                                   'ATPathCriterion')
                path_crit.setValue(self.UID())
                path_crit.setRecurse(True)
                smart_obj.getSortCriterion().setReversed(True)
            else:
                smart_obj.sort_on = u'getReleaseDate'
                smart_obj.sort_reversed = True
                #: Query by Type and Review State
                smart_obj.query = [
                    {'i': u'portal_type',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'PressRelease'],
                     },
                    {'i': u'review_state',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'published'],
                     },
                    {'i': u'path',
                     'o': u'plone.app.querystring.operation.string.relativePath',
                     'v': '..::-1',
                     },
                ]

        if 'press-clips' not in self.objectIds():
            self.invokeFactory(folder_type, 'press-clips')
            obj = self['press-clips']
            aspect = ISelectableConstrainTypes(obj, alternate=obj)
            if getattr(aq_base(aspect), 'canSetConstrainTypes', None):
                aspect.setConstrainTypesMode(1)
                aspect.setImmediatelyAddableTypes(["PressClip",])
                aspect.setLocallyAllowedTypes([coll_type, "PressClip",])

            obj.setTitle(utranslate('pressroom', u'Press Clips', context=self))
            obj.setDescription(utranslate('pressroom', u'See us in the news!', context=self))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory(coll_type, 'all-press-clips')
            obj.setDefaultPage('all-press-clips')

            smart_obj = obj['all-press-clips']
            smart_obj.setTitle(utranslate('pressroom', u'Press Clips', context=self))
            smart_obj.setDescription(utranslate('pressroom', u'See us in the news!', context=self))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()

            if coll_type == 'Topic':
                state_crit = smart_obj.addCriterion('review_state',
                                                    'ATSimpleStringCriterion')
                state_crit.setValue('published')
                type_crit = smart_obj.addCriterion('Type',
                                                   'ATPortalTypeCriterion')
                type_crit.setValue('Press Clip')
                smart_obj.addCriterion('getStorydate','ATSortCriterion')
                path_crit = smart_obj.addCriterion('path',
                                                   'ATPathCriterion')
                path_crit.setValue(self.UID())
                path_crit.setRecurse(True)
                smart_obj.getSortCriterion().setReversed(True)
            else:
                smart_obj.sort_on = u'getStorydate'
                smart_obj.sort_reversed = True
                #: Query by Type and Review State
                smart_obj.query = [
                    {'i': u'portal_type',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'PressClip'],
                     },
                    {'i': u'review_state',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'published'],
                     },
                    {'i': u'path',
                     'o': u'plone.app.querystring.operation.string.relativePath',
                     'v': '..::-1',
                     },
                ]


        if 'press-contacts' not in self.objectIds():
            self.invokeFactory("Folder", 'press-contacts')
            obj = self['press-contacts']
            aspect = ISelectableConstrainTypes(obj, alternate=obj)
            if getattr(aq_base(aspect), 'canSetConstrainTypes', None):
                aspect.setConstrainTypesMode(1)
                aspect.setImmediatelyAddableTypes(["PressContact",])
                aspect.setLocallyAllowedTypes([coll_type, "PressContact",])

            obj.setTitle(utranslate('pressroom', u'Press Contacts', context=self))
            obj.setDescription(utranslate('pressroom', u'Contact these people for more information', context=self))
            obj.reindexObject()

            # create Smart Folder to be this folder's default page
            obj.invokeFactory(coll_type, 'press-contacts')
            obj.setDefaultPage('press-contacts')

            smart_obj = obj['press-contacts']
            smart_obj.setTitle(utranslate('pressroom', u'Press Contacts', context=self))
            smart_obj.setDescription(utranslate('pressroom', u'Contact these people for more information', context=self))
            smart_obj.setLayout('folder_listing_pressroom')
            smart_obj.reindexObject()

            if coll_type == 'Topic':
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
                smart_obj.addCriterion('getObjPositionInParent','ATSortCriterion')
            else:
                smart_obj.sort_on = u'getObjPositionInParent'
                smart_obj.sort_reversed = False
                #: Query by Type and Review State
                smart_obj.query = [
                    {'i': u'portal_type',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'PressContact'],
                     },
                    {'i': u'review_state',
                     'o': u'plone.app.querystring.operation.selection.any',
                     'v': [u'published'],
                     },
                    {'i': u'path',
                     'o': u'plone.app.querystring.operation.string.relativePath',
                     'v': '..::-1',
                     },
                ]

        if use_large_folders and not large_folders_addable:
            lpf.manage_changeProperties(global_allow = False)

        transaction.savepoint()

    def manage_afterAdd(self, item, container):
        ATFolder.manage_afterAdd(self, item, container)

    security = ClassSecurityInfo()

registerType(PressRoom, PROJECTNAME)
