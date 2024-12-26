from setuptools import setup, find_packages

setup(
    name="PyNOTES",
    version="0.1.0",
    author="Hsuan-Han Chiu",
    author_email="chiu137@purdue.edu",
    description="This is a simple optimization and economic evaluation package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sean55123/PyNOTES",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=["numpy", 
                      "pandas", 
                      "scipy", 
                      "matplotlib"],  
)
