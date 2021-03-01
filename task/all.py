from invoke import Collection, task

import task.macav2 as macav2
import task.ncproj as ncproj
import task.region as region

@task(macav2.build)
def build(context):
    """
    Execute all build tasks
    """

    print("hello build!")

@task(ncproj.compile)
def compile(context):
    """
    Execute all compile tasks
    """

    print("hello compile!")

@task(region.stage)
def stage(context):
    """
    Execute all stage tasks
    """

    print("hello stage!")

namespace = Collection('all', build, compile, stage)
