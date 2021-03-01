from invoke import Collection, task

import task.ncproj as ncproj
import task.region as region

@task(ncproj.compile)
def build(context):
    """
    Build macav2 data
    """

    print("hello macav2 build!")

@task()
def clean(context):
    """
    Delete cached macav2 data
    """

    print("hello macav2 build!")

namespace = Collection('macav2', build, clean)
