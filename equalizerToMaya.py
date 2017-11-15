import maya.cmds as cmds
import maya.OpenMaya as om
import maya.mel as mel
import os.path

#Global Variables
locatorGroups = []
imgPlaneCameras = {}
imgPlanePaths = {}
newImgPlanes = []
melInputField = ""
script = ""
camName = ""
imgSeqQuery = {}

def UI():
    if cmds.window("EqToMUI", exists=True):
        cmds.deleteUI("EqToMUI")
    window = cmds.window("EqToMUI", title="Equalizer to Maya v1.2", w=450, h=500, mnb=False, mxb=False, s=False)
    
    #Create main layout
    mainLayout = cmds.columnLayout(w=450, h=500)
    cmds.frameLayout(label="Setup", w=450 , h=85)
    cmds.rowColumnLayout(nc=3, cw=[(1,400),(2,5),(3,25)], co=[(1,"both",5), (2,"both", 5), (3,"both",5)] )

    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)

    cmds.text(l="Load 3D Equalizer MEL script:", al="left")
    cmds.text(l="")
    cmds.text(l="")

    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)

    cmds.textField("melInputField", w=400)
    cmds.text(l="")
    cmds.button("browseMel", l="...", w=25, c=browseFilePath)

    cmds.setParent( '..' )
    cmds.setParent( '..' )

    cmds.frameLayout(label ="Locators", w = 450 , h=65)
    cmds.rowColumnLayout(nc=11, cw=[(1,35),(2,2),(3,30),(4,40),(5,80),(6,6),(7,30),(8,20),(9,80),(10,6),(11,30)])

    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)

    cmds.text(l="Size:")
    cmds.text(l="")
    cmds.textField("locatorSize", w=30, tx="5")
    cmds.text(l="")
    cmds.text(l="Hide Attributes:")
    cmds.text(l="")
    cmds.checkBox("hideLocator", l="", v=True)
    cmds.text(l="")
    cmds.text(l="Lock Attributes:")
    cmds.text(l="")
    cmds.checkBox("lockLocator", l="", v=True)

    cmds.setParent( '..' )
    cmds.setParent( '..' )

    cmds.frameLayout(label ="Cameras", w = 450 , h=100)
    cmds.rowColumnLayout(nc=11, cw=[(1,35),(2,2),(3,30),(4,40),(5,80),(6,6),(7,30),(8,20),(9,80),(10,6),(11,30)])

    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)

    cmds.text(l="Size:")
    cmds.text(l="")
    cmds.textField("cameraSize", w=30, tx="20")
    cmds.text(l="")
    cmds.text(l="Hide Attributes:")
    cmds.text(l="")
    cmds.checkBox("hideCamera", l="", v=True)
    cmds.text(l="")
    cmds.text(l="Lock Attributes:")
    cmds.text(l="")
    cmds.checkBox("lockCamera", l="", v=True)

    cmds.setParent( '..' )
    cmds.rowColumnLayout(nc=7, cw=[(1,90),(2,2),(3,50),(4,30),(5,80),(6,2),(7,50)])

    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)

    cmds.text(l="Near Clip Plane:")
    cmds.text(l="")
    cmds.textField("nearClipPlane", w=50, tx="0.1")
    cmds.text(l="")
    cmds.text(l="Far Clip Plane:")
    cmds.text(l="")
    cmds.textField("farClipPlane", w=50, tx="100000")

    cmds.setParent( '..' )
    cmds.setParent( '..' )

    cmds.rowColumnLayout(nc=3, cw=[(1,125),(2,200),(3,125)])

    cmds.separator(h=15, vis=False)
    cmds.separator(h=15, vis=False)
    cmds.separator(h=15, vis=False)

    cmds.text(l="")
    cmds.button("importData", l="Import Data", h=30, c=importData)
    cmds.text(l="")

    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)
    cmds.separator(h=10, vis=False)

    cmds.setParent( '..' )

    cmds.rowColumnLayout(nc=3, cw=[(1,15),(2,420),(3,15)])

    cmds.text(l="")
    cmds.progressBar("progress", width=400)
    cmds.text(l="")

    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)

    cmds.setParent( '..' )

    cmds.rowColumnLayout(nc=2, cw=[(1,15),(2,435)])
    cmds.text(l="")
    cmds.text("warningsFeedback", l="0 Warnings", al="left")

    cmds.separator(h=2, vis=False)
    cmds.separator(h=2, vis=False)

    cmds.text(l="")
    cmds.text("errorsFeedback", l="0 Errors", al="left")

    cmds.separator(h=5, vis=False)
    cmds.separator(h=5, vis=False)

    cmds.setParent( '..' )

    cmds.rowColumnLayout(nc=2, cw=[(1,220),(2,210)])
    cmds.text(l="")
    cmds.text("copyright", l="Jeronimo Maggi", al="right")

    cmds.showWindow(window)

