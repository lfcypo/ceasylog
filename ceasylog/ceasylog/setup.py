from setuptools import setup, find_packages

setup(
    name='ceasylog',
    version='1.2.2',
    keywords='ceasylog',
    description='A great log util from CandyStar',
    author='CandyStar@HuangXudong',
    license='Apache License 2.0',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=['colorama', 'requests'],
)
