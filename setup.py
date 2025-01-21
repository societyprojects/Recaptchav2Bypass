from setuptools import setup, find_packages

setup(
    name='Rcptchv2Bypss',
    version='0.0.1',
    author='Thunder (@thd3r)',
    author_email='thd3r@proton.me',
    description='Rcptchv2Bypss',
    packages=find_packages(),
    install_requires=[
        'rich',
        'pydub',
        'asyncio',
        'selenium',
        'SpeechRecognition',
        'webdriver-manager'
    ],
    entry_points={
        'console_scripts': [
            'rcptchv2bypss = src.main'
        ]
    },
    license='MIT',
    url='https://github.com/societyprojects/Rcptchv2Bypss',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['Rcptchv2Bypss', 'Recaptchav2', 'captchav2']
)
