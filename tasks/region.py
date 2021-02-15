import os

#jq_format_string = '''.features
#    | map ( 
#        { gis_join : 
#            ( "G" + .properties.STATEFP10 + "0" 
#                + .properties.COUNTYFP10 + "0" 
#            )
#        }
#        + ( .properties
#            | with_entries( .value = .value )
#            | with_entries( .key |= ascii_downcase )
#        )
#        + { geometry : .geometry }
#    )
#    | .[]'''

def task_stage_region():
    return {
        'file_dep' : ['logs/stage.region.county',
            'logs/stage.region.state'],
        'actions' : ['echo "complete" > %(targets)s'],
        'targets' : ['logs/stage.region'],
        'clean' : True
    }

def task_stage_region_county():
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

    # return task
    return {
        'file_dep' : [],
        'actions' : [
            # unpack shapefile
            'ogr2ogr -f geoJSON '+ json_file + ' ' + source_file,
            # format json
            'cat ' + json_file + ' | jq \'' + jq_format_string
                + '\' > ' + formatted_file, 
            # mongo import
            mongoimport_binary
                + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
                + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
                + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
                + ' --collection=region_county --type=json '
                + formatted_file + ' >> %(targets)s 2>&1',
            # create 2dsphere index
            mongo_binary + ' ' + os.getenv('SUSTAIN_MONGODB_DATABASE') 
                + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
                + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
                + ' --eval "db.region_county.createIndex({geometry:\\\"2dsphere\\\"})"'
                +  ' >> %(targets)s 2>&1',
            # cleanup
            'rm ' + json_file + ' ' + formatted_file,
            # flag target complete
            'echo "completed: $(date)" > %(targets)s'],
        'targets' : ['logs/stage.region.county'],
        'uptodate' : [True],
        'clean' : True
    }

def task_stage_region_state():
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

    # return task
    return {
        'file_dep' : [],
        'actions' : [
            # unpack shapefile
            'ogr2ogr -f geoJSON '+ json_file + ' ' + source_file,
            # format json
            'cat ' + json_file + ' | jq \'' + jq_format_string
                + '\' > ' + formatted_file, 
            # mongo import
            mongoimport_binary
                + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
                + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
                + ' --db=' + os.getenv('SUSTAIN_MONGODB_DATABASE')
                + ' --collection=region_state --type=json '
                + formatted_file + ' >> %(targets)s 2>&1',
            # create 2dsphere index
            mongo_binary + ' ' + os.getenv('SUSTAIN_MONGODB_DATABASE') 
                + ' --host=' + os.getenv('SUSTAIN_MONGODB_HOST')
                + ' --port=' + os.getenv('SUSTAIN_MONGODB_PORT')
                + ' --eval "db.region_state.createIndex({geometry:\\\"2dsphere\\\"})"'
                +  ' >> %(targets)s 2>&1',
            # cleanup
            'rm ' + json_file + ' ' + formatted_file,
            # flag target complete
            'echo "completed: $(date)" >> %(targets)s'],
        'targets' : ['logs/stage.region.state'],
        'uptodate' : [True],
        'clean' : True
    }
