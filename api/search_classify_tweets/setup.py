from setuptools import setup, find_packages

setup(
    name='ppa',
    version='1.0.0',
    description='Arquitetura padrão Microservice módulo.',
    url='-',
    author='Lucas Dynczuki',

    classifiers=[
        'Development Status :: Developer/Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='Flasgger documentation',

    packages=find_packages(),

    install_requires=['flask-restplus==0.13.0', 'Flask-SQLAlchemy==2.1'],
)
