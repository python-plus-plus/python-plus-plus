from distutils.core import setup
setup(
    name='python-plus-plus',
    packages=['ppp_lib'],  # this must be the same as the name above
    entry_points={
        "console_scripts": ['ppp = ppp_lib.__main__:main']
    },
    version='0.1',
    description='All the functionality of Python, with less of the annoyances.',
    author='Jason Chan, James Liu, Shikib Mehri, William Qi',
    author_email='',
    url='https://github.com/python-plus-plus/python-plus-plus',  # use the URL to the github repo
    download_url='https://github.com/python-plus-plus/python-plus-plus',  # I'll explain this in a second
    keywords=['python++', 'tail call optimization', 'mutable default', 'deep copy', '++'],  # arbitrary keywords
    classifiers=[],
)
