import os

def task_compile_ncproj():
    ncproj_dir = os.getenv('ETL_BUILD_DIR') + '/ncproj'

    return {
        'file_dep' : [],
        'actions' : [
            # create impl directory
            '[ -d "impl" ] || mkdir ' + os.getenv('ETL_BUILD_DIR'),
            # clone ncproj git repository
            'git clone https://github.com/hamersaw/ncproj '
                + ncproj_dir + ' >> %(targets)s',
            # build project
            '(cd ' + ncproj_dir + '; ./gradlew build) >> %(targets)s',
            # flag target complete
            'echo "completed: $(date)" >> %(targets)s'],
        'targets' : ['logs/compile.ncproj'],
        'clean' : True
    }
