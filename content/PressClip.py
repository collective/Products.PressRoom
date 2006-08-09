try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

from Products.ATContentTypes.content.newsitem import ATNewsItem, ATNewsItemSchema, finalizeATCTSchema

from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName
#from AccessControl import ClassSecurityInfo

from Products.Archetypes.Marshall import PrimaryFieldMarshaller
from Products.PressRoom.config import *

schema = ATNewsItemSchema.copy()

# text field not required for clips
schema['text'].required = 0

schema += Schema((
    StringField('reporter',
                required=0,
                searchable=0,
                primary=False,
                languageIndependent=0,
                index="FieldIndex:brains",
                widget=StringWidget(
                        label='Reporter\'s Name',
                        label_msgid = "label_reporter_name",
                        description='Provide the name of the reporter',
                        description_msgid = "help_reporter_name",
                        i18n_domain = "pressroom",),
                ),
    LinesField('publication',
                required=0,
                searchable=0,
                primary=False,
                languageIndependent=0,
                index="FieldIndex:brains",
                widget=KeywordWidget(
                        size=6,
                        label='Name of Publication',
                        label_msgid = "label_publication_name",
                        description='Provide the name of the publication (i.e. name of newspaper, magazine, book, etc.).  Previously used publications can be selected in the left column.  New publications should be added one-per-line in the right column.',
                        description_msgid = "help_publication_name",
                        i18n_domain = "pressroom",),
                ),
    StringField('permalink',
                index="FieldIndex:brains",
                widget=StringWidget(
                        label='URL of Press Clip',
                        label_msgid = "label_pressclip_url",
                        description='Provide the URL to the Press Clip',
                        description_msgid = "help_pressclip_url",
                        i18n_domain = "pressroom",),
                ),
	DateTimeField('storydate',
                index="FieldIndex:brains",
                widget=CalendarWidget(
                        label='Story Date',
                        label_msgid = "label_pressclip_storydate",
                        description='The date the story was originally published',
                        description_msgid = "help_pressclip_storydate",
                        i18n_domain = "pressroom",),
                ),				
    ))

finalizeATCTSchema(schema)

class PressClip(ATNewsItem):
    """For organization's press clips."""
    meta_type = portal_type = 'PressClip'
    archetype_name = 'Press Clip'
    immediate_view = 'pressclip_view'
    default_view   = 'pressclip_view'
    content_icon   = 'pressclip_icon.gif'
    typeDescription = """For organization's press clips."""
    typeDescMsgId  = """Press_clip_description_edit"""
    schema         = schema
    
    _at_rename_after_creation = True
    
    # Get the standard actions (tabs)
    actions = ATNewsItem.actions

    # Make sure we get all the interface declarations from ATDocument,
    # which includes support for ISelectableBrowserDefault to get the
    # 'display' menu to work, IHistoryAware and other standard interfaces.
    __implements__ = ATNewsItem.__implements__

    # enable FTP/WebDAV and friends
    PUT = ATNewsItem.PUT
    
    def getPublication(self):
        """fetch a list of the available publication types from the vocabulary
        """
        f = self.getField('publication')
        result = self.collectKeywords('publication', f.accessor)
        return tuple(result)

registerType(PressClip)
