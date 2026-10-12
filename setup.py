from setuptools import find_packages,setup
from typing import List

def get_requirements()-> List[str]:
    """
    This Function will return list of requirments
    """

    requirement_lst:List[str]=[]
    
    try:
        with open('requirements.txt','r') as file:
            lines = file.readlines()

            for line in lines:
                requirement = line.strip()

                if requirement and requirement != "-e .":
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")

    return requirement_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author_email="samar20464@iiitd.ac.in",
    packages=find_packages(),
    install_requires=get_requirements()
)