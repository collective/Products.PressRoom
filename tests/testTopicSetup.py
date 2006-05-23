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

        self.pressreleases = getattr(self.pressroom, 'press-releases')
        self.allreleases = getattr(self.pressreleases, 'all-press-releases')

        self.pressclips = getattr(self.pressroom, 'press-clips')
        self.allclips = getattr(self.pressclips, 'all-press-clips')

        self.presscontacts = getattr(self.pressroom, 'press-contacts')
        self.contactroster = getattr(self.presscontacts, 'roster')
        
        self.childFolderMapping = {
                                    'press-releases':'all-press-releases',
                                    'press-clips':'all-press-clips',
                                    'press-contacts':'roster',
                                  }

    # test press release smart folders
    def testNumbersOfReleases(self):
        n = 3
        
        # create 3 press releases
        for i in range(3):
            i += 1    
            self.pressreleases.invokeFactory('PressRelease', id="release%s" % i, title="Press Release %s" % i)
    
        self.assertEqual(len(self.pressreleases.objectIds("PressRelease")),n)
        
        # see how many topic results we've got
        self.assertEqual(len(self.allreleases.queryCatalog()),0)
        
        # now publish all releases and test length of topic
        workflow = self.portal.portal_workflow

        for i in range(3):
            i += 1    
            self.releaseObj = getattr(self.pressreleases, "release%s" % i)
            workflow.doActionFor(self.releaseObj,"publish")
        
        self.assertEqual(len(self.allreleases.queryCatalog()),n)

    def testContactRosterCriteria(self):
        # Press Contact topic is in place as default view and has a criterion to show
        # only Press Contacts with the public checkbox set for appearance in roster listing.
        self.assertEqual(self.contactroster._getPortalTypeName(), 'Topic')
        self.assertEqual(self.contactroster.buildQuery()['Type'], ('Press Contact',))
        self.assertEqual(self.contactroster.buildQuery()['review_state'], 'published')
        self.assertEqual(self.contactroster.getSortCriterion().field,'getObjPositionInParent')

    def testAllPressReleasesCriteria(self):
        # Press Contact topic is in place as default view and has a criterion to show
        # only Press Contacts with the public checkbox set for appearance in roster listing.
        self.assertEqual(self.allreleases._getPortalTypeName(), 'Topic')
        self.assertEqual(self.allreleases.buildQuery()['Type'], ('Press Release',))
        self.assertEqual(self.allreleases.buildQuery()['review_state'], 'published')
        self.assertEqual(self.allreleases.getSortCriterion().field,'effective')
        self.assertEqual(self.allreleases.getSortCriterion().getReversed(),True)

    def testAllPressClipCriteria(self):
        # Press Contact topic is in place as default view and has a criterion to show
        # only Press Contacts with the public checkbox set for appearance in roster listing.
        self.assertEqual(self.allclips._getPortalTypeName(), 'Topic')
        self.assertEqual(self.allclips.buildQuery()['Type'], ('Press Clip',))
        self.assertEqual(self.allclips.buildQuery()['review_state'], 'published')
        self.assertEqual(self.allclips.getSortCriterion().field,'effective')
        self.assertEqual(self.allclips.getSortCriterion().getReversed(),True)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPressRoomCreation))
    return suite

if __name__ == '__main__':
    framework()