def browseFilePath(*args):
    returnPath = cmds.fileDialog2(ds=2, fm=1, ff="Mel files (*.mel)", cap="Select 3DE MEL Script")[0]
    cmds.textField("melInputField", edit=True, text=returnPath)

def importData(*args):
    #Get script location
    global melInputField, script #Mel Eval only accepts global vars
    melInputField = cmds.textField("melInputField", q=True, tx=True)
    melInputField = "/".join(melInputField.split("\\"))
    try:
        if melInputField.rpartition(".")[-1] != "mel":
            cmds.error("Select a MEL Script!")
    except:
       cmds.error("Select a MEL Script!")
    #Get MEL Script info
    sceneName, script = searchMelScript(melInputField)
    try:
        if cmds.text("copyright", q=True, l=True) != "Jeronimo Maggi":
            cmds.error("Copyright")
    except:
        cmds.error("Copyright")
       #Check if sceneName already exists
    if sceneName in cmds.ls(tr=True):
        cmds.text("errorsFeedback", l="1 Error - You can't import the same script again! Check the Script Editor for details", e=True, al="left")
        cmds.error("You can't import the same script again! \n The object/group \"" + sceneName + "\" has the same name as the 3D Equalizer group. Please rename it or delete it and try again.")
    #Execute MEL Script - Evaluating in MEL a variable after source will return an error.
    #Use a variable that includes the source keyword and remember to use \".
    melInputField = "source \"" + melInputField + "\""
    try:
        mel.eval(script)
    except:
        cmds.error("Error executing MEL script")   
    #Query locator info
    locatorSize = cmds.textField("locatorSize", q=True, tx=True)
    try:
        locatorSize = float(locatorSize)
    except:
        raise ValueError("Locator Size value is invalid. Only use numbers")
    hideLocator = not cmds.checkBox("hideLocator", q=True, v=True) #Invert with NOT bc Maya uses keyable, not hide.
    lockLocator = cmds.checkBox("lockLocator", q=True, v=True)
    #Query camera info
    cameraSize = cmds.textField("cameraSize", q=True, tx=True)
    try:
        cameraSize = float(cameraSize)
    except:
        raise ValueError("Camera Size value is invalid. Only use numbers")
    hideCamera = not cmds.checkBox("hideCamera", q=True, v=True) #Invert wiht NOT bc Maya uses keyable, not hide.
    lockCamera = cmds.checkBox("lockCamera", q=True, v=True)
    nearClipPlane = cmds.textField("nearClipPlane", q=True, tx=True)
    try:
        nearClipPlane = float(nearClipPlane)
    except:
        raise ValueError("Near Clip Plane value is invalid. Only use numbers")
    farClipPlane = cmds.textField("farClipPlane", q=True, tx=True)
    try:
        farClipPlane = float(farClipPlane)
    except:
        raise ValueError("Far Clip Plane value is invalid. Only use numbers")

    getLocatorGroups(sceneName)
    cameras = getCameras(sceneName)
    locators = getLocators(locatorGroups)[0]

    createDisplayLayer(locators)
    lockUnlockLocators(locators, lockLocator, hideLocator, locatorSize)
    lockUnlockGroups(locatorGroups, sceneName, lockLocator, hideLocator)

    lockUnlockCameras(cameras, lockCamera, hideCamera)
    camerasAttributes(cameras, cameraSize, nearClipPlane, farClipPlane)

    getImgPlanePaths(imgPlaneCameras.values())
    errors, warnings = createImagePlanes()
    setImgPlaneAttribs(newImgPlanes)

    if errors == 1:
        cmds.text("errorsFeedback", l="1 Error: Image file is missing! - Check the Script Editor for details", e=True, al="left")
    elif errors > 1:
        cmds.text("errorsFeedback", l="{0} Errors: Image files are missing! - Check the Script Editor for details".format(str(errors)), e=True, al="left")
    if warnings == 1:
        cmds.text("warningsFeedback", l="1 Warning: Dewarped image not found! - Check the Script Editor for details", e=True, al="left")
    elif warnings > 1:
        cmds.text("warningsFeedback", l="{0} Warnings: Dewarped images not found! - Check the Script Editor for details".format(str(warnings)), e=True, al="left")

