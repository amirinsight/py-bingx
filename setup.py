from setuptools import setup, find_packages

setup(
    name='py-bingx',
    version='0.1',
    license='MIT',
    author="M1raX",
    author_email='mirax@mirax.com',
    packages=find_packages('bingx'),
    package_dir={'': 'bingx'},
    url='https://github.com/M1raX/py-bingx',
    keywords='bingx api',
    install_requires=[
        'requests',
    ],

)
