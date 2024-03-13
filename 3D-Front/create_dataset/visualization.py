import trescope
from trescope import Trescope
from trescope.config import FRONT3DConfig, Scatter2DConfig
from trescope import *
from trescope.toolbox import *

Trescope().initialize(True, simpleDisplayOutputs(1, 1))
# Trescope().selectOutput(1).plotScatter2D(
#     [1, 2, 3],
#     [1, 1, 1],
# ).withConfig(Scatter2DConfig().name('plotScatter2D').color(0xffff0000).size(1))
Trescope().selectOutput(0).plotFRONT3D('/home/rso/codes/CAD_Merge_NeRF/3D-Front/data/3D-FRONT/0a482eb4-e8fa-4b44-90d0-3623e0a60c71.json').withConfig(
FRONT3DConfig()
    .view('top')
    .renderType('color')
    .shapeLocalSource('/home/rso/codes/CAD_Merge_NeRF/3D-Front/data/3D-FUTURE-model')
    .hiddenMeshes(['Ceiling', 'SlabTop', 'ExtrusionCustomizedCeilingModel']))
# Trescope().selectOutput(0).plotFRONT3D('/home/rso/codes/CAD_Merge_NeRF/3D-Front/data/3D-FRONT/0a9f5311-49e1-414c-ba7b-b42a171459a3.json').withConfig(
# FRONT3DConfig()
#     .view('top')
#     .renderType('color')
#     .shapeLocalSource('/home/rso/codes/CAD_Merge_NeRF/3D-Front/data/3D-FUTURE-model')
#     .hiddenMeshes(['Ceiling', 'SlabTop', 'ExtrusionCustomizedCeilingModel']))