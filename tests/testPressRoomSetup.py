#
# Test our Press Room installation
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PressRoom.tests import PressRoomTestCase
from Products.CMFPlone import transaction


class TestInstallation(PressRoomTestCase.PressRoomTestCase):
    """Ensure product is properly installed"""

    def afterSetUp(self):
        self.css        = self.portal.portal_css
        self.kupu       = self.portal.kupu_library_tool
        self.skins      = self.portal.portal_skins
        self.types      = self.portal.portal_types
        self.factory    = self.portal.portal_factory
        self.workflow   = self.portal.portal_workflow
        self.properties = self.portal.portal_properties
        self.atct_tool  = self.portal.portal_atct

        self.metaTypes = ('PressRoom','PressRelease', 'PressClip', 'PressContact')
    
    def testSkinLayersInstalled(self):
        self.failUnless('pressroom_content' in self.skins.objectIds())
        self.failUnless('pressroom_scripts' in self.skins.objectIds())
        self.failUnless('pressroom_styles' in self.skins.objectIds())
        
    def testTypesInstalled(self):
        for t in self.metaTypes:
            self.failUnless(t in self.types.objectIds())

    def testPortalFactorySetup(self):
        for t in self.metaTypes:
            if t != 'PressRoom':
                self.failUnless(t in self.factory.getFactoryTypes())

    def testTypesNotSearched(self):
        types_not_searched = self.properties.site_properties.getProperty('types_not_searched')
        self.failUnless('PressContact' in types_not_searched)

    def testCssInstalled(self):
        self.failUnless('PressRoom.css' in self.css.getResourceIds())
    
    def testDefaultPageType(self):
        default_page_types = self.properties.site_properties.getProperty('default_page_types')
        self.failUnless('PressRelease' in default_page_types)
        self.failUnless('PressClip' in default_page_types)
        
    def testKupuResources(self):
        linkable = self.kupu.getPortalTypesForResourceType('linkable')
        for t in self.metaTypes:
            self.failUnless(t in linkable)

        collection = self.kupu.getPortalTypesForResourceType('collection')
        for t in ('PressRoom',):
            self.failUnless(t in collection)

    def testFolderPositionEnabled(self):
        index = self.atct_tool.getIndex("getObjPositionInParent")
        self.failUnless(index.enabled)

    def testTypeATCTCriterion(self):
        index = self.atct_tool.getIndex("Type")
        self.failUnless("ATListCriterion" in index.criteria)


class TestContentCreation(PressRoomTestCase.PressRoomTestCase):
    """Ensure content types can be created and edited"""

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.folder.invokeFactory('PressRelease', 'pr1')
        self.pr1 = getattr(self.folder, 'pr1')

        self.folder.invokeFactory('PressClip', 'pc1')
        self.pc1 = getattr(self.folder, 'pc1')

        self.folder.invokeFactory('PressContact', 'pcont1')
        self.pcont1 = getattr(self.folder, 'pcont1')

    def testCreatePressRelease(self):
        self.failUnless('pr1' in self.folder.objectIds())

    def testEditPressRelease(self):
        from DateTime import DateTime
        now = DateTime()
        
        self.pr1.setTitle('Big Foot Sighting!')
        self.pr1.setSubhead('Sasquatch Seen Lurking in Local Park')
        self.pr1.setDescription('A description')
        self.pr1.setText('<p>Body text</p>')
        self.pr1.setLocation('SEATTLE, WA')
        self.pr1.setReleaseTiming('FOR IMMEDIATE RELEASE')
        self.pr1.setReleaseDate(now)

        self.assertEqual(self.pr1.Title(), 'Big Foot Sighting!')
        self.assertEqual(self.pr1.getSubhead(), 'Sasquatch Seen Lurking in Local Park')
        self.assertEqual(self.pr1.Description(), 'A description')
        self.assertEqual(self.pr1.getText(), '<p>Body text</p>')
        self.assertEqual(self.pr1.getLocation(), 'SEATTLE, WA')
        self.assertEqual(self.pr1.getReleaseTiming(), 'FOR IMMEDIATE RELEASE')
        self.assertEqual(self.pr1.getReleaseDate(), now)

    def testCreatePressClip(self):
        self.failUnless('pc1' in self.folder.objectIds())

    def testEditPressClip(self):
        self.pc1.setTitle('A Title')
        self.pc1.setDescription('A description')
        self.pc1.setText('<p>Body text</p>')
        self.pc1.setPermalink('http://www.onenw.org')
        self.pc1.setReporter('John Smith')
        self.pc1.setPublication('Seattle Post-Intelligencer')

        self.assertEqual(self.pc1.Title(), 'A Title')
        self.assertEqual(self.pc1.Description(), 'A description')
        self.assertEqual(self.pc1.getText(), '<p>Body text</p>')
        self.assertEqual(self.pc1.getPermalink(), 'http://www.onenw.org')
        self.assertEqual(self.pc1.getReporter(), 'John Smith')
        self.assertEqual(self.pc1.getPublication(), 'Seattle Post-Intelligencer')

    def testCreatePressContact(self):
        self.failUnless('pcont1' in self.folder.objectIds())

    def testEditPressClip(self):
        self.pcont1.setTitle('John Smith')
        self.pcont1.setJobtitle('Plonista')
        self.pcont1.setEmail('john@example.com')
        self.pcont1.setCity('Seattle')
        self.pcont1.setStateOrProvince('WA')
        self.pcont1.setOrganization('Plone Foundation')
        self.pcont1.setPhone('555-555-1234')

        self.assertEqual(self.pcont1.Title(), 'John Smith')
        self.assertEqual(self.pcont1.getJobtitle(), 'Plonista')
        self.assertEqual(self.pcont1.getEmail(), 'john@example.com')
        self.assertEqual(self.pcont1.getCity(), 'Seattle')
        self.assertEqual(self.pcont1.getStateOrProvince(), 'WA')
        self.assertEqual(self.pcont1.getOrganization(), 'Plone Foundation')
        self.assertEqual(self.pcont1.getPhone(), '555-555-1234')

    def testAssociateContactWithRelease(self):
        self.pr1.setReleaseContacts(self.pcont1)

        for contact in self.pr1.getReleaseContacts():
            self.assertEqual(contact, self.pcont1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstallation))
    suite.addTest(makeSuite(TestContentCreation))
    return suite

if __name__ == '__main__':
    framework()