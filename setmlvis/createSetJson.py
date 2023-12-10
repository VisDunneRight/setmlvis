import os
import itertools
import json
import time
from PIL import Image
from shapely.geometry import Polygon
from shapely.wkt import loads
from shapely import to_wkb
from shapely import from_wkb
from rtree import index
import multiprocessing as mp
import pprint as pp

DEBUG = False
FULLDEBUG = False


# input Folder Name
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


def createSetJson(
    *, folderName: str, objectClass: str, jsonName: str = None, setIou: float
) -> dict:
    """
    Create a JSON file that contains information about objects in a specified class, stored in a given folder.

    Parameters:
    folderName (str): The name of the folder where the data is stored.
    objectClass (str): The class of objects to be processed.
    jsonName (str): The name of the JSON file to be created.
    setIou (float): The Intersection over Union (IoU) threshold value used to determine whether two bounding boxes overlap.

    Returns:
    None
    """

    start = time.time()
    modelNames = getModelNames(folderName)
    emptyDictionary = createEmptyDictionary(modelNames)
    allFilesDictionary = parseInputFolder(folderName, objectClass, modelNames)
    diff = time.time()
    if DEBUG:
        print("GetModel, Empty, Parse:", diff - start, "s")

    imgGt = fillImageandGroundTruth(folderName, allFilesDictionary)
    imgGTMap = {}
    for i, item in enumerate(imgGt["imgs"]):
        imgGTMap[item["imgName"]] = i

    finalDictionary = fillDictionary(
        folderName,
        emptyDictionary,
        allFilesDictionary,
        imgGTMap,
        modelNames,
        setIou,
        objectClass,
    )
    finalTime = time.time()
    if DEBUG:
        print("finalDictionary:", finalTime - diff, "s")
    finalDictionaryWithMetadata = generateMetadata(
        folderName, finalDictionary, modelNames, setIou, imgGt
    )

    finalDictionaryWithMetadata = updateFalseNegativesInDictionary(
        finalDictionaryWithMetadata, folderName, modelNames, objectClass
    )

    if DEBUG:
        print("MetaDate:", time.time() - finalTime, "s")
    if jsonName != None:
        generateJson(finalDictionaryWithMetadata, jsonName)
    return finalDictionaryWithMetadata


def generateMetadata(folderName, dictionary, modelNames, setIOU, imgGt):
    """
    Adds metadata to a dictionary object.

    Parameters:
        dictionary (dict): A dictionary object to which metadata will be added.
        modelNames (list): A list of model names.
        setIOU (float): The IOU value used for the evaluation.

    Returns:
        dict: The dictionary object with metadata added.

    """
    newDict = {}
    newDict["meta"] = {
        "folderName": folderName + "images/",
        "modelNames": modelNames,
        "setIOU": setIOU,
    }
    newDict["models"] = dictionary
    newDict["ground_truth"] = imgGt["ground_truth"]
    newDict["imgs"] = imgGt["imgs"]
    return newDict


def read_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip().split() for line in lines]


def compare_ground_truth_model(ground_truth, model_predictions, object_class):
    false_negatives = []
    # Filter ground truth and predictions by the specified class
    filtered_gt = [gt for gt in ground_truth if gt[0] == object_class]
    filtered_mp = [mp for mp in model_predictions if mp[0] == object_class]

    for gt in filtered_gt:
        intersections = [getIntersection([gt, mp]) for mp in filtered_mp]
        # Check if there is no sufficient intersection with any prediction
        if not any(
            intersection.area / createPolygon(gt).area > 0.0
            for intersection in intersections
        ):
            false_negatives.append(gt)
    return false_negatives


