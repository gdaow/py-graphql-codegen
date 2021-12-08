#!python
"""Helpers for setuptools to build & install py-graphql-codegen."""
from pathlib import Path
from re import compile as re_compile
from subprocess import CalledProcessError
from subprocess import DEVNULL
from subprocess import check_output
from typing import Iterable
from typing import Union

from setuptools import setup


def _get_child_directories(path: Path) -> Iterable[Path]:
    for child in path.iterdir():
        if child.is_dir():
            yield child


def _find_packages(root: Union[str, Path]) -> Iterable[str]:
    root = Path(root)
    init_path = root / '__init__.py'
    if init_path.is_file():
        yield str(root)

    for child in _get_child_directories(root):
        for package in _find_packages(child):
            yield package


def _get_git_version() -> str:
    """Get package version from git tags."""
    pattern = re_compile(
        r'^v(?P<version>\d*\.\d*\.\d*)(-\d*-g(?P<commit>\d*))?'
    )
    try:
        command = [
            'git', 'describe',
            '--tags',
            '--match', 'v[0-9]*.[0-9]*.[0-9]*'
        ]
        version_bytes = check_output(command, stderr=DEVNULL)
        git_version = version_bytes.decode('utf-8')
        match = pattern.match(git_version)
        if match is not None:
            commit = match.group('commit')
            git_version = match.group('version')
            if commit is not None:
                git_version = f'{git_version}.dev{commit}'
            return git_version.rstrip()
    except CalledProcessError:
        pass

    return '0.0.0'


def _get_long_description() -> str:
    with open('README.md', encoding='utf-8') as readme:
        return readme.read()


setup(
    name='py-graphql-codegen',
    version=_get_git_version(),
    description='Code generation from GraphQL schema & operations.',
    long_description=_get_long_description(),
    long_description_content_type="text/markdown",
    license='WTFPL',
    url='https://gitea.dont-nod.com/gdaow/py-graphql-codegen',
    author='Corentin Séchet',
    author_email='gdaow@users.noreply.github.com',
    packages=list(_find_packages('graphql_codegen')),
    entry_points={
        'console_scripts': [
            'graphql-codegen = graphql_codegen.main:main'
        ],
    },
    # See list at https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',

        'Operating System :: OS Independent',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Environment :: Web Environment',
    ],
    keywords=['GraphQL', 'Web'],
    include_package_data=True,
    package_data={'py-graphql-codegen': ['templates/**/*']},
    install_requires=[
        'graphql-core',
        'mako'
    ],
    zip_safe=False,
)
