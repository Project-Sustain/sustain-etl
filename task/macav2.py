from invoke import Collection, task

import task.ncproj as ncproj
import task.region as region

@task(ncproj.compile, region.stage)
def build(context):
    """
    Build macav2 data
    """

    print("hello macav2 build!")

@task
def clean(context):
    """
    Clean macav2 data
    """

    print("hello macav2 clean!")

namespace = Collection('macav2', build, clean)
