# Select a single or multiple layers and then run this script
print("Running Export Script")

path = "C:/Users/Admin/Downloads/"

layers = iface.layerTreeView().selectedLayers()
for layer in layers:
    layerName = layer.name()
    #pathToFile = path + layerName + ".gpx"
    file_path = os.path.join(path, f'{layer.name()}.gpx')
    #print(layerName)
    #error, error_string = QgsVectorFileWriter.writeAsVectorFormat(
    #    layer,
    #    pathToFile,
    #    "utf-8",
    #    QgsCoordinateReferenceSystem(4326),
    #    "GPX", 
    #    onlySelected=True,
    #    datasourceOptions=["GPX_USE_EXTENSIONS=ON"],
    #    layerOptions=["FORCE_GPX_ROUTE=NO"])

    writer = QgsVectorFileWriter(
        file_path, 
        'utf-8', 
        layer.fields(), 
        QgsWkbTypes.LineString, 
        QgsCoordinateReferenceSystem(4326),
        "GPX")
    for ft in layer.getFeatures():
        ok = writer.addFeature(ft)
        #print(ok)# Check that addFeature() operation returned True

    if(writer.NoError == QgsVectorFileWriter.NoError):
        print("GPX saved: " + str(layerName))
        qgis.utils.iface.messageBar().pushMessage("GPX saved: " + str(layerName), Qgis.Success)
    else:
        print("Error creating: " + str(layerName))
        qgis.utils.iface.messageBar().pushMessage("Error creating: " + str(layerName), Qgis.Critical)
    
    del writer

#if error == QgsVectorFileWriter.NoError:
#    qgis.utils.iface.messageBar().pushMessage("GPX saved", Qgis.Success)
#else:
#    print('Error: {details}'.format(details=error_string))
#    qgis.utils.iface.messageBar().pushMessage('Error creating GPX: {details}'.format(details=error_string), Qgis.Critical)
