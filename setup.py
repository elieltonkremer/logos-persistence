from setuptools import setup

setup(
    name='logos-persistence',
    version='0.2',
    packages=['logos_persistence'],
    url='',
    license='MIT',
    author='Elielton Kremer',
    author_email='elieltonkremer2392@gmail.com',
    description='Logos persistence module',
    install_requires=[
        'peewee'
    ],
    dependency_links=[
        'https://github.com/elieltonkremer/logos.git'
    ]
)
