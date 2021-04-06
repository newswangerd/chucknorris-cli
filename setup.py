from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='chucknorris-cli',
    version='1.0.0',
    entry_points={
        'console_scripts': ['chucknorris=chucknorris_cli.main:main'],
    },
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/newswangerd/chucknorris-cli',
    description='The finest selection of Chuck Norris jokes.'
)
