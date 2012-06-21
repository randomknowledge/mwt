from setuptools import setup
import finddata


setup(
    name="mwt",
    author="Florian Finke",
    author_email="flo@randomknowledge.org",
    version='0.1.0',
    packages=['mwt'],
    package_data=finddata.find_package_data(),
    url='https://git.randomknowledge.org/mwt',
    include_package_data=True,
    license='MIT',
    description='mwt or multipurpose website testing is a django app'
                ' for managing website tests (like "is site up).'
                ' New tests are can be added as plugins.',
    long_description=open('Readme.md').read(),
    zip_safe=False,
    install_requires=['Django==1.4', 'South==0.7.5', 'redis==2.4.13',
        'Celery==2.5.5', 'django-celery==2.5.5', 'pytz'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
)