def generateFalseNegatives(dictionary, folderName, modelNames, objectClass):
    ground_truth_path = os.path.join(folderName, "ground_truth")
    models_path = {model: os.path.join(folderName, model) for model in modelNames}

    false_negatives = {"FalseNegatives": {}}
    for model_name, model_path in models_path.items():
        false_negatives["FalseNegatives"][model_name] = []

        for img_id, filename in enumerate(sorted(os.listdir(ground_truth_path))):
            gt_file = os.path.join(ground_truth_path, filename)
            model_file = os.path.join(model_path, filename)

            ground_truth = read_file(gt_file)
            model_predictions = read_file(model_file)

            img_false_negatives = compare_ground_truth_model(
                ground_truth, model_predictions, objectClass
            )
            if img_false_negatives:
                false_negatives["FalseNegatives"][model_name].append(
                    {"imageId": img_id, "values": img_false_negatives}
                )
    dictionary["FalseNegatives"] = false_negatives
    return dictionary


def updateFalseNegativesInDictionary(
    existingDictionary, folderName, modelNames, objectClass
):
    # Generate the false negatives using the generateFalseNegatives function
    falseNegativesResults = generateFalseNegatives(
        existingDictionary, folderName, modelNames, objectClass
    )
    # Iterate through each model in the existing dictionary
    for model in existingDictionary.get("models", {}):
        modelFN = falseNegativesResults["FalseNegatives"].get(model.strip(","), [])

        # Iterate through each image detection for the model
        for detection in existingDictionary["models"][model]:
            imageId = detection.get("FN", {}).get("imageId", None)
            if imageId is not None:
                # Find matching false negatives for this image ID
                matchingFN = next(
                    (item for item in modelFN if item["imageId"] == imageId), None
                )
                if matchingFN:
                    # Update the FN field with the new false negatives
                    detection["FN"] = matchingFN

    return existingDictionary


def getModelNames(directory: str) -> list[str]:
    """
    Get the names of the prediction models stored in the specified directory.

    Parameters:
    directory (str): The name of the directory where the prediction models are stored.

    Returns:
    List[str]: A list of the names of the prediction models.
    """
    algorithms = []
    for folder in os.listdir(directory):
        if folder not in ["ground_truth", "images"]:
            algorithms.append(folder)
    return algorithms


def fillImageandGroundTruth(folderName, allFilesDictionary):
    imgGT = {"imgs": [], "ground_truth": []}
    idCount = 0

    for imgName, info in allFilesDictionary.items():
        im = Image.open(folderName + "images/" + imgName)
        img = {"imgName": imgName, "imgSize": im.size, "ground_truth": []}
        for gt in info["ground_truth"]:
            imgGT["ground_truth"].append(gt)
            img["ground_truth"].append(idCount)
            idCount += 1
        imgGT["imgs"].append(img)
    return imgGT


def createEmptyDictionary(modelNames: list[str]) -> dict[str, list[str]]:
    """
    Create an empty dictionary with keys formed by combinations of the specified model names.
    m1,m2,m3 == [m1, m2, m3, m1m2, m1m2, m2m3, m1m2m3]

    Parameters:
    modelNames (List[str]): A list of the names of the prediction models.

    Returns:
    Dict[str, List[str]]: An empty dictionary with keys formed by combinations of the model names.
    """
    newSetDict = {}

    for L in range(len(modelNames) + 1):
        for subset in itertools.combinations(modelNames, L):
            if len(subset) != 0:
                stringTotal = ""
                for s in subset:
                    stringTotal = stringTotal + s + ","
                newSetDict[stringTotal] = []
    return newSetDict


def parseInputFolder(
    folderName: str, objectClass: str, modelNames: list[str]
) -> dict[str, dict[str, list[list[str]]]]:
    """
    Parse the input folder and extract information about the objects in a specified class for each prediction model.

    Parameters:
    folderName (str): The name of the folder where the input data is stored.
    objectClass (str): The class of objects to be processed.
    modelNames (list[str]): A list of the names of the prediction models.

    Returns:
    dict[str, dict[str, list[list[str]]]]: A dictionary with information about the objects in the specified class for each prediction model.
    """
    imageDirectory = folderName + "images/"
    filterClass = objectClass

    allFilesDict = {}

    for filename in os.listdir(imageDirectory):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            imgName = filename[: filename.rfind(".")]
            fileTxt = filename[: filename.rfind(".")] + ".txt"
            fileDict = {}

            for folder in modelNames:
                fileDict[folder] = []

                with open(os.path.join(folderName + folder + "/", fileTxt)) as f:
                    lines = f.readlines()

                    for l in lines:
                        arrL = l.split()
                        if arrL[0] == filterClass:
                            fileDict[folder].append(l.split())

            fileDict["ground_truth"] = []
            with open(os.path.join(folderName + "ground_truth/", fileTxt)) as f:
                lines = f.readlines()
                for l in lines:
                    arrL = l.split()
                    if arrL[0] == filterClass:
                        fileDict["ground_truth"].append(l.split())

            allFilesDict[filename] = fileDict
    return allFilesDict


