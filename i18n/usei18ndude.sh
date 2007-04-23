#!/bin/bash 

PRODUCT="pressroom"
DOMAIN="pressroom"

i18ndude rebuild-pot --pot $PRODUCT.pot --create $DOMAIN --merge manual.pot ../

if [ -f $PRODUCT-??.po ]; then
    i18ndude sync --pot $PRODUCT.pot $PRODUCT-??.po;
fi

if [ -f $PRODUCT-plone-??.po ]; then
    i18ndude sync --pot $PRODUCT-plone.pot $PRODUCT-plone-??.po
fi