#Get Scene name, Img file paths, if sequence and return script without image planes
def searchMelScript(melPath):
    global camName #Used in the Mel command
    sceneGroupName = ""
    with open(melPath, "r") as f:
        searchLines = f.readlines()

    for i, line in enumerate(searchLines):
        #Get sceneName
        if "string $sceneGroupName = `group -em -name" in line:
            sceneGroupName = line.split("\"")[1]
        #Camera name, ImgPlane and query img seq
        elif "camera -name" in line:
            camName = line.split("\"")[1]
            camName = mel.eval('formValidObjectName(python("camName"))') #Replaces illegal chars with underscores
            imgPlaneCameras[camName] = searchLines[i+17].split("\"")[-2]
            imgSeqQuery[camName] = int(searchLines[i + 15].rpartition(")")[-1][1])
    #Delete Image Plane
    for i, line in enumerate(searchLines):
        if "// create image plane..." in line:
            del(searchLines[i:i+11])
    script = "".join(searchLines)
    return sceneGroupName, script

#Get Locator Groups
def getLocatorGroups(scene):
    relativeNodes = cmds.listRelatives(scene)
    for node in relativeNodes:
        try:
            if cmds.nodeType(node) == "transform":
                if cmds.listRelatives(cmds.listRelatives(node)[0])[0] in cmds.ls(type="locator"):
                    locatorGroups.append(node)
        except:
            continue

#Get Cameras
def getCameras(scene):
    allCams = []
    cameras = []
    for camera in cmds.ls(ca=True):
        transformCam = cmds.listRelatives(camera, p=True)[0]
        allCams.append(transformCam)
    relativeNodes = cmds.listRelatives(scene)
    for node in relativeNodes:
        if node in allCams:
            cameras.append(node)
    return cameras

#Get Locators
def getLocators(locatorGroups):
    tmp = []
    for group in locatorGroups:
         tmp.append(cmds.listRelatives(group, c=True))
    return tmp

#Create display layer
def createDisplayLayer(locs):
    try:
        if cmds.objectType("locators") == "displayLayer":
                cmds.editDisplayLayerMembers("locators", locs)
    except:
        cmds.createDisplayLayer(n="locators", e=True, nr=True)
        cmds.setAttr("locators.color", 13)
        cmds.editDisplayLayerMembers("locators", locs)

#Lock/Unlock all locators channels
def lockUnlockLocators(locators, lock, hide, size):
    for locator in locators:
        cmds.setAttr("{0}.tx".format(locator), l=lock, k=hide)
        cmds.setAttr("{0}.ty".format(locator), l=lock, k=hide)
        cmds.setAttr("{0}.tz".format(locator), l=lock, k=hide)
        cmds.setAttr("{0}.rx".format(locator), l=lock, k=hide)
        cmds.setAttr("{0}.ry".format(locator), l=lock, k=hide)
        cmds.setAttr("{0}.rz".format(locator), l=lock, k=hide)
        #Scale
        cmds.setAttr("{0}.scale".format(locator), size, size, size, type="double3")

