"""
Computes animation values relative to a master step value. This is done by
evaluating the domain defined by ValueStart and ValueEnd between the frame/step
values defined by AnimationStart and AnimationEnd. 
    Inputs:
        ValueStart: The start of the value domain
        ValueEnd: The end of the value domain
        Frame: The master frame/step value from the master animation
               slider.
        AnimationStart: The frame/step value at which the evaluation begins.
        AnimationEnd: The frame/step value at which the evaluation ends.
    Output:
        Value: The animation value computed by evaluating the domain between
               start and end of the animation using the position of the
               step/frame value.
    Remarks:
        Author: Max Eschenbach
        License: MIT License
        Version: 200702
"""

# GHPYTHON STANDARD LIBRARY IMPORTS
from __future__ import division

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "SimpleAnimationValues"
ghenv.Component.NickName ="SAV"
ghenv.Component.Category = "GhPyAnimation"
ghenv.Component.SubCategory = "02 Animation Values"

class SimpleAnimationValues(component):
    
    def remap_number(self, start, end, tstart, tend, val):
        #range check
        if start == end:
            return start
        if tstart == tend:
            return tstart
        remapped_number = ((val-start) * (tend-tstart) / (end-start)) + tstart
        return remapped_number
    
    def RunScript(self, ValueStart, ValueEnd, Frame, AnimationStart, AnimationEnd):
        
        # set defaults
        if ValueStart == None:
            ValueStart = 0.0
        if ValueEnd == None:
            ValueEnd = 1.0
        if AnimationStart == None:
            AnimationStart = 0
        if AnimationEnd == None:
            AnimationEnd = 30
        
        # initialize output so it's never empty
        Value = Grasshopper.DataTree[object]()
        
        # only do sth if frame value exists
        if Frame != None:
            if Frame < AnimationStart:
                Value = ValueStart
            if (Frame >= AnimationStart) and (Frame < AnimationEnd):
                Value = self.remap_number(AnimationStart,
                                          AnimationEnd,
                                          ValueStart,
                                          ValueEnd,
                                          Frame)
            elif Frame >= AnimationEnd:
                Value = ValueEnd
        else:
            rml = self.RuntimeMessageLevel.Warning
            self.AddRuntimeMessage(rml,
                        "Input parameter Frame failed to collect data")
        
        # return outputs if you have them; here I try it for you:
        return Value
