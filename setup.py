from setuptools import setup

# https://pypi.org/pypi?%3Aaction=list_classifiers
# https://oceanprotocol.github.io/dev-ocean/doc/development/python-developer-guide.html

# read the contents of the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Claver-Message-Board',
    version='0.0.4',
    packages=['interface', 'interface.gui', 'interface.news', 'interface.games', 'interface.lists', 'interface.timer',
              'interface.doodle', 'interface.photos', 'interface.widgets', 'interface.calendar', 'interface.messages',
              'interface.settings', 'interface.settings.categories'],
    url='https://github.com/mccolm-robotics/Claver-Interactive-Message-Board',
    license='MIT',
    description='Interactive messaging board for RPi',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications :: GTK',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Communications :: Chat',
        'License :: OSI Approved :: MIT License'
    ]
)

print(setup.version())
