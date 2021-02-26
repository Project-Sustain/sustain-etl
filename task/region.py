from invoke import Collection, task

@task
def stage_county(context):
    """
    Stage county data
    """

    print("hello county stage!")

county_namespace = Collection('county')
county_namespace.add_task(stage_county, name = 'stage')

@task
def stage_state(context):
    """
    Stage state data
    """

    print("hello state stage!")

state_namespace = Collection('state')
state_namespace.add_task(stage_state, name = 'stage')

@task
def clean(context):
    """
    Clean region data
    """

    print("hello region clean!")

@task(stage_county, stage_state)
def stage(context):
    """
    Stage region data
    """

    print("hello region stage!")

namespace = Collection('region', clean, stage)
namespace.add_collection(county_namespace)
namespace.add_collection(state_namespace)
