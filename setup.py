#Setup based off of https://trstringer.com/easy-and-nice-python-cli/

from setuptools import setup
setup(
    name = 'WhereShouldIHaveGone',
    version = '0.1.0',
    packages = ['get_attractions'],
    entry_points = {
        'console_scripts': [
            'WhereShouldIHaveGone = get_attractions.__main__:main'
        ]
    })