def initPool(folName, modNames, iout, filClass, imggt):
    global folderName
    global modelNames
    global iou
    global filterClass
    global imgGtMap

    folderName = folName
    modelNames = modNames
    iou = iout
    filterClass = filClass
    imgGtMap = imggt


def poolFillDict(item):
    [key, value] = item
    start = time.time()
    bigDict = getEachImageInformation(
        folderName, key, value, iou, modelNames, filterClass, imgGtMap
    )
    end = time.time()
    if DEBUG:
        print("Each", key, end - start)
    return bigDict


def fillDictionary(
    folderName,
    emptyDictionary,
    allFilesDictionary,
    imgGtMap,
    modelNames,
    iou,
    filterClass,
):
    """
    This function fills the empty dictionary with information about the bounding boxes for each image.

    Parameters:
        emptyDictionary (dict): An empty dictionary to be filled with information about the bounding boxes.
        allFilesDictionary (dict): A dictionary containing information about all the bounding boxes for all images.
        modelNames (list): A list of the names of the models used to generate the bounding boxes.
        iou (float): The IOU threshold for accepting a bounding box as a true positive.
        filterClass (str): The class of objects to be filtered.

    Returns:
        dict: A filled dictionary with information about the bounding boxes.

    The returned dictionary has the following structure:
        {
            "model1+model2+...+modelN": [
                {
                    "imgName": str,
                    "IOU": float,
                    "boxes": {
                        "model1": [list of bounding boxes],
                        ...,
                        "modelN": [list of bounding boxes]
                    },
                    "shape": [center x, center y, width, height],
                    "confidence": [list of confidences values],
                    "iouGT": float,
                    "gtShape": [class, x, y, width, height]
                },
                ...
            ],
            ...
            "FN": [list of false negatives]
        }
        where model1, model2, ..., modelN are the names of the models used to generate the bounding boxes.
    """

    idCounter = Counter()
    pool = mp.Pool(
        initializer=initPool,
        initargs=(folderName, modelNames, iou, filterClass, imgGtMap),
    )
    res = pool.map(poolFillDict, allFilesDictionary.items())
    for image in res:
        for key, value in image.items():
            for name, detect in value["detections"].items():
                detect["id"] = str(idCounter.count) + detect["id"]
                idCounter.increment()
            # value["id"] = str(idCounter.count) + value["id"]
            emptyDictionary[key].append(value)

    # idCounter = Counter()
    # for key, value in allFilesDictionary.items():
    #     start = time.time()
    #     bigDict = getEachImageInformation(
    #         folderName, key, value, iou, modelNames, filterClass, idCounter
    #     )
    #     for key, value in bigDict.items():
    #         emptyDictionary[key].append(value)
    #     end = time.time()
    #     if DEBUG:
    #         print("Each", key, end - start)
    return emptyDictionary


