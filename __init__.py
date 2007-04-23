from Globals import package_home
from Products.CMFCore import utils, CMFCorePermissions, DirectoryView
from Products.CMFPlone.PloneUtilities import ToolInit
from Products.Archetypes.public import *
from Products.Archetypes import listTypes
from Products.Archetypes.utils import capitalize

import os, os.path, sys

# Get configuration data, permissions
from Products.PressRoom.config import *

# Register skin directories so they can be added to portal_skins
DirectoryView.registerDirectory('skins', product_globals)
DirectoryView.registerDirectory('skins/pressroom_content', product_globals)
DirectoryView.registerDirectory('skins/pressroom_scripts', product_globals)
DirectoryView.registerDirectory('skins/pressroom_styles', product_globals)

# message factory code stolen from CMFPlone 2.5
# Import "PressRoomMessageFactory as _" to create message ids in the pressroom domain
# Zope 3.1-style messagefactory module
# BBB: Zope 2.8 / Zope X3.0
try:
    from zope.i18nmessageid import MessageFactory
except ImportError:
    from messagefactory_ import PressRoomMessageFactory
else:
    PressRoomMessageFactory = MessageFactory('pressroom')

def initialize(context):

    # Import the type, which results in registerType() being called
    from content import PressRoom, PressRelease, PressClip, PressContact
    
    # initialize the content, including types and add permissions
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
