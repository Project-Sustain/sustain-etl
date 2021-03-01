from invoke import Collection, task

import os

"""
configuration values
"""
region_dir = 'region'

county_shapefile = os.getenv('SUSTAIN_DATA_DIR') \
    + '/' + region_dir + '/tl_2010_us_county10.shp'
county_json_file = county_shapefile + '.json'
county_formatted_file = county_json_file + '.formatted'

state_shapefile = os.getenv('SUSTAIN_DATA_DIR') \
    + '/' + region_dir + '/tl_2010_us_state10.shp'
state_json_file = state_shapefile + '.json'
state_formatted_file = state_json_file + '.formatted'

mongo_binary = os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongo'
mongoimport_binary = \
    os.getenv('SUSTAIN_MONGODB_BIN_DIR') + '/mongoimport'

@task
def clean_county(context):
    """
    Delete cached county data
    """

    print("[-] deleting cached files")
    context.run('rm ' + county_json_file + ' ' + county_formatted_file)

@task
def stage_county(context):
    """
    Stage county data
    """

    # unpack shapefile
    if os.path.isfile(county_json_file):
        print('[|] json file "' + county_json_file \
            + '" already exists')
    else:
        print("[+] unpacking shapefile")
        context.run('ogr2ogr -f geoJSON ' + county_json_file \
            + ' ' + county_shapefile)

    # format json
    if os.path.isfile(county_formatted_file):
        print('[|] formatted json file "' + county_formatted_file \
            + '" already exists')
    else:
        print("[+] formatting json")
        jq_format_string = '''.features[] 
            | { 
                gis_join: ("G" + .properties.STATEFP10 + "0"
                    + .properties.COUNTYFP10 + "0"),
                name: .properties.NAME10,
                geometry: .geometry
            }'''

        context.run('cat ' + county_json_file + ' | jq \''
            + jq_format_string + '\' > ' + county_formatted_file)

    # mongo import
    print("[+] importing mongodb collection")
    context.run(mongoimport_binary
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
        + ' --collection=region_county --type=json '
        + county_formatted_file)

    # create 2dsphere index
    print("[+] creating mongodb spatial index")
    context.run(mongo_binary + ' '
        + os.getenv('SUSTAIN_MONGODB_DATABASE') 
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --eval "db.region_county.createIndex({geometry:\\\"2dsphere\\\"})"')

county_namespace = Collection('county')
county_namespace.add_task(clean_county, name = 'clean')
county_namespace.add_task(stage_county, name = 'stage')

@task
def clean_state(context):
    """
    Delete cached state data
    """

    print("[-] deleting cached files")
    context.run('rm ' + state_json_file + ' ' + state_formatted_file)

@task
def stage_state(context):
    """
    Stage state data
    """

    # unpack shapefile
    if os.path.isfile(state_json_file):
        print('[|] json file "' + county_json_file \
            + '" already exists')
    else:
        print("[+] unpacking shapefile")
        context.run('ogr2ogr -f geoJSON ' + state_json_file \
            + ' ' + state_shapefile)

    # format json
    if os.path.isfile(state_formatted_file):
        print('[|] formatted json file "' + state_formatted_file \
            + '" already exists')
    else:
        print("[+] formatting json")
        jq_format_string = '''.features[] 
            | { 
                gis_join: ("G" + .properties.STATEFP10 + "0"),
                name: .properties.NAME10,
                geometry: .geometry
            }'''

        context.run('cat ' + state_json_file + ' | jq \''
            + jq_format_string + '\' > ' + state_formatted_file)

    # mongo import
    print("[+] importing mongodb collection")
    context.run(mongoimport_binary
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
        + ' --collection=region_state --type=json '
        + state_formatted_file)

    # create 2dsphere index
    print("[+] creating mongodb spatial index")
    context.run(mongo_binary + ' ' 
        + os.getenv('SUSTAIN_MONGODB_DATABASE') 
        + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
        + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
        + ' --eval "db.region_state.createIndex({geometry:\\\"2dsphere\\\"})"')

state_namespace = Collection('state')
state_namespace.add_task(clean_state, name = 'clean')
state_namespace.add_task(stage_state, name = 'stage')

@task(clean_county, clean_state)
def clean(context):
    """
    Clean region data
    """

@task(stage_county, stage_state)
def stage(context):
    """
    Stage region data
    """

namespace = Collection('region', clean, stage)
namespace.add_collection(county_namespace)
namespace.add_collection(state_namespace)
