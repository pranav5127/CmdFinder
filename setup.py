from setuptools import setup, find_packages

setup(
    name="cmdfinder",
    version="1.0.0",
    description="Search and run shell history with a Textual TUI",
    packages=find_packages(),
    python_requires=">=3.10",
    include_package_data=True,

    install_requires=[
        "linkify-it-py==2.0.3",
        "markdown-it-py==4.0.0",
        "mdit-py-plugins==0.5.0",
        "mdurl==0.1.2",
        "platformdirs==4.5.0",
        "Pygments==2.19.2",
        "RapidFuzz==3.14.3",
        "rich==14.2.0",
        "textual==6.6.0",
        "typing_extensions==4.15.0",
        "uc-micro-py==1.0.3",
    ],

    package_data={
        "cmdfinder": ["*.tcss"],
    },

    entry_points={
        "console_scripts": [
            "cmdfinder = cmdfinder.app:main",
            "cf = cmdfinder.app:main",
        ],
    },
)