def getEachImageInformation(
    folderName, imageName, inp, iouAlgos, modelNames, filterClass, imgGtMap
):
    bigDict = {}
    dictionary = []
    removeItems = []
    previous_gt_shapes = set()

    ground_truth_boxes = {}
    for model_name in modelNames:
        ground_truth_boxes[model_name] = []

    used_gt_by_image = (
        {}
    )  # Initialize a dictionary to store used ground truth bounding boxes for each image
    count = 0
    count2 = 0
    for L in range(len(modelNames) + 1, -1, -1):
        reduceInput(removeItems, inp)
        count += 1
        for subset in itertools.combinations(modelNames, L):
            if len(subset) != 0:
                count2 += 1
                start = time.time()
                dictionary, falseNegatives, inp, previous_gt_shapes = getRealSets(
                    inp,
                    subset,
                    iouAlgos,
                    folderName,
                    imageName,
                    filterClass,
                    ground_truth_boxes,
                    previous_gt_shapes,
                    used_gt_by_image,
                    imgGtMap,
                )
                if FULLDEBUG:
                    print("\t subSet:", time.time() - start)
                stringTotal = ""
                for s in subset:
                    stringTotal = stringTotal + s + ","
                for key, dictionaryItem in dictionary.items():
                    for model_name, box in dictionaryItem["boxes"].items():
                        box_key = model_name
                        box_value = box
                        removeItems.append(box_value)
                        if "gtShape" in dictionaryItem:
                            ground_truth_boxes[model_name].append(
                                dictionaryItem["gtShape"]
                            )

                # Update the used_gt_by_image dictionary
                for model_name in subset:
                    for box in ground_truth_boxes[model_name]:
                        if imageName not in used_gt_by_image:
                            used_gt_by_image[imageName] = []
                        used_gt_by_image[imageName].append(box)

                bigDict[stringTotal] = {"detections": dictionary, "FN": {}}
    return bigDict


