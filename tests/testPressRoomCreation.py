#
# Test Press Room content type initialization
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PressRoom.tests import PressRoomTestCase
from Products.CMFPlone import transaction


if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

class TestPressRoomCreation(PressRoomTestCase.PressRoomTestCase):
    """Ensure content types can be created and edited"""

    def afterSetUp(self):
        self.setRoles(['Manager'])
        self.folder.invokeFactory('PressRoom', id="pressroom", title="Press Room",)
        self.pressroom = getattr(self.folder, 'pressroom')
        
        self.childFolderMapping = {
                                    'press-releases':'all-press-releases',
                                    'press-clips':'all-press-clips',
                                    'press-contacts':'roster',
                                  }

    def testCreatePressRoom(self):
        self.failUnless('pressroom' in self.folder.objectIds())

    def testEditPressRoom(self):
        self.pressroom.setTitle('Media Center')
        self.pressroom.setDescription('Our Media Center')
        self.pressroom.setNum_releases(5)
        self.pressroom.setNum_clips(5)
        self.pressroom.setShow_contacts(True)
        self.pressroom.setText('<p>Here are our latest <strong>press releases and press clips</strong>:</p>')
        
        self.assertEqual(self.pressroom.Title(), 'Media Center')
        self.assertEqual(self.pressroom.Description(), 'Our Media Center')
        self.assertEqual(self.pressroom.getNum_releases(), 5)
        self.assertEqual(self.pressroom.getNum_clips(), 5)
        self.assertEqual(self.pressroom.getShow_contacts(), True)
        self.assertEqual(self.pressroom.getText(), '<p>Here are our latest <strong>press releases and press clips</strong>:</p>')
        self.failUnlessRaises(ValueError, self.pressroom.setNum_clips,"Some text")
        self.failUnlessRaises(ValueError, self.pressroom.setNum_releases,"Some text")

    def testPressRoomChildrenCreated(self):
        for f in self.childFolderMapping.keys():
            self.failUnless(f in self.pressroom.objectIds())

    def testPressContactsTypesContrained(self):
        self.presscontacts = getattr(self.pressroom,'press-contacts')
        self.assertEqual(self.presscontacts.getConstrainTypesMode(), 1)
        self.failUnless("PressContact" in self.presscontacts.getLocallyAllowedTypes())
        self.failUnless("Topic" in self.presscontacts.getLocallyAllowedTypes()) 
        self.failUnless("PressContact" in self.presscontacts.getImmediatelyAddableTypes())

    def testPressClipsTypesContrained(self):
        self.presscontacts = getattr(self.pressroom,'press-clips')
        self.assertEqual(self.presscontacts.getConstrainTypesMode(), 1)
        self.failUnless("PressClip" in self.presscontacts.getLocallyAllowedTypes())
        self.failUnless("Topic" in self.presscontacts.getLocallyAllowedTypes()) 
        self.failUnless("PressClip" in self.presscontacts.getImmediatelyAddableTypes())
    
    def testDefaultPage(self):
        for k,v in self.childFolderMapping.items():
            self.assertEqual(self.pressroom[k].getDefaultPage(), v)

    def testChildrenTopicsCreated(self):
        for k,v in self.childFolderMapping.items():
            self.failUnless(v in self.pressroom[k].objectIds())
            
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPressRoomCreation))
    return suite

if __name__ == '__main__':
    framework()