"""A document type for press releases"""

__author__  = ''
__docformat__ = 'plaintext'

# Core
from AccessControl import ClassSecurityInfo
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.utils import getToolByName

#Arch
try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

from Products.Archetypes.Marshall import PrimaryFieldMarshaller

# ATCT
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.content.newsitem import ATNewsItemSchema
from Products.ATContentTypes.content.newsitem import finalizeATCTSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget

# PC
from Products.PressRoom.config import *

#qi = getToolByName("portal_quickinstaller")


# Schema declaration
schema = ATNewsItemSchema.copy()

schema = schema + Schema((

    StringField('subhead',
                required=0,
                primary=False,
                languageIndependent=1,
                index="FieldIndex:brains",
                searchable=1,
                widget=StringWidget(
                    label='Subheadline',
                    label_msgid = "label_subheadline",
                    description='Please provide a subheadline for your press release',
                    description_msgid = "help_subheadline",
                    i18n_domain = "pressroom",),
                ),
    StringField('location',
                required=0,
                searchable=0,
                primary=False,
                languageIndependent=0,
                index="FieldIndex:brains",
                widget=StringWidget(
                    label='Press release location',
                    label_msgid = "label_location",
                    description='Typically press releases have an associated location in a common format (i.e. <City>, <State>)',
                    description_msgid = "help_location",
                    i18n_domain = "pressroom",),
                ),
    ReferenceField('releaseContacts',
            relationship = 'releaseContacts',
            multiValued = True,
            isMetadata = True,
            allowed_types=('PressContact',),
            languageIndependent = False,
            index = 'KeywordIndex',
            write_permission = ModifyPortalContent,
            widget = ReferenceBrowserWidget(
                        allow_search = True,
                        allow_browse = True,
                        show_indexes = False,
                        force_close_on_insert = True,
                        label = "Release Contact(s)",
                        label_msgid = "label_release_contacts",
                        description = "",
                        description_msgid = "help_release_contacts",
                        i18n_domain = "plone",
                        visible = {'edit' : 'visible', 'view' : 'visible' }
                )
            )
    ),)

schema.moveField('subhead', after='title')
schema.moveField('location', after='subhead')
finalizeATCTSchema(schema)

class PressRelease(ATNewsItem):
    """For an organization's original press release documents."""
    
    meta_type = portal_type = 'PressRelease'
    archetype_name  = 'Press Release'
    immediate_view  = 'pressrelease_view'
    default_view    = 'pressrelease_view'
    content_icon    = 'newsitem_icon.gif'
    typeDescription = """For an organization's original press release documents"""
    typeDescMsgId   = """Press_release_description_edit"""
    schema          = schema
    
    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True
    
    # Get the standard actions (tabs)
    actions = ATNewsItem.actions

    # Make sure we get all the interface declarations from ATNewsItem,
    # which includes support for ISelectableBrowserDefault to get the
    # 'display' menu to work, IHistoryAware and other standard interfaces.
    __implements__ = ATNewsItem.__implements__

    # enable FTP/WebDAV and friends
    PUT = ATNewsItem.PUT

registerType(PressRelease, PROJECTNAME)