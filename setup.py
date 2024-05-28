# setup.py

from setuptools import setup, find_packages
import os

# Read the long description from the README file


def read_long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()


setup(
    name='voice-assistant-tutor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'SpeechRecognition',
        'pygame',
        'openai',
        'groq',
        'deepgram-sdk',
        'python-dotenv',
        'colorama',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'voice-assistant-tutor=run_voice_assistant:main'
        ]
    },
    author='Ayush Pujari',
    author_email='ayush08.pujari@gmail.com',
    description='A modular voice assistant application with support for multiple state-of-the-art models.',
    long_description=read_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ayush-Pujari-07/voice-assistant-tutor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    python_requires='>=3.10',
    include_package_data=True,
)
