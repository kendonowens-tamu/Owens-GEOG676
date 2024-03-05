import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [GarageBuffer]


class GarageBuffer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Garage Buffer"
        self.description = "Determines which buildings on the A&M Campus are within a certain distance of a parking garage"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="Buffer Distance (m)",
            name="bufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="Structure Layer Name",
            name="structurename",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Geodatabase Name",
            name="gdbname",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage CSV Name",
            name="garagename",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="Output File Name",
            name="fileoutput",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Workspace Folder",
            name="workspace",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param6 = arcpy.Parameter(
            displayName="Strcuture GDB",
            name="StructureGDB",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        params = [param0,param1,param2,param3,param4,param5,param6]
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
        arcpy.env.workspace = parameters[5].valueAsText
        folder_path = parameters[5].valueAsText
        GDB = folder_path+'\\'+parameters[2].valueAsText
        buildings = GDB+'\\'+parameters[1].valueAsText
        user_input = int(parameters[0].value)
        garage_buffer = GDB + parameters[4].valueAsText
        arcpy.CreateFileGDB_management(folder_path, parameters[2].valueAsText)

        garages = arcpy.management.MakeXYEventLayer(parameters[3].valueAsText,"X","Y","garages")
        input_layers = [parameters[6].valueAsText+'\\'+parameters[1].valueAsText, garages]
        arcpy.FeatureClassToGeodatabase_conversion(input_layers, GDB)
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garages,GDB+'\Garage_Points_Projection',spatial_ref)

        arcpy.Buffer_analysis(GDB + "/Garage_Points_Projection", garage_buffer, user_input+" Meters")
        arcpy.Intersect_analysis([garage_buffer, buildings], GDB + "/Intersect", "ALL")
        arcpy.TableToTable_conversion(GDB+"/Intersect",GDB,parameters[4].valueAsText+".csv")
        
        return