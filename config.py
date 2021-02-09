import os

# set data environment variables
os.environ['SUSTAIN_DATA_DIR'] = '/home/hamersaw/downloads/sustain-data'

# set mongodb environment variables
os.environ['SUSTAIN_MONGODB_BIN_DIR'] = '/home/hamersaw/development/tumen/bin'
os.environ['SUSTAIN_MONGODB_CONNECTION_STR'] = '127.0.0.1:27017'
os.environ['SUSTAIN_MONGODB_DATABASE'] = 'sustain_db'
