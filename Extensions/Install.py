from Products.CMFCore.utils import getToolByName
from Products.CMFFormController.FormAction import FormActionKey
from Products.Archetypes.Extensions.utils import installTypes
from Products.Archetypes.Extensions.utils import install_subskin
from Products.Archetypes.public import listTypes

from StringIO import StringIO

from Products.CMFDynamicViewFTI.migrate import migrateFTIs

from Products.PressRoom.config import *

def install(self):
    """Install press room content types, skin layer, stylesheet, 
    set up global properties, enable the portal factory
    """

    out = StringIO()

    print >> out, "Installing Press Room"

    # Install types
    classes = listTypes(PROJECTNAME)
    installTypes(self, out,
                 classes,
                 PROJECTNAME)
    print >> out, "Installed types"

    # Install skin
    install_subskin(self, out, product_globals)
    print >> out, "Installed skin"

    # Migrate FTI, to make sure we get the necessary infrastructure for the
    # 'display' menu to work.
    migrated = migrateFTIs(self, product=PROJECTNAME)
    print >>out, "Switched to DynamicViewFTI: %s" % ', '.join(migrated)

    # Install stylesheet
    portal_css = getToolByName(self, 'portal_css')
    portal_css.manage_addStylesheet(id = 'PressRoom.css',
                                    expression = 'python:object.getTypeInfo().getId() in ("PressRoom","PressRelease","PressClip","PressContact")',
                                    media = 'all',
                                    title = 'PressRoom styles',
                                    enabled = True)

    # Enable portal_factory
    factory = getToolByName(self, 'portal_factory')
    types = factory.getFactoryTypes().keys()
    types_to_add = ('PressClip','PressContact','PressRelease',)
    for t in types_to_add:
        if t not in types:
            types.append(t)
    factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    print >> out, "Added press room content types to portal_factory"

    propsTool = getToolByName(self, 'portal_properties')
    siteProperties = getattr(propsTool, 'site_properties')

    # Add the PressContact to types_not_searched
    # (this is configurable via the Search settings control panel)
    typesNotSearched = list(siteProperties.getProperty('types_not_searched'))
    if 'PressContact' not in typesNotSearched:
        typesNotSearched.append('PressContact')
    siteProperties.manage_changeProperties(types_not_searched = typesNotSearched)
    print >> out, "Added PressContact to types_not_searched"

    # Add to default_page_types
    defaultPageTypes = list(siteProperties.getProperty('default_page_types'))
    for type in ("PressRelease","PressClip",):
        if type not in defaultPageTypes:
            defaultPageTypes.append(type)
    siteProperties.manage_changeProperties(default_page_types = defaultPageTypes)

    # Add FileAttachment and ImageAttachment to kupu's linkable and collection types
    kupuTool = getToolByName(self, 'kupu_library_tool')
    linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
    collection = list(kupuTool.getPortalTypesForResourceType('collection'))
    mediaobject = list(kupuTool.getPortalTypesForResourceType('mediaobject'))

    for t in ("PressRoom","PressRelease","PressClip","PressContact",):
        if t not in linkable:
            linkable.append(t)

    for t in ('PressRoom',):
        if t not in collection:
            collection.append(t)

    # kupu_library_tool has an odd interface, basically written purely to
    # work with its configuration page. :-(
    kupuTool.updateResourceTypes(({'resource_type' : 'linkable',
                                   'old_type'      : 'linkable',
                                   'portal_types'  :  linkable},
                                  {'resource_type' : 'mediaobject',
                                   'old_type'      : 'mediaobject',
                                   'portal_types'  :  mediaobject},
                                  {'resource_type' : 'collection',
                                   'old_type'      : 'collection',
                                   'portal_types'  :  collection},))
    print >> out, "Added PressRoom types to kupu's linkable types, PressRoom type to collection"
    
    # enable two indices to be used by smart folders
    smart_folder_tool = getToolByName(self, 'portal_atct')

    index = smart_folder_tool.getIndex("getObjPositionInParent")
    index_def = {'index'        : index.index,
                 'friendlyName' : index.friendlyName,
                 'description'  : index.description,
                 'criteria'     : index.criteria
                }
    smart_folder_tool.addIndex(enabled=True, **index_def)

    typeIndex = smart_folder_tool.getIndex("Type")
    typeIndex_def = {'index'        : typeIndex.index,
                     'friendlyName' : typeIndex.friendlyName,
                     'description'  : typeIndex.description,
                     'criteria'     : typeIndex.criteria + ("ATListCriterion",)
                    }
    smart_folder_tool.addIndex(enabled=True, **typeIndex_def)

    print >> out, "Enabling the getObjPositionInParent and getPublic indices for use by smart folders, updating settings on the Type index field with the portal_atct tool"
    
    # Add folder_listing_pressroom view to topic view methods
    types_tool = getToolByName(self, 'portal_types')
    topicFTI = types_tool.getTypeInfo('Topic')
    if topicFTI:
        view_methods = list(topicFTI.view_methods)
        if 'folder_listing_pressroom' not in view_methods:
            view_methods.append('folder_listing_pressroom')
            topicFTI.view_methods = tuple(view_methods)
    print >> out, "Added folder_listing_pressroom view to topic view methods"
    

    return out.getvalue()

