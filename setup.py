from setuptools import setup, find_packages

setup(
    name='MusicCLI',
    version='1.0',
    license='MIT',
    author="Otabek Nurmatov",
    author_email='mrotabek17@gmail.com',
    packages=find_packages('./'),
    package_dir={'': './'},
    url='https://github.com/otabeknurmatov/MusicCLI',
    keywords='MusicCLI',
    install_requires=[
        'requests',
        'bs4',
        'beautifulsoup4',
        'lxml',
    ],
)