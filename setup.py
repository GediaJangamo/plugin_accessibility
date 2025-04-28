from setuptools import setup, find_packages

setup(
    name="siga-accessibility",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    description="Accessibility plugin for Django applications (SIGA)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Gédia Genifa Lucas Jangamo",
    author_email="gedyahgennyfah@gmail.com",
    url="https://github.com/GediaJangamo/plugin_accessibility.git",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.2",
    ],
)