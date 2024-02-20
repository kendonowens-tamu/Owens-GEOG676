import arcpy
arcpy.env.workspace = "C:/Users/kendo/Documents/ArcPy"
folder_path = "C:/Users/kendo/Documents/ArcPy"
arcpy.CreateFileGDB_management(folder_path, "CampusGarages.gdb")

garages = arcpy.management.MakeXYEventLayer("Data/garages.csv","X","Y","garages")
input_layers = ["Campus.gdb/Structures", garages]
arcpy.FeatureClassToGeodatabase_conversion(input_layers, "C:/Users/kendo/Documents/ArcPy/CampusGarages.gdb")
GDB = "C:/Users/kendo/Documents/ArcPy/CampusGarages.gdb"
buildings = GDB+'\\'+'Structures'
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garages,GDB+'\Garage_Points_Projection',spatial_ref)

user_input = input("Please input the buffer radius in meters: ")
arcpy.Buffer_analysis(GDB + "/Garage_Points_Projection", GDB + "/garage_buffer", user_input+" Meters")
arcpy.Intersect_analysis([GDB + "/garage_buffer", GDB + "/Structures"], GDB + "/Intersect", "ALL")
arcpy.TableToTable_conversion(GDB+"/Intersect",GDB,"nearbyBuildings.csv")
print("Finished")