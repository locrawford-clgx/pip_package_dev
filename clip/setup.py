from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name="clip",
    url="https://github.com/locrawford-clgx/pip_package_dev/tree/main/clip",
    author="Logan Crawford",
    author_email="locrawford@corelogic.com",
    
    # Needed to actually package something
    packages=["clip"],
    
    # Needed for dependencies
    install_requires=["requests", "pandas"],
    
    # *strongly* suggested for sharing
    version="1.0.0",
    
    # The license can be anything you like
    license="MIT",
    description="An example of a Python package from pre-existing code",
    long_description=open("README.md").read(),
)
