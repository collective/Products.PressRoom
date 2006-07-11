from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from Products.CMFCore.CMFCorePermissions import AddPortalContent
try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

PROJECTNAME = "PressRoom"
SKINS_DIR = 'skins'
ADD_CONTENT_PERMISSION = 'PressRoom: Add portal press rooms'
DEFAULT_ADD_CONTENT_PERMISSION = AddPortalContent


#dictionary of addtional types so that permissions can be set separately in the install
ADD_CONTENT_PERMISSIONS = { 'PressContact': DEFAULT_ADD_CONTENT_PERMISSION,
'PressRelease':DEFAULT_ADD_CONTENT_PERMISSION,
}

setDefaultRoles(ADD_CONTENT_PERMISSION, ('Manager'))
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner',))

product_globals=globals()