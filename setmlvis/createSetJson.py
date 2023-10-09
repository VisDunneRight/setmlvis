import os
import itertools
import json
from PIL import Image
from shapely.geometry import Polygon


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

    modelNames = getModelNames(folderName)
    emptyDictionary = createEmptyDictionary(modelNames)
    allFilesDictionary = parseInputFolder(folderName, objectClass, modelNames)

    finalDictionary = fillDictionary(
        folderName, emptyDictionary, allFilesDictionary, modelNames, setIou, objectClass
    )
    finalDictionaryWithMetadata = generateMetadata(
        folderName, finalDictionary, modelNames, setIou
    )

    if jsonName != None:
        generateJson(finalDictionaryWithMetadata, jsonName)
    return finalDictionaryWithMetadata


def generateMetadata(folderName, dictionary, modelNames, setIOU):
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
    return newDict


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


def createEmptyDictionary(modelNames: list[str]) -> dict[str, list[str]]:
    """
    Create an empty dictionary with keys formed by combinations of the specified model names.

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


def fillDictionary(
    folderName, emptyDictionary, allFilesDictionary, modelNames, iou, filterClass
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
    for key, value in allFilesDictionary.items():
        bigDict = getEachImageInformation(
            folderName, key, value, iou, modelNames, filterClass, idCounter
        )
        for key, value in bigDict.items():
            emptyDictionary[key].append(value)
    return emptyDictionary


def getEachImageInformation(
    folderName, imageName, inp, iouAlgos, modelNames, filterClass, idCounter
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

    for L in range(len(modelNames) + 1, -1, -1):
        reduceInput(removeItems, inp)

        for subset in itertools.combinations(modelNames, L):
            if len(subset) != 0:
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
                    idCounter,
                )

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

                bigDict[stringTotal] = {"detections": dictionary, "FN": falseNegatives}

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
    idCounter,
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

    # Create a list of the input bounding boxes from the subset
    for s in subset:
        arr.append(inp[s])

    dictRank = []

    # Calculate the IOU between each combination of input bounding boxes
    for x in itertools.product(*arr):
        intersection = getIntersection(x)
        if intersection.area == 0:
            continue
        union = getUnion(x)
        IOU = intersection.area / union.area
        tup = (IOU, x)
        dictRank.append(tup)

    # Sort the list of IOU values in descending order
    sortedList = sorted(dictRank, key=lambda x: x[0], reverse=True)
    values_to_remove = []

    # Keep only the bounding boxes with IOU values higher than the threshold

    count = 0
    for key, value in sortedList:
        if key != 0:
            if key >= iouAlgos:
                values_to_remove = value
                addList, sortedList = keepValues(sortedList, key, values_to_remove)

                if addList[0] != 0:
                    newDict = {}
                    newDict["imgName"] = imageName
                    newDict["id"] = str(idCounter.count) + "-" + imageName
                    newDict["IOU"] = key
                    newDict["boxes"] = dict(zip(subset, value))
                    im = Image.open(folderName + "images/" + imageName)
                    newDict["imgSize"] = im.size
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
                    idCounter.increment()
                    # dictionary.append(newDict)

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

    # # Add these lines to store false positive categories in the dictionary
    # dictionary['duplicate_detections'] = duplicate_detections
    # dictionary['wrong_class_detections'] = wrong_class_detections
    # dictionary['far_away_detections'] = far_away_detections
    for key, value in dictionary.items():
        if "gtShape" in value and value["iouGT"] > 0.0:
            previous_gt_shapes.add(tuple(value["gtShape"]))
    return dictionary, falseNegatives, inp, previous_gt_shapes


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


def getUnion(boundingBoxArray):
    unionPolygon = None
    xL = float(boundingBoxArray[0][1])
    xR = float(boundingBoxArray[0][3])
    yT = float(boundingBoxArray[0][2])
    yL = float(boundingBoxArray[0][4])
    unionPolygon = Polygon([(xL, yT), (xR, yT), (xR, yL), (xL, yL)])
    i = 1

    while i < len(boundingBoxArray):
        xL = float(boundingBoxArray[i][1])
        xR = float(boundingBoxArray[i][3])
        yT = float(boundingBoxArray[i][2])
        yL = float(boundingBoxArray[i][4])
        otherPolygon = Polygon([(xL, yT), (xR, yT), (xR, yL), (xL, yL)])
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
    xL = float(boundingBoxArray[0][1])
    xR = float(boundingBoxArray[0][3])
    yT = float(boundingBoxArray[0][2])
    yL = float(boundingBoxArray[0][4])
    intersectionPolygon = Polygon([(xL, yT), (xR, yT), (xR, yL), (xL, yL)])
    i = 1

    while i < len(boundingBoxArray):
        xL = float(boundingBoxArray[i][1])
        xR = float(boundingBoxArray[i][3])
        yT = float(boundingBoxArray[i][2])
        yL = float(boundingBoxArray[i][4])
        otherPolygon = Polygon([(xL, yT), (xR, yT), (xR, yL), (xL, yL)])
        newIntersection = intersectionPolygon.intersection(otherPolygon)
        if newIntersection.area == 0:
            return newIntersection
        intersectionPolygon = newIntersection
        i = i + 1

    return intersectionPolygon
