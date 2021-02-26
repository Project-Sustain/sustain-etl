from invoke import Collection, task

@task
def clean(context):
    print("Hello macav2 Clean!")

@task
def build(context):
    print("Hello macav2 Build!")

namespace = Collection('macav2', clean, build)
