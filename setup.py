# -*- coding:utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='apweb',
    version='1.0.dev1',
    description='Common AP pyramid patterns',
    long_description = open('README.rst').read(),
    long_description_content_type='text/x-rst',
    classifiers=['Programming Language :: Python', 'Framework :: Pyramid'],
    keywords='pyramid',
    author='Adam & Paul Pty Ltd',
    author_email='tech@adamandpaul.biz',
    url='https://adamandpaul.biz',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',

        'pyramid',
        'pyramid_chameleon',
        'pyramid_exclog',
        'pyramid_tm',
        'pyramid_mailer',
        'pyramid_nacl_session',

        'sqlalchemy',
        'sqlalchemy-utils',
        'zope.sqlalchemy',

        'redis',

        'pyjwt',
        'bcrypt',

        'contextplus>1.9',

        'psycopg2-binary',
    ],
    entry_points="""
        [console_scripts]
        #tool = package.module:main
    """,
)
