Press Room

    Press Room is a simple add-on product which can be used to easily manage an online
    Press Room within your Plone site.  It adds 3 new content types to your Plone site 
    including a Press Release, a Press Clip (i.e. a reference to your organization in the news), 
    and Press Contact, which is a person within or outside of your organization that has been 
    deemed the expert on a particular topic.
    
    In addition to these types, we also provide a Press Room, which is a folderish object
    that contains a nice default view plus some folders and smart folders to help you organize
    and present your press materials.
    
    Some press rooms we observed in making this product were found at: microsoft.com, intel.com,
    nrdc.org, sierraclub.org, and google.com.  Our goal was to make something suitable for many kinds of
    organizations, including nonprofits, businesses, educational institutions, and more.

Current Status of Press Room

    This is beta quality code!  Please do not use this on anything other than a test/sandbox 
    instance.  Please do give feedback about what you want to see to make Press Room production quality!


Installation

    Install in the usual way, by:

        - Uncompressing Press Room in your Zope instances "products" directory
        - Browse to your plone site --> site setup --> add/remove products
        - click install (alternately: used the QuickInstaller tool in the Zope Management Interface)

    Tested with Plone 2.1.3 + Archetypes 1.3.9-final and Plone 2.5 + Archetypes 1.4.0 final. 
    We believe it should also work with Plone 2.1, 2.1.1 and 2.1.2, but have not tested.

 Known Issues and Potential Improvements

    * Internationalization is weak at this point, but intended to be added asap
            
    * More issues listed in TODO.txt
    
    * Suggestions welcome!  (Code even more welcome!)

Usage

     We recommend creating a Press Room object in the root of your site.
     Then, begin creating Press Releases, Press Clips and Press Contacts in your
     Press Room.  
     
     The "Add Press (item)" links in the Press Room will shortcut you to
     subfolders intended to store your items.  Only items stored in their appropriate 
     subfolder will be shown in the Press Room listing view.
     
     You can also create Press Releases, Clips and Contacts elsewhere in your site,
     but these will not be shown in the Press Room view.
    
 Authors
  
   See CREDITS.TXT

   