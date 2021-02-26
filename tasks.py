from invoke import Collection, task

import config
import task.macav2 as macav2
import task.ncproj as ncproj
import task.region as region

@task(macav2.build)
def build(context):
    """
    Execute all build tasks
    """

    print("Hello Build!")

@task(macav2.clean, region.clean)
def clean(context):
    """
    Execute all clean tasks
    """

    print("Hello Clean!")

@task(ncproj.compile)
def compile(context):
    """
    Execute all compile tasks
    """

    print("Hello Compile!")

@task(region.stage)
def stage(context):
    """
    Execute all stage tasks
    """

    print("Hello Stage!")

namespace = Collection(build, clean, compile, stage)
namespace.add_collection(macav2.namespace)
namespace.add_collection(ncproj.namespace)
namespace.add_collection(region.namespace)
