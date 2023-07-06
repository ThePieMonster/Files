# Select a single or multiple layers and then run this script
layers = iface.layerTreeView().selectedLayers()
for layer in layers:
    layer.renderer().symbol().setWidth(1.00)
    layer.triggerRepaint()
    iface.layerTreeView().refreshLayerSymbology(layer.id())
