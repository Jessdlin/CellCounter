import numpy as np
from scipy.signal import correlate2d
import scipy.ndimage as ndi
import skimage.measure as skm
from skimage import morphology
# from skimage.io import imsave
from skimage.external.tifffile import imsave, TiffFile
import cv2
import warnings
import datetime
import matplotlib.pyplot as plt
from math import pi, sqrt


def findCells(img, size, variance, minSize, maxSize, threshold=.125):
    # Add noise to blank pixels
    img_w_noise = addHorizontalNoise(img)

    # create gaussian image cell template
    var = variance
    low = -(size - 0.5)
    high = size + 0.5
    X, Y = np.meshgrid(np.arange(low, high), np.arange(low, high))
    temp = np.exp(-.5 * ((X ** 2 + Y ** 2) / var))

    # correlate with image
    xc = correlate2d(img_w_noise, temp - temp.mean(), 'same')
    # threshold
    cells = xc > xc.max() * threshold
    cells2 = morphology.remove_small_objects(cells, min_size=minSize, connectivity=2)
    cells2 = cells2.astype(np.uint8)
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(cells2, connectivity=8)
    sizes = stats[1:, -1];
    nb_components = nb_components - 1
    cells3 = np.zeros((output.shape))
    for i in range(0, nb_components):
        if sizes[i] <= maxSize:
            cells3[output == i + 1] = 255

    cells3 = cells3.astype(np.uint8)
    #cells3[:20, :] = 0
   # cells3[:, :20] = 0
  #  cells3[-20:, :] = 0
  #  cells3[:, -20:] = 0
    #print(cells3.shape)
    return cells3

def findCellsPixelValue(labels, areaThreshold, img, l=None):
    label_img = labels.T #labeled binary image

    label_img[label_img == 255] = 1 #convert to 1 so can multiply
    original_img = img #original color channel image
    x = original_img.shape[0] #width
    y = original_img.shape[1] #height
    X, Y = np.ogrid[:x, :y] #creating an indexed grid same dim as original image

    area = areaThreshold/0.4 #recreating average cell size from earlier
    radius = sqrt(area/pi) #finding radius
    cell_img = label_img * original_img #get rid of background -- only keep cells
    cell_img2 = cell_img.astype(np.uint8) #convert to uint8 because this is what next step requires
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(cell_img2, connectivity=8) #get centroids

    expressionLevelArray = []
    prevLayerVal = 0
    layerNum = 1

    currentCell = []
    layerExpressionLevelArray = []

    if l is None:
        layerValues = [x]
    else:
        layerValues = l.copy()
        layerValues.append(x)
    print(layerValues)
    for layer in layerValues:
        for index, center in enumerate(centroids[1:]): #go through each centroid
            dist_from_center = np.sqrt((X - center[1]) ** 2 + (Y - center[0]) ** 2) #calculating distances from centroid across ogrid
            mask = dist_from_center <= radius #keeping cell values that are acceptable

            masked_img = cell_img.copy() #copy original image
            masked_img[~mask] = 0 #apply mask

            masked_img[masked_img == 0] = 'nan'
            cellExpressionLevel = np.nanmean(masked_img)
            expressionLevelArray.append(cellExpressionLevel)

            if prevLayerVal <= center[1] < layer:
                currentCell.append(cellExpressionLevel)
                currentCell.append(layerNum)
                layerExpressionLevelArray.append(currentCell)
                currentCell = []

        layerNum += 1
        prevLayerVal = layer

    expressionLevelAvg = np.mean(expressionLevelArray)

    return expressionLevelAvg, layerExpressionLevelArray

def countCells(bin_img, channelType, thresholds, l=None):
    layerNums = []  # cell count per layer array
    layerCount = 0  # cell count for current layer
    # print(len(l))

    y = 0
    x = 0
    height = bin_img.shape[1]
    # print(len(layerValues))

    if l is None:
        layerValues = [height]
    else:
        layerValues = l.copy() # where the layers are
        layerValues.append(height)

    #if layerValues is None:
    #    layerValues = [height]
    #else:
    #    layerValues.append(height)

    labels = skm.label(bin_img)
    stats = skm.regionprops(labels)
    prevLayerVal = 0
    areaThreshold = np.mean(thresholds)

    for layer in layerValues:
        # print(str(prevLayerVal)+"<"+str(layer))
        for prop in stats:
            x, y = prop.centroid
            if prevLayerVal <= y < layer:
                if prop.area >= areaThreshold:
                    layerCount += 1
        # print(layerCount)
        layerNums.append(layerCount)
        layerCount = 0
        prevLayerVal = layer
    return layerNums

def processColoc(coloc, thresholds):
    areaThreshold = np.mean(thresholds)
    coloc_labels = coloc
    print(coloc_labels.shape)
    print(areaThreshold)
    print(type(coloc_labels))
    coloc2 = morphology.remove_small_objects(coloc_labels, min_size=areaThreshold, connectivity=2)
    imsave("blah", coloc2)
    print(type(coloc2))
    return coloc2

def addHorizontalNoise(image):
    image = image.astype(float)
    image_with_noise = image.copy()
    for i in range(image.shape[0]):
        zm = image[i, :] == 0
        if np.all(zm):
            continue
        image_with_noise[i, zm] = np.random.randn(np.sum(zm)) * np.std(image[i, ~zm]) + np.mean(image[i, ~zm])
        ones = np.where(zm == 0)[0]
        fo = ones.min()
        lo = ones.max()
        image_with_noise[i, 0:fo + 4] = ndi.filters.gaussian_filter1d(image_with_noise[i, 0:fo + 4], 4)
        image_with_noise[i, lo - 4:] = ndi.filters.gaussian_filter1d(image_with_noise[i, lo - 4:], 4)

    return image_with_noise


def addLayers(blue, numLayers):
    adder = 1 / (numLayers + 1)
    multiplier = 0
    layers = []
    for x in range(0, numLayers):
        multiplier += adder
        layer = int(multiplier * blue.shape[0])
        layers.append(layer)

    return layers


def saveImages(filename, channelLabels, channelNames, layerValues, thresholdValues, minValues, maxValues, tsValues,
               varValues):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
    now = datetime.datetime.now()
    for x in range(0, len(channelLabels)):
        imsave(filename + "_" + str(now.year) + "-" + str(now.month) +  "-" + str(now.day) + "-" + str(now.hour) + "," + str(now.minute) + "_" + channelNames[x] + ".tif", channelLabels[x].astype(np.uint8),
               metadata={"layers": layerValues, "thresholdValues": thresholdValues, "minValues": minValues,
                         "maxValues": maxValues, "tsValues": tsValues, "varValues": varValues})
