from StringIO import StringIO
from Products.CMFCore.utils import getToolByName

from Products.PressRoom.config import PROJECTNAME
from Products.PressRoom.Extensions.utils import restoreKupuSettings, \
                                                restoreTinyMCESettings, \
                                                restorePropertiesSettings, \
                                                restoreViewMethods


def uninstall(portal, reinstall=False):
    """Remove PressRoom cruft"""
    out = StringIO()

    if not reinstall:
        print >> out, "Uninstalling Press Room"
        profile = 'profile-Products.PressRoom:uninstall'
        setup_tool = getToolByName(portal, 'portal_setup')
        setup_tool.runAllImportStepsFromProfile(profile)
        setup_tool.unsetLastVersionForProfile('profile-Products.PressRoom:master')
        setup_tool.unsetLastVersionForProfile('profile-Products.PressRoom:default')
        print >> out, "Ran uninstall profile"
        return out.getvalue()
