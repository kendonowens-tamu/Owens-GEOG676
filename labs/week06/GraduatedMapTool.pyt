import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GraduatedMap"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Graduated Colors"
        self.description = "Create a Graduated Colored Map based on a specific attribute of a layer"
        self.canRunInBackground = False
        self.category = "MapTools"

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project Name",
            name="aprxInputName",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Layer to Classify",
            name="LayerToClassify",
            datatype="GPLayer",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Attribute Input Name",
            name="AttributeInput",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",
            datatype="DEFolder",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutputProjectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0,param1,param2,param3,param4]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        readTime = 3
        start = 0
        max = 100
        step = 33

        arcpy.SetProgressor("step","Validating Project File...",start,max,step)
        arcpy.AddMessage("Validating Project File...")

        project = arcpy.mp.ArcGISProject(parameters[0].valueAsText)

        campus = project.listMaps('Map')[0]

        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Finding your map layer...")
        arcpy.AddMessage('Finding your map layer...')

        for layer in campus.listLayers():
            if layer.isFeatureLayer:
                symbology = layer.symbology
                if hasattr(symbology,'renderer'):
                    if layer.name == parameters[1].valueAsText:
                        arcpy.SetProgressorPosition(start + step*2)
                        arcpy.SetProgressorLabel("Calculating and classifying...")
                        arcpy.AddMessage("Calculating and classifying...")

                        symbology.updateRenderer('GraduatedColorsRenderer') #Rendered updated to graduated
                        symbology.renderer.classificationField = parameters[2].valueAsText #field that the cloropleth is created from
                        symbology.renderer.breakCount = 5 #classes we'll have for the map
                        symbology.renderer.colorRamp = project.listColorRamps('Oranges (5 Classes)')[0]
                        layer.symbology = symbology

                        arcpy.AddMessage("Finishing Generating Layer...")
                    else:
                        print("No layers found")
                        arcpy.AddMessage("No Layers Found!")
        arcpy.SetProgressorPosition(start+step*3)
        arcpy.SetProgressorLabel("Saving...")
        arcpy.AddMessage("Saving...")

        project.saveACopy(parameters[3].valueAsText+"\\"+parameters[4].valueAsText+".aprx")
        return