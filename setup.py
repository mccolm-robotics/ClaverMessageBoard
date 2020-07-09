from setuptools import setup

# read the contents of the README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Claver-Message-Board',
    version='0.0.3',
    packages=['interface', 'interface.gui', 'interface.news', 'interface.games', 'interface.lists', 'interface.timer',
              'interface.doodle', 'interface.photos', 'interface.widgets', 'interface.calendar', 'interface.messages',
              'interface.settings', 'interface.settings.categories'],
    url='https://github.com/mccolm-robotics/Claver-Interactive-Message-Board',
    license='MIT',
    description='Interactive messaging board for RPi',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
