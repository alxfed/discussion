# -*- coding: utf-8 -*-
# Python

"""Copyright (c) Alexander Fedotov.
This source code is licensed under the license found in the
LICENSE file in the root directory of this source tree.
"""
import os
from . import githubapi
import yaml


DISCUSSION_ORGANIZATION_NAME = ''
PRIVATE_REPO_WITH_TEXT = 'discussion_private'

try:
    gh = githubapi.connectto_repo(organization=DISCUSSION_ORGANIZATION_NAME,
                                  repository_name=PRIVATE_REPO_WITH_TEXT,
                                  private=True)
    MACHINE_YAML = githubapi.read_file(repository=gh, file_path='discussion.yaml')

except Exception as e:
    machina_path = os.path.join(os.path.dirname(__file__), '../scene/discussion.yaml')
    with open(machina_path, 'r') as yaml_file:
        MACHINE_YAML = yaml_file.read()

MEMORY_MACHINE = yaml.load(MACHINE_YAML, Loader=yaml.FullLoader)
