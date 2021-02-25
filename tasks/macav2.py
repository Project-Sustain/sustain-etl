#def task_build_macav2():
#    return {
#        'file_dep' : ['logs/stage.macav2'],
#        'actions' : ['echo "test" > %(targets)s'],
#        'targets' : ['logs/build.macav2'],
#        'clean' : True
#    }

def task_stage_macav2():
    return {
        'file_dep' : ['logs/compile.ncproj'],
        'actions' : ['echo "test" > %(targets)s'],
        'targets' : ['logs/stage.macav2'],
        'clean' : True
    }
