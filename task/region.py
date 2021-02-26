from invoke import Collection, task

@task
def clean(context):
    print("Hello region Clean!")

@task
def stage(context):
    print("Hello region Build!")

namespace = Collection('region', clean, stage)
