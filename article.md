# How to Build and Publish your own Python Command Line Tool

When I was learning python in university, our workflow was to use python's `input()` function to get information from the user. A typical assignment would look like:

```shell
$ python3 my_assginment.py 
Enter parameter 1: foo
Enter parameter 2: bar
Enter parameter 3: foobar
```

While this is a convenient way to do things when you're learning how to code, it's not going to help you build and publish anything that anyone else can easily consume. The goal of this article is help bridge the gap between writing a basic script for an assignment and building a real package that can be distributed to other developers.

The final code from this tutorial can be found at [https://github.com/newswangerd/chucknorris-cli](https://github.com/newswangerd/chucknorris-cli) and the final build can be found on [PyPI](https://pypi.org/project/chucknorris-cli/1.0.0/).

## Project Setup

First things first, lets create a new python module for our CLI tool. It will look something like this.

```
├── chucknorris_cli
│   ├── __init__.py
│   ├── main.py
│   └── quips.py
├── README.md
└── setup.py
```

We've got a python module named `chucknorris_cli` that contains `quips.py` and `main.py` and a top level `setup.py`.

This is what `quips.py` looks like:
```python
import random

quips = '''When Alexander Bell invented the telephone, he had three missed calls from {name}.
Fear of spiders is arachnophobia, fear of tight spaces is claustrophobia, fear of {name} is called logic.
{name} doesn't call the wrong number. You answer the wrong phone.
There used to be a street named after {name}, but it was changed because nobody crosses {name} and lives.
Ghosts sit around the campfire and tell {name} stories.
{name} has already been to Mars. That's why there are no signs of life.
{name} won American Idol using only sign language.'''

def quip(name = "Chuck Norris", number=None):
    q = quips.split('\n')

    if number is None:
        return random.choice(q).format(name=name)
    else:
        return q[number % len(q)].format(name=name)
```

And this is what `main.py` looks like:
```python
from quips import quip

def main():
    name = input('Enter a name (default: Chuck Norris): ')
    number = input('Enter a number for a quip (default: random): ')

    if name == '':
        name = 'Chuck Norris'
    if number == '':
        number = None
    else:
        number = int(number)

    print(quip(name=name, number=number))

main()
```

`main.py` simply imports `quip()` from `quips` and uses `input()` to get information from the user.

This is what it looks like:

```shell
$ python3 chucknorris_cli/main.py 
Enter a name (default: Chuck Norris): Chucky 
Enter a number for a quip (default: random): 29
Fear of spiders is arachnophobia, fear of tight spaces is claustrophobia, fear of Chucky is called logic.
```

## Running the Project as it's own CLI

We don't want to launch our CLI tool by running `$ python3 path/to/main.py`. Instead we want to something like `$ chucknorris`. To accomplish that, lets take a look at our `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name='chucknorris-cli',
    version='1.0.0',
    entry_points={
        'console_scripts': ['chucknorris=chucknorris_cli.main:main'],
    },
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
)
```

The part we care about here is `'console_scripts': ['chucknorris=chucknorris_cli.main:main']`. This tells python to create an executable in you `PATH` that points the `chucknorris` command to run the `main()` function in `chucknorris_cli.main`. To install our new command, simply run `pip install -e .`. This will take the current project and install it in editable mode so that we can make changes. If you're using the system python, this won't always install the script to a directory that's in your `PATH`, so I recommend using [virtualenvs](https://docs.python.org/3/tutorial/venv.html) for this.

Now we can run `chucknorris`.

```shell
$ chucknorris
Traceback (most recent call last):
  [...]
  File "/home/david/code/sample-python-cli/chucknorris_cli/main.py", line 1, in <module>
    from quips import quip
ModuleNotFoundError: No module named 'quips'
```

But wait! This breaks. The reason for this is `main.py` is trying to import `quips.py` locally, which works when running it using `python3 main.py`, but not when the package is installed. Installing our module as a package allows us to reference it globally and so we can fix this issue by updating `main.py` to use the following import:

```python
from chucknorris_cli.quips import quip

def main():
    [...]
```

Now we can run the command again:
```shell
$ chucknorris 
Enter a name (default: Chuck Norris): Norry
Enter a number for a quip (default: random): 
Norry won American Idol using only sign language.
```

## Parse CLI Arguments

Our tool still uses `input()`, which we want to avoid. Instead we want to be able to pass a name and number via CLI arguments. To do that, we'll update `main.py` to use `argparse`.

```python
import argparse

from chucknorris_cli.quips import quip

def parse_args():
    parser = argparse.ArgumentParser(description='The finest selection of Chuck Norris jokes.')
    parser.add_argument('name', nargs='?', default='Chuck Norris', help='Use another name.')
    parser.add_argument('--number', '-n', type=int, dest='quip_number', help='Pick a specific quip.')

    return parser.parse_args()

def main():
    args = parse_args()

    print(quip(name=args.name, number=args.quip_number))
```

This adds two arguments:
- `name`: An optional positional parameter that allows the user to pick a name to substitute in for Chuck Norris.
- `--number`, `-n`: Allows the user to specify a specific joke by number using either `--number 29` or `-n 29`.

Argparse has a ton of functionality that you can read more about on the official [python docs](https://docs.python.org/3/library/argparse.html)

Now we can run:
```shell
$ chucknorris Chuckster --number 29
Fear of spiders is arachnophobia, fear of tight spaces is claustrophobia, fear of Chuckster is called logic.
```

## Publish the Project

Before publishing the project, lets add some more information to our `setup.py` to make it easier to use.

```python
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
```

This simply adds a description and our README file as the long description, which will make it appear on the PyPI page. `setup.py` has more metadata you can add. More information about it can be found on the [official python docs](https://docs.python.org/3/distutils/setupscript.html)

Before we proceed, you'll need to install twine and build
```shell
$ pip install build
$ pip install twine
```

To build the project simply run `python3 -m build`. This will create two new directories:
- `dist`: the build python packages which can be uploaded to PyPI.
- `build`: the build context that setup uses to create the packages.

To publish the newly build package run:

```shell
$ $ twine upload dist/*
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: <your_username> 
Enter your password: 
Uploading chucknorris_cli-1.0.0-py3-none-any.whl
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 5.70k/5.70k [00:01<00:00, 3.01kB/s]
Uploading chucknorris-cli-1.0.0.tar.gz
100%|█████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████| 4.98k/4.98k [00:00<00:00, 5.93kB/s]

View at:
https://pypi.org/project/chucknorris-cli/1.0.0/
```

This will upload the package in `dist/` to PyPI. Our tool can can now be installed by simply running `pip install chucknorris-cli`.

A more in depth tutorial on publishing packages can be found on the [official python docs](https://packaging.python.org/tutorials/packaging-projects/)

## Conclusion
You should have everything you need to know in order to build and publish your very own python CLI.