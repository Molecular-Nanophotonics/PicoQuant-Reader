

import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
     name='dokr',  
     version='0.1',
     scripts=['dokr'] ,
     author="Deepak Kumar",
     author_email="deepak.kumar.iet@gmail.com",
     description="A Docker and AWS utility package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/javatechy/dokr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )



from distutils.core import setup

with open("README.md", "r") as f:
    long_description = f.read()
    
setup(
    name = 'pqreader',         # How you named your package folder (MyLib)
    #packages = ['YOURPACKAGENAME'],   # Chose the same as "name"
    version = '0.1',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'TYPE YOUR DESCRIPTION HERE',   # Give a short description about your library
    long_description = long_description,
    author = 'Martin',                   # Type in your name
    author_email = 'martin.fraenzl@physik.uni-leipzig.de',      # Type in your E-Mail
    url = 'https://github.com/molecular-nanophotonics/pqreader',    # I explain this later on
    classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
    ],
)