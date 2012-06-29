from setuptools import setup
import finddata


setup(
    name="mwt",
    author="Florian Finke",
    author_email="flo@randomknowledge.org",
    version='0.1.1',
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
    install_requires=['Django==1.4', 'South==0.7.5', 'pytz', 'html5lib==0.95', 'lxml==2.3.4', 'rq'],
    dependency_links=['https://github.com/nvie/rq/tarball/master#egg=rq'],
    classifiers=[
        #'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        #'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production/Stable',
        #'Development Status :: 6 - Mature',
        #'Development Status :: 7 - Inactive',

        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',

        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',

        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',

        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Monitoring',
        ]
)