def uninstall(portal, reinstall=False):
    """Remove PressRoom cruft"""
    out = StringIO()

    print >> out, "Uninstalling Press Room"
    
    # 1: Fix Kupu settings
    #    Remove PressRoom types from kupu's linkable & collection types
    kupuTool = getToolByName(portal, 'kupu_library_tool')
    linkable    = list(kupuTool.getPortalTypesForResourceType('linkable'))
    collection  = list(kupuTool.getPortalTypesForResourceType('collection'))
    mediaobject = list(kupuTool.getPortalTypesForResourceType('mediaobject'))

    for t in ("PressRoom","PressRelease","PressClip","PressContact",):
        if t in linkable:
            linkable.remove(t)

    if 'PressRoom' in collection:
        collection.remove('PressRoom')

    kupuTool.updateResourceTypes(({'resource_type' : 'linkable',
                                   'old_type'      : 'linkable',
                                   'portal_types'  :  linkable},
                                  {'resource_type' : 'mediaobject',
                                   'old_type'      : 'mediaobject',
                                   'portal_types'  :  mediaobject},
                                  {'resource_type' : 'collection',
                                   'old_type'      : 'collection',
                                   'portal_types'  :  collection},))
    print >> out, "Removed reference to PressRoom types from kupu's linkable and collection types"

    # 2: Remove PressRoom's contributions to various portal_properties.site_properties props
    props_tool = getToolByName(portal, 'portal_properties')
    if hasattr(props_tool, 'site_properties'):
        site_properties = getattr(props_tool, 'site_properties')

        types_not_searched = list(site_properties.getProperty('types_not_searched'))
        if 'PressContact' in types_not_searched:
            types_not_searched.remove('PressContact')
            site_properties.manage_changeProperties(types_not_searched = types_not_searched)
            print >> out, "Removed PressContact from types_not_searched"

        # default_page_types
        defaultPageTypes = list(site_properties.getProperty('default_page_types'))
        for t in ("PressRelease","PressClip",):
            if t in defaultPageTypes:
                defaultPageTypes.remove(t)
        site_properties.manage_changeProperties(default_page_types = defaultPageTypes)
        print >> out, "Removed PressRoom types from default page types"

        # use_folder_tabs (i couldn't find any installation code for this, but it 
        # still seems to be getting added to this property)
        use_folder_tabs = list(site_properties.getProperty('use_folder_tabs'))
        if 'PressRoom' in use_folder_tabs:
            use_folder_tabs.remove('PressRoom')
            site_properties.manage_changeProperties(use_folder_tabs = use_folder_tabs)
            print >> out, "Removed PressRoom from use_folder_tabs"

        # typesLinkToFolderContentsInFC (same thing: i couldn't find any installation
        # code for this, but it still seems to be getting added to this property)
        typesLinkToFolderContentsInFC = list(site_properties.getProperty('typesLinkToFolderContentsInFC'))
        if 'PressRoom' in typesLinkToFolderContentsInFC:
            typesLinkToFolderContentsInFC.remove('PressRoom')
            site_properties.manage_changeProperties(typesLinkToFolderContentsInFC = typesLinkToFolderContentsInFC)
            print >> out, "Removed PressRoom from typesLinkToFolderContentsInFC"
        
    # 3: Remove 'folder_listing_pressroom' view from topic's list of view methods
    types_tool = getToolByName(portal, 'portal_types')
    topicFTI = types_tool.getTypeInfo('Topic')
    if topicFTI:
        view_methods = list(topicFTI.view_methods)
        if 'folder_listing_pressroom' in view_methods:
            view_methods.remove('folder_listing_pressroom')
            topicFTI.view_methods = tuple(view_methods)
            print >> out, "Removed 'folder_listing_pressroom' view from topic's list of view methods"


    return out.getvalue()

