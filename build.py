from pybuilder.core import use_plugin, init, Author

use_plugin("python.install_dependencies")
use_plugin("python.core")
use_plugin("python.distutils")

authors = [Author('Marco Hoyer', 'marco.hoyer@immobilienscout24.de')]
description = """whisper-schema-info - simple helper displaying storage and aggregation config equivalent to carbon for a given metric name

for more documentation, visit https://github.com/marco-hoyer/whisper-schema-info
"""

name = 'whisper-schema-info'
license = 'GNU GPL v3'
summary = 'whisper-schema-info - simple helper displaying storage and aggregation config equivalent to carbon for a given metric name'
url = 'https://github.com/marco-hoyer/whisper-schema-info'
version = '1.0'

default_task = ['publish']


@init
def initialize(project):

    project.depends_on("argparse")

    project.set_property('dir_dist_scripts', 'scripts')

    project.set_property('distutils_classifiers', [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: System :: Monitoring',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ])


@init(environments='teamcity')
def set_properties_for_teamcity_builds(project):
    import os

    project.version = '%s-%s' % (project.version, os.environ.get('BUILD_NUMBER', 0))
    project.default_task = ['install_dependencies', 'package']
    project.set_property('install_dependencies_use_mirrors', False)
    project.get_property('distutils_commands').append('bdist_rpm')