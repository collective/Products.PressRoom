#
# PloneTestCase
#

# $Id: PloneTestCase.py 8140 2005-10-07 11:24:23Z shh42 $

from Testing import ZopeTestCase

# XXX: Suppress DeprecationWarnings
import warnings
warnings.simplefilter('ignore', DeprecationWarning, append=1)

ZopeTestCase.installProduct('CMFCore')
ZopeTestCase.installProduct('CMFDefault')
ZopeTestCase.installProduct('CMFCalendar')
ZopeTestCase.installProduct('CMFTopic')
ZopeTestCase.installProduct('DCWorkflow')
ZopeTestCase.installProduct('CMFUid', quiet=1)
ZopeTestCase.installProduct('CMFActionIcons')
ZopeTestCase.installProduct('CMFQuickInstallerTool')
ZopeTestCase.installProduct('CMFFormController')
ZopeTestCase.installProduct('ResourceRegistries')
ZopeTestCase.installProduct('GroupUserFolder')
ZopeTestCase.installProduct('ZCTextIndex')
ZopeTestCase.installProduct('ExtendedPathIndex')
ZopeTestCase.installProduct('SecureMailHost')
if ZopeTestCase.hasProduct('ExternalEditor'):
    ZopeTestCase.installProduct('ExternalEditor')
ZopeTestCase.installProduct('CMFPlone')
ZopeTestCase.installProduct('MailHost', quiet=1)
ZopeTestCase.installProduct('PageTemplates', quiet=1)
ZopeTestCase.installProduct('PythonScripts', quiet=1)
ZopeTestCase.installProduct('ExternalMethod', quiet=1)
ZopeTestCase.installProduct('kupu', quiet=1)

# Archetypes/ATContentTypes dependencies
ZopeTestCase.installProduct('Archetypes')
ZopeTestCase.installProduct('MimetypesRegistry', quiet=1)
ZopeTestCase.installProduct('PortalTransforms', quiet=1)
ZopeTestCase.installProduct('ATContentTypes')
ZopeTestCase.installProduct('ATReferenceBrowserWidget')

# These must install cleanly
ZopeTestCase.installProduct('PressRoom')

from Products.PloneTestCase import PloneTestCase

PRODUCTS = ['PressRoom']

PloneTestCase.setupPloneSite(products=PRODUCTS)

class PressRoomTestCase(PloneTestCase.PloneTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