# commented
def getRealSets(
    inp,
    subset,
    iouAlgos,
    folderName,
    imageName,
    filterClass,
    ground_truth_boxes,
    previous_gt_shapes,
    used_gt_by_image,
    imgGtMap,
):
    """
    This function finds the intersection and union between sets of bounding boxes and returns a list of dictionaries containing information about the bounding boxes with the highest IOU.

    Parameters:
        inp (dict): A dictionary containing the ground truth bounding boxes and the input bounding boxes.
        subset (list): A list of lists containing the input bounding boxes.
        iouAlgos (float): The IOU threshold for accepting a bounding box as a true positive.
        imageName (str): The name of the image being processed.

    Returns:
        tuple: A tuple of two values:
            dictionary (list of dicts): A list of dictionaries containing information about the bounding boxes with the highest IOU.
            inp (dict): The input dictionary.
    """
    dictionary = {}
    arr = []
    grpMerch = []

    # Create a list of the input bounding boxes from the subset
    indexCount = 0
    grpCount = 0
    for s in subset:
        for obj in inp[s]:
            arr.append((indexCount, obj))
            indexCount += 1
            grpMerch.append(grpCount)
        grpCount += 1
    dictRank = []

    start = time.time()
    # Create RTree
    idx = index.Index()
    # populates Rtree with rectangle
    for dect in arr:
        idx.insert(
            dect[0],
            (
                float(dect[1][1]),
                float(dect[1][2]),
                float(dect[1][3]),
                float(dect[1][4]),
            ),
        )
    intVisited = {}
    uniVisited = {}
    # For each rectangle check the interactions and create
    for dect in arr:
        # Get the all rectangles that intersect
        res = list(
            idx.intersection(
                (
                    float(dect[1][1]),
                    float(dect[1][2]),
                    float(dect[1][3]),
                    float(dect[1][4]),
                )
            )
        )
        # Group the ids together
        grps = []
        for i in range(grpCount):
            grps.append([])
        for id in res:
            grps[grpMerch[id]].append(arr[id])
        # Skip if one of the grps are empty
        skip = False
        for setGrp in grps:
            if len(setGrp) == 0:
                skip = True
        if skip:
            continue
        # Create the combo and get IOU
        for x in itertools.product(*grps):
            intersection = getIntersectionVisit(x, intVisited)
            if intersection.area == 0:
                continue
            union = getUnionVisited(x, uniVisited)
            IOU = intersection.area / union.area
            resX = []
            for val in x:
                resX.append(val[1])
            tup = (IOU, resX)
            dictRank.append(tup)

    # [1,2,3],[4,5,6],[7,8,9,10] =>
    # [1,2],[4,5],[7,8] =>
    # [1,4,7],[1,4,8]
    #

    # # Old Version
    # for s in subset:
    #     arr.append(inp[s])

    # dictRank = []
    # # Calculate the IOU between each combination of input bounding boxes
    # for x in itertools.product(*arr):
    #     intersection = getIntersection(x)
    #     if intersection.area == 0:
    #         continue
    #     union = getUnion(x)
    #     IOU = intersection.area / union.area
    #     tup = (IOU, x)
    #     dictRank.append(tup)

    afterProduct = time.time()
    if FULLDEBUG:
        print("        Product Calculate:", round(afterProduct - start, 2))
    # Sort the list of IOU values in descending order
    sortedList = sorted(dictRank, key=lambda x: x[0], reverse=True)
    # print(len(sortedList))
    values_to_remove = []
    afterSort = time.time()
    # if FULLDEBUG:
    #    print("        sort:", round(afterSort - afterProduct, 2))

    # Keep only the bounding boxes with IOU values higher than the threshold
    count = 0
    for key, value in sortedList:
        if key != 0:
            if key >= iouAlgos:
                values_to_remove = value
                addList, sortedList = keepValues(sortedList, key, values_to_remove)

                if addList[0] != 0:
                    newDict = {}
                    newDict["imgId"] = imgGtMap[imageName]
                    newDict["id"] = "-" + imageName
                    newDict["IOU"] = key
                    newDict["tags"] = []
                    newDict["boxes"] = dict(zip(subset, value))
                    # im = Image.open(folderName + "images/" + imageName)
                    # newDict["imgSize"] = im.size
                    polygonShape = getIntersection(value)
                    newAreaCoords = list(polygonShape.exterior.coords)
                    x, y = list(zip(*newAreaCoords))

                    # Calculate the center, width, and height of the bounding box
                    xmin = min(x)
                    ymin = min(y)
                    xmax = max(x)
                    ymax = max(y)
                    shape = [xmin, ymin, xmax, ymax]
                    newDict["shape"] = [filterClass] + shape
                    confidenceArray = []
                    for v in value:
                        confidenceArray.append(v[-1])
                    newDict["confidence"] = confidenceArray
                    dictionary[str(count)] = newDict
                    count = count + 1
                    # dictionary.append(newDict)

    keepIOU = time.time()
    # if FULLDEBUG:
    #   print("        keepIOU:", round(keepIOU - afterSort, 2))
    gtArray = inp["ground_truth"]

    gtTest = []
    usedGT = []
    for model in subset:
        for boxes in ground_truth_boxes[model]:
            usedGT.append(boxes)

    unusedGTArray = [gt for gt in gtArray if gt not in usedGT]

    # Calculate the IOU between each ground truth bounding box and the input bounding
    for gt in unusedGTArray:
        for key, item in dictionary.items():
            dictItem = {}
            value = [gt, item["shape"]]

            intersection = getIntersection(value)

            union = getUnion(value)
            IOU = intersection.area / union.area
            dictItem["gtIOU"] = IOU
            dictItem["gtShape"] = gt
            dictItem["shape"] = item["shape"].copy()
            if IOU != 0.0:
                gtTest.append(dictItem)

    # Sort the list of ground truth bounding boxes based on their IOU values
    sortedGT = sorted(gtTest, key=lambda x: x["gtIOU"], reverse=True)

    # Filter out any duplicate ground truth bounding boxes
    valuesToRemove = []
    second_list = delete_list_items(sortedGT, valuesToRemove)

    filtered_list = []

    for item in second_list:
        if item["gtShape"] in unusedGTArray:
            filtered_list.append(item)

        if len(filtered_list) == len(unusedGTArray):
            break

    # Set the IOU value for each input bounding box relative to its corresponding ground truth bounding box
    for key, item in dictionary.items():
        item["iouGT"] = 0.0
        for gt in filtered_list:
            if item["shape"] == gt["shape"]:
                item["iouGT"] = gt["gtIOU"]
                item["gtShape"] = gt["gtShape"]

    classification = time.time()
    # if FULLDEBUG:
    #   print("        classification:", round(classification - keepIOU, 2))
    falseNegatives = findFalseNegatives(gtArray, filtered_list)

    # Add these lines to initialize the false positive categories
    for key, item in dictionary.items():
        if item["iouGT"] == 0.0:
            duplicate_detected = False
            # Case 1: Duplicate detection on the same object
            if imageName in used_gt_by_image:
                for used_gt in used_gt_by_image[imageName]:
                    intersection = getIntersection([item["shape"], used_gt])
                    union = getUnion([item["shape"], used_gt])
                    IOU = intersection.area / union.area
                    if IOU > 0:  # Replace iou_threshold with a suitable value
                        item["category"] = "duplicate"  # Add category information
                        duplicate_detected = True
                        break

            if not duplicate_detected:
                # Case 2: Wrong class detection

                item["category"] = "wrong_class"  # Add category information
                gt_txt_file = (
                    folderName
                    + "ground_truth/"
                    + imageName.replace(".jpg", ".txt")
                    .replace(".jpeg", ".txt")
                    .replace(".png", ".txt")
                )
                with open(gt_txt_file, "r") as f:
                    gt_lines = f.readlines()

                gt_boxes = []
                for line in gt_lines:
                    gt_data = line.strip().split()
                    gt_class = " ".join(
                        gt_data[:-4]
                    )  # Join the first elements until the last 4 into a single string
                    gt_box = [
                        float(coord) for coord in gt_data[-4:]
                    ]  # Extract the last 4 elements as bounding box coordinates
                    if gt_class != filterClass:
                        gt_boxes.append((gt_class, gt_box))

                for gt_class, gt_box in gt_boxes:
                    value = [item["shape"], [gt_class] + gt_box]

                    intersection = getIntersection(value)
                    if intersection.area == 0:
                        continue

                    union = getUnion(value)
                    IOU = intersection.area / union.area
                    if IOU >= 0.5:  # The IOU threshold for checking overlaps
                        item["category"] = "wrong_class"
                        break
                else:
                    item["category"] = "far_away"  # Add category information
        else:
            item[
                "category"
            ] = "low_threshold"  # Add category information for low threshold detections

    endclass = time.time()
    # if FULLDEBUG:
    #   print("        endclass:", round(endclass - classification, 2))

    # # Add these lines to store false positive categories in the dictionary
    # dictionary['duplicate_detections'] = duplicate_detections
    # dictionary['wrong_class_detections'] = wrong_class_detections
    # dictionary['far_away_detections'] = far_away_detections
    for key, value in dictionary.items():
        if "gtShape" in value and value["iouGT"] > 0.0:
            previous_gt_shapes.add(tuple(value["gtShape"]))

    return (
        dictionary,
        {"imageId": imgGtMap[imageName], "values": falseNegatives},
        inp,
        previous_gt_shapes,
    )


