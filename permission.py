"""
"""
__author__  = 'Andrew Burkhalter <andrewb AT onenw DOT org>'
__docformat__ = 'restructuredtext'

from Products.CMFCore.permissions import setDefaultRoles

PRESS_ROOM_ROLES = ('Manager',)

# Gathering PressRoom into one place
AddPressRooms = 'PressRoom: Add portal press rooms'
setDefaultRoles(AddPressRooms, PRESS_ROOM_ROLES)