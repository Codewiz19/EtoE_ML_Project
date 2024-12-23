'''
setup.py is a configuration script commonly used in Python projects to define how a project should
be packaged and distributed. It is primarily associated with Python's packaging ecosystem, 
particularly for projects that use Setuptools.
'''

from setuptools import setup,find_packages
from typing import List

def get_requirements(file_path:str)->   List[str] :
    '''
    This function returns a list of strings representing the dependencies
    '''
    requirments = [] 
    with open(file_path) as file_obj:
        requirments = file_obj.readlines()
        # but readlies will also read \n
        requirments = [req.replace("\n","") for req in requirments]

        if "-e ." in requirments :
            requirments.remove("-e .")

    return requirments



setup(
    name='Project 1',
    version='1.0',
    author='Code_Wiz',
    packages= find_packages(),
    install_requires= get_requirements('requirements.txt'),

)