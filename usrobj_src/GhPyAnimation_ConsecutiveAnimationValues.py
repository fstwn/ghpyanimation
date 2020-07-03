"""
Computes animation values relative to a primary step value. This is done by
interpolating between the given stop values using the amount of frames defined
by AnimationStart and AnimationEnd.
    Inputs:
        ValueStops: The stop values to interpolate between.
                    {list, float}
        Frame: The frame/step value from the primary animation slider.
               {item, int}
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
ghenv.Component.Name = "ConsecutiveAnimationValues"
ghenv.Component.NickName ="CAV"
ghenv.Component.Category = "GhPyAnimation"
ghenv.Component.SubCategory = "02 Animation Values"

class ConsecutiveAnimationValues(component):
    
    def slice_sequence(self, seq, numslices):
        n = min(numslices, len(seq))
        k, m = divmod(len(seq), numslices)
        return (seq[i * k + min(i, m):(i + 1) * k + min(i + 1, m)]
                for i in range(numslices))
    
    def remap_number(self, start, end, tstart, tend, val):
        #range check
        if start == end:
            return start
        if tstart == tend:
            return tstart
        remapped_number = ((val-start) * (tend-tstart) / (end-start)) + tstart
        return remapped_number
    
    def RunScript(self, ValueStops, Frame, AnimationStart, AnimationEnd):
        
        # initialize output so it's never empty
        Value = Grasshopper.DataTree[object]()
        
        # set defaults
        if ValueStops == None:
            ValueStops = [0, 1]
        if AnimationStart == None:
            AnimationStart = 0
        if AnimationEnd == None:
            AnimationEnd = 30
        if AnimationEnd <= AnimationStart:
            rml = self.RuntimeMessageLevel.Warning
            err = ("Slider animations cannot run in reverse. AnimationEnd has "
                   "to be larger than AnimationStart!")
            self.AddRuntimeMessage(rml, err)
                        
            return Value
        
        # only do sth if frame value exists
        if Frame != None:
            
            frame_sequence = range(AnimationStart, AnimationEnd+1)
            if len(frame_sequence) < len(ValueStops):
                rml = self.RuntimeMessageLevel.Warning
                self.AddRuntimeMessage(rml,
                    "Number of ValueStops cannot exceed number of frames!")
                return Value
            
            if Frame < AnimationStart:
                Value = ValueStops[0]
            if (Frame >= AnimationStart) and (Frame < AnimationEnd):
                chunks = list(self.slice_sequence(frame_sequence, len(ValueStops)-1))
                for i, chunk in enumerate(chunks):
                    if not Frame in chunk:
                        continue
                    if i < len(ValueStops)-1:
                        j = i+1
                    else:
                        j = -1
                    Value = self.remap_number(chunk[0],
                                              chunk[-1],
                                              ValueStops[i],
                                              ValueStops[j],
                                              Frame)
                
            elif Frame >= AnimationEnd:
                Value = ValueStops[-1]
        else:
            rml = self.RuntimeMessageLevel.Warning
            self.AddRuntimeMessage(rml,
                        "Input parameter Frame failed to collect data")
        
        # return outputs if you have them; here I try it for you:
        return Value