def generateJson(dictionary, jsonName):
    with open(jsonName + ".json", "w") as fp:
        json.dump(dictionary, fp)


# Helper functions
def reduceInput(removeItems, inp):
    for x in removeItems:
        for a in inp.values():
            if x in a:
                a.remove(x)


def delete_list_items(sorted_list, values_to_remove):
    if not sorted_list:
        return []
    if sorted_list[0]["shape"] not in values_to_remove:
        values_to_remove.append(sorted_list[0]["shape"])

        return [sorted_list[0]] + delete_list_items(sorted_list[1:], values_to_remove)
    return delete_list_items(sorted_list[1:], values_to_remove)


def keepValues(sortedList, key, valuesToRemove):
    sortedListFinal = (0, 0)
    for i, (key, value) in enumerate(sortedList):
        if key == key and value == valuesToRemove:
            sortedListFinal = (key, value)
    for x in valuesToRemove:
        sortedList = deleteValue(sortedList, x)

    return sortedListFinal, sortedList


def deleteValue(sortList, val):
    returnList = []
    for key, value in sortList:
        if val not in value:
            returnList.append((key, value))
    return returnList


def findFalseNegatives(groundTruthBoxes, overlappedBoxes):
    """
    This function finds the ground truth bounding boxes that do not have a corresponding input bounding box.

    Parameters:
        groundTruthBoxes (list): A list of ground truth bounding boxes.
        overlappedBoxes (list): A list of input bounding boxes that overlap with the ground truth bounding boxes.

    Returns:
        list: A list of ground truth bounding boxes that do not have a corresponding input bounding box.
    """
    overlapList = []
    for item in overlappedBoxes:
        overlapList.append(item["gtShape"])
    set1 = set(tuple(x) for x in groundTruthBoxes)
    set2 = set(tuple(x) for x in overlapList)

    result = list(set1 - set2)
    return result


