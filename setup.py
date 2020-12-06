from setuptools import setup
setup(
    name = 'get_attractions',
    version = '0.1.0',
    packages = ['get_attractions'],
    entry_points = {
        'console_scripts': [
            'get_attractions = get_attractions.__main__:main'
        ]
    })
