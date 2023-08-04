// Set scale -- make pixelDensity a commandline arg or something
pixelDensity = 1200
pixelWidth = getWidth()
umInAnInch = 25400
knownDistance = round(pixelWidth / pixelDensity * umInAnInch)
run("Set Scale...", "distance=pixelWidth known=knownDistance unit=microns");

// Subtract background from image stack
run("Subtract Background...", "rolling=10 light stack");

// Generate a binary image from our image stack
setThreshold(0, 240);
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes", "stack");
saveAs("tif", "../binary_" + getTitle());

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's stack redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay display exclude include add stack");
roiManager("Show None");
saveAs("Results", "../results_" + File.getNameWithoutExtension(getTitle()) + ".csv");
