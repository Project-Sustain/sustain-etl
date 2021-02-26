from invoke import Collection, task

@task
def update(context):
    print("Hello ncproj Update!")

@task(update)
def compile(context):
    print("Hello ncproj Compile!")

namespace = Collection('ncproj', compile)
