"""
Set the camera of the active Rhino viewport.
    Inputs:
        Toggle: If True, camera control is activated.
                {item, bool}
        Location: The location of the camera.
                  {item, point3d}
        Target: The target for the camera (i.e. where the camera is looking at)
                {item, point3d}
        LensLength: The lenslength for the camera.
                    Defaults to 50.
                    {item, float}
        Remarks:
            Author: Max Eschenbach
            License: MIT License
            Version: 200703
"""

# GHPYTHON SDK IMPORTS
from ghpythonlib.componentbase import executingcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
import scriptcontext

# GHENV COMPONENT SETTINGS
ghenv.Component.Name = "SetActiveCamera"
ghenv.Component.NickName ="SAC"
ghenv.Component.Category = "GhPyAnimation"
ghenv.Component.SubCategory = "01 Camera"

class SetActiveCamera(component):
    
    def RunScript(self, Toggle, Location, Target, LensLength):
        
        if LensLength == None:
            LensLength = 50
        
        Camera = Grasshopper.DataTree[object]()
        
        if Location and Target and Toggle:
            av = scriptcontext.doc.Views.ActiveView
            vp = av.ActiveViewport
            
            vp.SetCameraLocation(Location, True)
            vp.SetCameraDirection(Target - Location, True);
            
            vp.Camera35mmLensLength = LensLength
        else:
            if not Location:
                rml = self.RuntimeMessageLevel.Warning
                self.AddRuntimeMessage(rml, 
                            "Input parameter Location failed to collect data")
            if not Target:
                rml = self.RuntimeMessageLevel.Warning
                self.AddRuntimeMessage(rml, 
                            "Input parameter Target failed to collect data")
        
        # return outputs if you have them; here I try it for you:
        return Camera
