import os
import os.path as osp

from renderer.BlenderRenderer import Renderer

import numpy as np
import copy
import startup
from Pose import Pose
import numpy as np
import math

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

import cPickle as pickle
import errno

class ShapenetRenderer():
    def __init__(self, numPoses=10, imX=224, imY=224):
        print 'Init:'
        self.numPoses = numPoses
        self.imX = imX
        self.imY = imY
        self._initModelInfo()
        self.renderer = Renderer([self.synsetModels[0][0]])

    def renderAllSynsets(self):
        for sId,synset in enumerate(self.synsets):

            print( "\nprocessing category %d / %d: %s" % ( sId, len( self.synsets ), synset ) )
            for mId in range(len(self.synsetModels[sId])):
            #for mId in range(10):
                mName = self._loadNewModel(sId, mId)
                print( "processing model %d / %d: %s" % ( mId, len(self.synsetModels[sId]), mName ) )

                renderDir = osp.join(self.config['renderPrecomputeDir'], synset, mName)
                mkdir_p(renderDir)
                poseSamples = self._randomPoseSamples()

                infoFile = osp.join(renderDir,'poseInfo.pickle')
                with open(infoFile, 'w') as f:
                    pickle.dump([poseSamples], f)
                self.renderer.renderViews(poseSamples, renderDir)

    def _loadNewModel(self, synsetId, modelId):
        mPath = self.synsetModels[synsetId][modelId]
        mName = (mPath.split('/'))[-2]
        self.renderer.reInit([mPath])
        return mName

    def _randomPoseSamples(self):
        poseSamples = []
        for n in range(self.numPoses):
            poseSamples.append(Pose({'rot':[np.random.randint(-180,180),np.random.randint(-20,40),0]}))
        return poseSamples

    def _initModelInfo(self):
        self.config = startup.params()
        self.synsets = [ '03001627' ]
        # self.synsets = ['03001627','02691156','02958343']
        self.synsetModels = [[osp.join(self.config['shapenetDir'],s,f,'model.obj') for f in os.listdir(osp.join(self.config['shapenetDir'],s)) if len(f) > 3] for s in self.synsets]
        print( "config:" )
        print( "config['basedir']  = %s" % ( self.config['basedir']  ) )
        print( "config['shapenetDir']  = %s" % ( self.config['shapenetDir']  ) )
        print( "config['renderPrecomputeDir']  = %s" % ( self.config['renderPrecomputeDir']  ) )
        print( "synsets:" )
        print self.synsets
        print( "synsetModels: parsed %d models for category 0" % ( len( self.synsetModels[0] ) ) ) # hardcode 0


if __name__ == '__main__':
    print 'Init:'
    rnd = ShapenetRenderer()
    rnd.renderAllSynsets()