def createPolygon(rectangle):
    xL = float(rectangle[1])
    xR = float(rectangle[3])
    yT = float(rectangle[2])
    yL = float(rectangle[4])
    return Polygon([(xL, yT), (xR, yT), (xR, yL), (xL, yL)])


def getUnion(boundingBoxArray):
    unionPolygon = None
    unionPolygon = createPolygon(boundingBoxArray[0])
    i = 1

    while i < len(boundingBoxArray):
        otherPolygon = createPolygon(boundingBoxArray[i])
        unionPolygon = unionPolygon.union(otherPolygon)
        i = i + 1

    return unionPolygon


def getIntersection(boundingBoxArray):
    """
    Calculate the intersection between a set of bounding boxes.

    Parameters:
        boundingBoxArray (list): A list of bounding boxes.

    Returns:
        Polygon: The intersection between the bounding boxes.
    """
    intersectionPolygon = None
    intersectionPolygon = createPolygon(boundingBoxArray[0])
    i = 1

    while i < len(boundingBoxArray):
        otherPolygon = createPolygon(boundingBoxArray[i])
        newIntersection = intersectionPolygon.intersection(otherPolygon)
        if newIntersection.area == 0:
            return newIntersection
        intersectionPolygon = newIntersection
        i = i + 1

    return intersectionPolygon


def getUnionVisited(boundingBoxArray, visited):
    unionPolygon = None
    if (boundingBoxArray[0][0],) in visited:
        unionPolygon = visited[(boundingBoxArray[0][0],)]
    else:
        unionPolygon = createPolygon(boundingBoxArray[0][1])
        visited[(boundingBoxArray[0][0],)] = unionPolygon
    i = 1
    idgrp = (boundingBoxArray[0][0],)

    while i < len(boundingBoxArray):
        if idgrp + (boundingBoxArray[i][0],) in visited:
            unionPolygon = visited[idgrp + (boundingBoxArray[i][0],)]
            idgrp = idgrp + (boundingBoxArray[i][0],)
        else:
            otherPolygon = createPolygon(boundingBoxArray[i][1])
            unionPolygon = unionPolygon.union(otherPolygon)
            idgrp = idgrp + (boundingBoxArray[i][0],)
            visited[idgrp] = unionPolygon
        i = i + 1

    return unionPolygon


def getIntersectionVisit(boundingBoxArray, visited):
    """
    Calculate the intersection between a set of bounding boxes.

    Parameters:
        boundingBoxArray (list): A list of bounding boxes.

    Returns:
        Polygon: The intersection between the bounding boxes.
    """
    # print(boundingBoxArray)
    intersectionPolygon = None
    if (boundingBoxArray[0][0],) in visited:
        intersectionPolygon = visited[(boundingBoxArray[0][0],)]
    else:
        intersectionPolygon = createPolygon(boundingBoxArray[0][1])
        visited[(boundingBoxArray[0][0],)] = intersectionPolygon
    i = 1
    idgrp = (boundingBoxArray[0][0],)

    while i < len(boundingBoxArray):
        if idgrp + (boundingBoxArray[i][0],) in visited:
            newIntersection = visited[idgrp + (boundingBoxArray[i][0],)]
            # print(idgrp + (boundingBoxArray[i][0],))
            idgrp = idgrp + (boundingBoxArray[i][0],)
            if newIntersection.area == 0:
                return newIntersection
            intersectionPolygon = newIntersection
        else:
            otherPolygon = createPolygon(boundingBoxArray[i][1])
            newIntersection = intersectionPolygon.intersection(otherPolygon)
            # print("created", idgrp)
            idgrp = idgrp + (boundingBoxArray[i][0],)
            visited[idgrp] = newIntersection
            if newIntersection.area == 0:
                return newIntersection
            intersectionPolygon = newIntersection
        i = i + 1

    return intersectionPolygon
