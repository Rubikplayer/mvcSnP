import os
import os.path as osp
import sys

def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)
        print 'added {}'.format(path)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

add_path(os.getcwd())

def params():
    config = {}
    config['basedir'] = os.getcwd()
    config['shapenetDir'] = '/data1/shubhtuls/cachedir/Datasets/shapeNetCoreV1/'
    config['renderPrecomputeDir'] = osp.join(config['basedir'],'..','..','..','cachedir','blenderRenderPreprocess')
    mkdir_p( osp.join(config['basedir'],'..','..','..','cachedir') ) 
    mkdir_p( config['renderPrecomputeDir'] )
    print( 'params(): created dir: %s' % osp.join(config['basedir'],'..','..','..','cachedir') )
	print( 'params(): created dir: %s' % config['renderPrecomputeDir'] )
    return config
