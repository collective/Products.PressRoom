1) Set up your environment
add the following lines to your ~/.bash_profile after you doctor the parts in red (to suit your local zope install/instance):
export INSTANCE_HOME='/path/to/instance/home'
export SOFTWARE_HOME='/path/to/software/home'                       

2) Download PloneTestCase and put it in your Products dir (http://plone.org/products/plonetestcase)

3) Change directory to any one of the Products with test suites
cd CMFPlone/tests
cd ATContentTypes/tests
cd PressRoom/tests

and run all the tests. You can run individual ones as well.

python runalltests.py

If the extensive output ends with "OK", they passed. Failure is more self-evident...