from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='py-bingx',
    version='0.4',
    license='MIT',
    author="Amirhossein Zare",
    description='BingX REST API Python implementation',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author_email='',
    packages=['bingx'],
    url='https://github.com/amirinsight/py-bingx',
    keywords='bingx api cryptocurrency trading btc eth rest exchange',
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],

)
