from setuptools import setup, find_packages
from aio_cache import __version__

install_requires = []

with open("init.reqs.txt") as f:
    for l in f.readlines():
        while l.endswith('\n'):
            l = l[:-1]
        if l == '':
            continue
        install_requires.append(l)

setup(name='aio_cache',
      version=__version__,
      description='python cache library for asyncio projects',
      url='https://github.com/anhaeh/aio_cache',
      author='Andres Haehnel',
      packages=find_packages(exclude=["tests", "tests.*"]),
      zip_safe=False,
      install_requires=install_requires)
