// Open image from arguments if available
var closeWindow = false;
if (lengthOf(getArgument()) > 0) {
	// Open the image
	open(getArgument());
	closeWindow = true;
}

// Set scale -- make pixelDensity a commandline arg or something
pixelDensity = 1200;
pixelWidth = getWidth();
umInAnInch = 25400;
knownDistance = pixelWidth / pixelDensity * umInAnInch;
run("Set Scale...", "distance=pixelWidth known=knownDistance unit=microns");

// Subtract background from image
run("Subtract Background...", "rolling=10 light");

// Generate a binary image from our image
setThreshold(0, 240);
setOption("BlackBackground", false);
run("Convert to Mask", "method=Default background=Light");
run("Fill Holes");
run("Watershed");
saveAs("tif", "spraycards/images/" + File.getNameWithoutExtension(getTitle()));

// Generate ROIs
run("Set Measurements...", "area centroid perimeter fit shape feret's redirect=None decimal=3");
run("Analyze Particles...", "circularity=0.00-1.00 show=Overlay display exclude include add");
roiManager("Show None");
saveAs("Results", "spraycards/results/Results_" + File.getNameWithoutExtension(getTitle()) + ".csv");

// Close ImageJ window when running in batches
if (closeWindow) {
	run("Quit");
}
