from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name="cmdfinder",
    version="2.3.0",
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
        "pygtail",
    ],

    package_data={
        "cmdfinder": ["ui/*.tcss"],
    },

    entry_points={
        "console_scripts": [
            # Main TUI application
            "cmdfinder = cmdfinder.ui.app:main",
            "cf = cmdfinder.ui.app:main",
            # Background watcher process
            "cmdfinder-watcher = cmdfinder.utils.watcher:watch",
            # Service setup utility
            "cmdfinder-setup = cmdfinder.utils.service_installer:install_service",
        ],
    },

    long_description=description,
    long_description_content_type="text/markdown"
)