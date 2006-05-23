PressRoom

    PressRoom is a simple add-on product which can be used to easily manage an online
    Press Room within your Plone site.  It adds 3 new content types to your Plone site 
    including a Press Release, a Press Clip (i.e. a reference to your organization in the news), 
    and Press Contact, which is a person within or outside of your organization that has been 
    deemed the expert on a particular topic.
    
    In addition to these types, on creation of a Press Room, we setup some logic folders and smart
    folders that help slice and dice your releases, clips, and contacts in typical ways, as 
    seen in other Press Rooms throughout the internet.
    
    Some press rooms we observed in making this product were found at: microsoft.com, intel.com,
    nrdc.org, sierraclub.org, and google.com.  The goal was to make something suitable cross-sector.

Current Status of Press Room

    This is pre-alpha quality code!  Please do not use this on anything other than a test/sandbox 
    instance.  Please do give feedback about what you want to see to make this alpha quality!


Installation

    Install in the usual way, by:

        - Uncompressing PressRoom in your Zope instances "products" directory
        - Browse to your plone site --> site setup --> add/remove products
        - click install (alternately: used the QuickInstaller tool in the Zope Management Interface)

    Tested with Plone 2.1.3 and Archetypes 1.3.9-final, though this is likely to work with each Plone 
    version within the Plone 2.1.x branch.

  Known Issues and Potential Improvements

    o Internationalization is weak at this point, but intended to be added asap
    
    o On creation of a PressRoom, several logical smart folders are created, which is a manager/owner-only
    content type.  Thus, a PressRoom appears addable within the member folder and should not.  Need to remove
    this as an allowable type to members, since this is confusing.
    
    o More issues listed in TODO.txt
    
  Authors

    Andrew Burkhalter (andrewb AT onenw DOT org)
    Jon Baldivieso (jonb AT onenw DOT org)
    Trey Beck (trey DOT beck AT ohtogo DOT com)

  We're interested to hear feedback and information about how this is being used.  Please consider
  sending email to any of the above contacts.