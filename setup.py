from distutils.core import setup
setup(
    name='python-plus-plus',
    packages=['ppp_lib'],
    entry_points={
        "console_scripts": ['ppp = ppp_lib.__main__:main']
    },
    version='1.0.0',
    description='All the functionality of Python, with less of the annoyances.',
    author='Jason Chan, James Liu, Shikib Mehri, William Qi',
    url='https://github.com/python-plus-plus/python-plus-plus',
    download_url='https://github.com/python-plus-plus/python-plus-plus/archive/1.0.0.tar.gz',
    keywords=['python++', 'tail call optimization', 'mutable default', 'deep copy', '++'],
    classifiers=[],
)
