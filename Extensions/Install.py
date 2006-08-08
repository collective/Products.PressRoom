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
    for type in types_to_add:
        if type not in types:
            types.append(type)
    factory.manage_setPortalFactoryTypes(listOfTypeIds = types)
    print >> out, "Added press room content types to portal_factory"

    propsTool = getToolByName(self, 'portal_properties')
    siteProperties = getattr(propsTool, 'site_properties')
    navtreeProperties = getattr(propsTool, 'navtree_properties')

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

    # Add FileAttachment and ImageAttachment to kupu's linkable and media
    # types
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


    # kupu_library_tool has an idiotic interface, basically written purely to
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

    # enable key fields with portal_atct tool
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

    print >> out, "Enabling the getObjPositionInParent and getPublic index fields, updating settings on the Type index field with the portal_atct tool"

    return out.getvalue()