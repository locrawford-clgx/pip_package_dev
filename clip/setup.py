from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name = 'Clip_test_library',
    url = 'https://github.com/corelogic/saa-geospatial-tools/tree/master/clip',
    author = 'Logan Crawford',
    author_email = 'locrawford@corelogic.com',
    
    # Needed to actually package something
    packages = ['clip'],
    
    # Needed for dependencies
    install_requires = ['os', 'json', 'requests', 'pandas', 'datetime'],
    
    # *strongly* suggested for sharing
    version = '1.0.0',
    
    # The license can be anything you like
    
    license = 'MIT',
    description = 'An example of a python package from pre-existing code',
    long_description = open('README.txt').read(),
)