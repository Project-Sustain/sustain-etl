from invoke import Collection, task

import os

@task
def stage_county(context):
    """
    Stage county data
    """

    # initialize instance variables
    source_file = os.getenv('SUSTAIN_DATA_DIR') \
        + '/region/tl_2010_us_county10.shp '
    json_file = os.getenv('SUSTAIN_DATA_DIR') + '/tmp/county.json'
    formatted_file = os.getenv('SUSTAIN_DATA_DIR') \
        + '/tmp/county-formatted.json'

    mongo_binary = os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongo'
    mongoimport_binary = \
        os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongoimport'

    jq_format_string = '''.features[] 
        | { 
            gis_join: ("G" + .properties.STATEFP10 + "0"
                + .properties.COUNTYFP10 + "0"),
            name: .properties.NAME10,
            geometry: .geometry
        }'''

    # unpack shapefile
    context.run('ogr2ogr -f geoJSON '+ json_file + ' ' + source_file)

    # format json
    context.run('cat ' + json_file + ' | jq \''
        + jq_format_string + '\' > ' + formatted_file)

    # mongo import
    context.run(mongoimport_binary
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
        + ' --collection=region_county --type=json '
        + formatted_file)

    # create 2dsphere index
    context.run(mongo_binary + ' '
        + os.getenv('SUSTAIN_MONGODB_DATABASE') 
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --eval "db.region_county.createIndex({geometry:\\\"2dsphere\\\"})"')

    # cleanup
    context.run('rm ' + json_file + ' ' + formatted_file)

county_namespace = Collection('county')
county_namespace.add_task(stage_county, name = 'stage')

@task
def stage_state(context):
    """
    Stage state data
    """

    # initialize instance variables
    source_file = os.getenv('SUSTAIN_DATA_DIR') \
        + '/region/tl_2010_us_state10.shp '
    json_file = os.getenv('SUSTAIN_DATA_DIR') + '/tmp/state.json'
    formatted_file = os.getenv('SUSTAIN_DATA_DIR') \
        + '/tmp/state-formatted.json'

    mongo_binary = os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongo'
    mongoimport_binary = \
        os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongoimport'

    jq_format_string = '''.features[] 
        | { 
            gis_join: ("G" + .properties.STATEFP10 + "0"),
            name: .properties.NAME10,
            geometry: .geometry
        }'''

    # unpack shapefile
    context.run('ogr2ogr -f geoJSON '+ json_file + ' ' + source_file)

    # format json
    context.run('cat ' + json_file + ' | jq \''
        + jq_format_string + '\' > ' + formatted_file)

    # mongo import
    context.run(mongoimport_binary
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
        + ' --collection=region_state --type=json '
        + formatted_file)

    # create 2dsphere index
    context.run(mongo_binary + ' ' 
        + os.getenv('SUSTAIN_MONGODB_DATABASE') 
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --eval "db.region_state.createIndex({geometry:\\\"2dsphere\\\"})"')

    # cleanup
    context.run('rm ' + json_file + ' ' + formatted_file)

state_namespace = Collection('state')
state_namespace.add_task(stage_state, name = 'stage')

@task(stage_county, stage_state)
def stage(context):
    """
    Stage region data
    """

namespace = Collection('region', stage)
namespace.add_collection(county_namespace)
namespace.add_collection(state_namespace)
