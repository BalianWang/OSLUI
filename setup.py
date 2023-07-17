from setuptools import setup, find_packages

setup(
    name='oslui',
    version='0.1.0',
    url='https://github.com/BalianWang/OSLUI',
    author='BalianWang',
    author_email='balian.wang1997@gmail.com',
    description='Natural Language User Interface for Operating Systems',
    packages=find_packages(),
    install_requires=[
        'openai',
        'guidance',
        'google-search-results',
    ],
    entry_points={
        'console_scripts': [
            'oslui = oslui.main:main',
        ],
    },
    license='MIT',
    python_requires='>=3'
)