#Lock/Unlock locator group and scene
def lockUnlockGroups(locatorGroup, sceneGroup, lock, hide):
    scene = [sceneGroup]
    groups = scene + locatorGroup
    for group in groups:
        cmds.setAttr("{0}.tx".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.ty".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.tz".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.rx".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.ry".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.rz".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.sx".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.sy".format(group), l=lock, k=hide)
        cmds.setAttr("{0}.sz".format(group), l=lock, k=hide)

#Store Img Planes dewarped paths
def getImgPlanePaths(imagePlanes):
    for imagePlane in imagePlanes:
        try:
            imagePlane = "/".join(imagePlane.split("\\"))
            imgName = imagePlane.split("/")[-1]
            imgName = imgName.split(".")
            imgExtension = "." + imgName[-1]
            imgName = ".".join(imgName[:-1])
            dewarpedName = imgName + "_dewarped"
            dewarpedPath = "/".join(imagePlane.split("/")[:-1]) + "/" + dewarpedName + imgExtension
            #Check for file existance
            if not os.path.isfile(dewarpedPath) and not os.path.isfile(imagePlane): #If neither file exists
                imgPlanePaths[imagePlane] = ""
            elif os.path.isfile(dewarpedPath):
                imgPlanePaths[imagePlane] = dewarpedPath
            else:
                imgPlanePaths[imagePlane] = imagePlane
        except:
            om.MGlobal_displayError("There are no Image Planes")

#Create New Image Planes        
def createImagePlanes():
    errors = 0
    warnings = 0
    if 100 % len(imgPlaneCameras) != 0:
        progressAmount = (100 // len(imgPlaneCameras)) + 1
    else:
        progressAmount = 100 / len(imgPlaneCameras)

    for i, camera in enumerate(imgPlaneCameras.keys()):
        defaultImgPlane = imgPlaneCameras[camera]
        dewarpedImg = imgPlanePaths[defaultImgPlane]
        if dewarpedImg == defaultImgPlane:
            om.MGlobal_displayWarning("The dewarped image wasn't found for the following camera :" + "\n"+ camera + "\nUsing default warped image instead...")
            warnings += 1
        elif dewarpedImg == "":
            om.MGlobal_displayError("The image plane for camera " + camera + " was not set since no dewarped or warped file was found.")
            errors += 1
        cmds.imagePlane(c=cmds.listRelatives(camera, c=True)[0], n=camera + "_imagePlane1", fn=dewarpedImg, sia=False)
        newImgPlanes.append(camera + "_imagePlane1")
        cmds.progressBar("progress", e=True, pr=progressAmount * (i+1))
    cmds.progressBar("progress", e=True, pr=100)
    return errors, warnings

#Lock cameras attributes
def lockUnlockCameras(cameras, lock, hide):
    for camera in cameras:
        cmds.setAttr("{0}.tx".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.ty".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.tz".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.rx".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.ry".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.rz".format(camera), l=lock, k=hide)
        cmds.setAttr("{0}.hfa".format(camera), l=lock)
        cmds.setAttr("{0}.vfa".format(camera), l=lock)
        cmds.setAttr("{0}.fl".format(camera), l=lock)
        cmds.setAttr("{0}.lsr".format(camera), l=lock)
        cmds.setAttr("{0}.fs".format(camera), l=lock)
        cmds.setAttr("{0}.fd".format(camera), l=lock)
        cmds.setAttr("{0}.sa".format(camera), l=lock)
        cmds.setAttr("{0}.coi".format(camera), l=lock)

#Set Cameras attributes
def camerasAttributes(cameras, cameraSize, nearClip, farClip):
    camShape = ""
    for camera in cameras:
        cmds.setAttr("{0}.scale".format(camera), cameraSize, cameraSize, cameraSize, type="double3")
        camShape = cmds.listRelatives(camera, s=True)[0]
        cmds.setAttr(camShape+ ".nearClipPlane", nearClip)
        cmds.setAttr(camShape+ ".farClipPlane", farClip)

#Set Img Plane attribs (view through current, depth)
def setImgPlaneAttribs(imagePlanes):
    imgPlaneShape = ""
    for imagePlane in imagePlanes:
        imgPlaneShape = cmds.listRelatives(imagePlane, ad=True)[0]
        cmds.setAttr(imgPlaneShape + ".displayOnlyIfCurrent", True)
        cmds.setAttr(imgPlaneShape + ".depth", 1000)
        cmds.setAttr(imgPlaneShape + ".useFrameExtension", imgSeqQuery[cmds.listRelatives(cmds.listRelatives(imagePlane, p=True)[0], ap=True)[0]])
        cmds.refreshEditorTemplates()

UI()

