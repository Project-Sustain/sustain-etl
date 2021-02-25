def task_build_all():
    return {
        'file_dep' : [],
        'actions' : ['echo "completed: $(date)" >> %(targets)s'],
        'targets' : ['logs/build.all'],
        'clean' : True
    }

def task_compile_all():
    return {
        'file_dep' : ['logs/compile.ncproj'],
        'actions' : ['echo "completed: $(date)" >> %(targets)s'],
        'targets' : ['logs/compile.all'],
        'clean' : True
    }

def task_stage_all():
    return {
        'file_dep' : ['logs/stage.region'],
        'actions' : ['echo "completed: $(date)" >> %(targets)s'],
        'targets' : ['logs/stage.all'],
        'clean' : True
    }
