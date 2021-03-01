from invoke import Collection, task

import os

@task
def update(context):
    """
    Update the ncproj git repository
    """

    print("hello ncproj update")

@task(update)
def compile(context):
    """
    Compile the ncproj git repository
    """

    print("hello ncproj compile")

namespace = Collection('ncproj', update, compile)
