
# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
from os import environ
from github import Github, UnknownObjectException, InputGitAuthor
from urllib3 import disable_warnings


github_token    = environ.get('GITHUB_TOKEN', '')
github_name     = environ.get('GITHUB_NAME', '')
github_email    = environ.get('GITHUB_EMAIL', '')

disable_warnings()

author = InputGitAuthor(
    name=github_name,
    email=github_email
)


# Repo
def connectto_repo(organization=None,
                   repository_name=None,
                   private=False):
    """
    Establish connection with a repository.
    Return 'None' if connection fails.
    """
    gh = Github(github_token, verify=False)
    if organization:
        org = gh.get_organization(organization)
        try:
            repo = org.get_repo(f'{repository_name}')
        except UnknownObjectException:
            # print('Can not connect YOU to this repo in this organization')
            repo = None
        return repo
    else:
        user = gh.get_user()
        try:
            repo = user.get_repo(repository_name)
        except UnknownObjectException:
            # print('Can not connect YOU to this repo')
            repo = None
        return repo


def read_file(repository,
              file_path):
    """ Read a file in a repository
        file_path: path to the file formatted as
        'directory_in_repo/subdirectory/file.ext'
    """
    try:
        # Get the file if it exists
        ingested_file = repository.get_contents(file_path)
        content = ingested_file.decoded_content.decode("utf-8")

    except UnknownObjectException:
        # The file doesn't exist
        # print('The file does not exist')
        content = ''

    return content


def creupdate_file(repository,
                   file_path,
                   file_content,
                   branch='main'):
    """ Create or update a file in a repository
        file_path: path to the file formatted as
    """
    try:
        # Get the file if it exists
        file = repository.get_contents(file_path)

        # Update the file content
        repository.update_file(
            path=file.path,
            message='Dialogue with AI',
            content=file_content,
            sha=file.sha,
            branch=branch,
            committer=author,
            author=author
        )

    except UnknownObjectException:
        # Create a new file if it doesn't exist
        repository.create_file(
            path=file_path,
            message='Dialogue',
            content=file_content,
            branch=branch,
            committer=author,
            author=author,
        )
    return True


if __name__ == "__main__":
    """ Simple debug example 
    """
    example_md_file = """# Topic: Can human nature be changed?
\n\n<b>Alex:</b> Can human nature be changed?<br>
\n><b>Machina:</b> Yes.<br>
\n<b>Alex:</b> How can it be done?<br>
\n><b>Machina:</b> I don't know.<br>"""

    organization = 'great-ideas'

    repository_object = connectto_repo(repository_name='dialogue',
                                       private=False)

    try:
        result = creupdate_file(repository=repository_object,
                                file_path='./README.md',
                                file_content=example_md_file,
                                branch='second')
    except Exception as e:
        print('failed ', e)

    try:
        file = read_file(repository=repository_object,
                         file_path='./README.md')

    except UnknownObjectException:
        print('No such file')

    print('ok')