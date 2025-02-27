'''
* Team Id : GG_2336
* Author List : Ajan,Dhiraj,Harish,Santhosh
* Filename: mlcsv.py
* Theme: Geo Guide
* Functions: read_csv(),tracker(),classify_event(),detect_ArUco_details(),final_info(), task_4a_return()
* Global Variables: combat,rehab,military_vehicles,fire,destroyed_building,final={}
'''
####################### IMPORT MODULES #######################

import cv2
import numpy as np
from PIL import Image
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn.functional as F
import csv
import time

##############################################################



################# ADD UTILITY FUNCTIONS HERE #################

combat = "combat"
rehab = "humanitarianaid"
military_vehicles = "militaryvehicles"
fire = "fire"
destroyed_building = "destroyedbuilding"
final={}

#fire, destroyedbuilding, humanitarianaid, militaryvehicles, combat
'''
* Function Name: read_csv()
* Input: name of csv file
* Output: priority order in dictionary format
* Logic: Stores data in csv format
* Example Call: dict_with_pref=read_csv("priority.csv")
'''

def read_csv(csv_name):
    priority_order = {}

    # open csv file (lat_lon.csv)
    # read "lat_lon.csv" file
    # store csv data in lat_lon dictionary as {id:[lat, lon].....}
    # return lat_lon

    with open(csv_name, newline='', mode='r') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            # Check if the row has at least two elements
            if len(row) >= 2:
                priority_order[row[0]] = row[1]

    return priority_order

'''
* Function Name: tracker()
* Input: identified_labels
* Output: None
* Logic: arranging the rows based on priority in the csv file
* Example Call: tracker(identified_labels)
'''

def tracker(identified_labels):

    with open("priority.csv",mode="w") as csvfile:
      fieldnames = ["box","image"]
      writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
      #writer.writeheader()
      keys_nl=identified_labels.keys()
      keys=list(keys_nl)
      values_nl=identified_labels.values()
      values=list(values_nl)
      if "fire" in values:
        k=values.index("fire")
        l=keys[k]
        writer.writerow({"box":l,"image":identified_labels[l]})
      if "destroyedbuilding" in values:
        k=values.index("destroyedbuilding")
        l=keys[k]
        writer.writerow({"box":l,"image":identified_labels[l]})
      if "humanitarianaid" in values:
        k=values.index("humanitarianaid")
        l=keys[k]
        writer.writerow({"box":l,"image":identified_labels[l]})
      if "militaryvehicles" in values:
        k=values.index("militaryvehicles")
        l=keys[k]
        writer.writerow({"box":l,"image":identified_labels[l]})
      if "combat" in values:
        k=values.index("combat")
        l=keys[k]
        writer.writerow({"box":l,"image":identified_labels[l]})


'''
* Function Name: classify_event()
* Input: image-the i=image to classify
* Output:  Dictionary with the probability of each classes
* Logic: This function is used to find the probability of input image to be of which class. We are cropping the image such that the white border of the image is not visible 
* Example Call: classify_event(crop_image)
'''

def classify_event(image) :
    # Define the class names
    classes = [combat , destroyed_building , fire , rehab , military_vehicles]
    model = torch.load("34best_model6.pth")
    model = model.eval()

    # Load and preprocess the image
    h , w = 86 , 86
    x , y = 14 , 15
    img = Image.fromarray ( image )
    img = img.crop ( (x , y , x + w , y + h) )
    mean = [0.4542 , 0.4769 , 0.5142]
    std = [0.2396 , 0.2367 , 0.2449]
    image_transforms = transforms.Compose ( [
        transforms.Resize ( (86 , 86) ) ,
        transforms.ToTensor ( ) ,
        transforms.Normalize(mean, std)
    ] )
    image = image_transforms ( img ).unsqueeze ( 0 )

    output = model ( image )
    probabilities = F.softmax ( output , dim=1 )[0]

    probabilities = probabilities.tolist ( )

    class_probabilities = {class_name : probability for class_name , probability in zip ( classes , probabilities )}

    return class_probabilities

'''
* Function Name: detect_ArUco_details()
* Input: image
* Output: Aruco_corners
* Logic: We are finding the corners of all aruco markers
* Example Call: detect_ArUco_details(frame)
'''
def detect_ArUco_details(image):
    ArUco_corners = {}

    arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
    corners, ids, _ = cv2.aruco.detectMarkers(image, arucoDict)

    if ids is not None and len(ids) > 0:
        for i in range(ids.shape[0]):
            ArUco_corners[int(ids[i][0])] = corners[i][0]

    return ArUco_corners
'''
* Function Name: final_info(0
* Input: Probability-that we got from classify_event(),frameA,frameB,frameC,frameD,frameE-The no. of frames of A,B,C,D,E
* Output: final dictionary- with key as The location and value as the class
* Logic: we are averaging out the probabilities based on the number of frames. And whichever class has higher probability, that will be the class for the location
* Example Call: final_info(Probability,frameA,frameB,frameC,frameD,frameE)
'''
def final_info(Probability,frameA,frameB,frameC,frameD,frameE):
    for key in Probability :
        if key == "A" :
            frame_count = frameA
        elif key == "B" :
            frame_count = frameB
        elif key == "C" :
            frame_count = frameC
        elif key == "D" :
            frame_count = frameD
        elif key == "E" :
            frame_count = frameE
        if frame_count>6:
            Prob = {class_name : probability / frame_count for class_name , probability in Probability[key].items ( )}
            max_class = max ( Prob , key=Prob.get )
            final[key] = max_class
        else:
            final[key] = "No picture"


    return final

##############################################################

'''
* Function Name: task_4a_return()
* Input: None
* Output: identified_labels
* Logic: Same function as final_info()
* Example Call: task_4a_return()
'''
def task_4a_return():

    identified_labels = {}

##############	ADD YOUR CODE HERE	##############
    identified_labels= final_info(Probability , frameA , frameB , frameC , frameD , frameE)

##################################################
    return identified_labels
###############	Main Function	#################
if __name__ == "__main__":

    cap = cv2.VideoCapture ( 1, cv2.CAP_DSHOW )
    cap.set ( cv2.CAP_PROP_FRAME_WIDTH , 1920 )
    cap.set ( cv2.CAP_PROP_FRAME_HEIGHT , 1080 )

    if not cap.isOpened ( ) :
        print ( "Error: Could not open camera." )
        exit ( )
#these are used for counting frames
    frameA = 0
    frameB = 0
    frameC = 0
    frameD = 0
    frameE = 0
#Probability dictionary
    Probability = {
        "A" : {combat : 0 , destroyed_building : 0 , fire : 0 , rehab : 0 , military_vehicles : 0} ,
        "B" : {combat : 0 , destroyed_building : 0 , fire : 0 , rehab : 0 , military_vehicles : 0} ,
        "C" : {combat : 0 , destroyed_building : 0 , fire : 0 , rehab : 0 , military_vehicles : 0} ,
        "D" : {combat : 0 , destroyed_building : 0 , fire : 0 , rehab : 0 , military_vehicles : 0} ,
        "E" : {combat : 0 , destroyed_building : 0 , fire : 0 , rehab : 0 , military_vehicles : 0}}

    while True :
        ret , frame = cap.read ( )

        if not ret :
            print ( "Error: Could not read frame." )
            break

        ArUco_corners = detect_ArUco_details ( frame )

        # Check if all necessary markers are found
        if all ( key in ArUco_corners for key in [4 , 5 , 6 , 7] ) :
            output_size = (1080 , 1080)

            src_pts = np.float32 (
                [ArUco_corners[5][2] , ArUco_corners[4][3] , ArUco_corners[6][0] , ArUco_corners[7][1]] )
            dst_pts = np.float32 ( [[0 , 0] , [output_size[0] - 1 , 0] , [output_size[0] - 1 , output_size[1] - 1] ,
                                    [0 , output_size[1] - 1]] )

            perspective_matrix = cv2.getPerspectiveTransform ( src_pts , dst_pts )
            transformed_image = cv2.warpPerspective ( frame , perspective_matrix , output_size )
            # denoised_image = cv2.fastNlMeansDenoising ( transformed_image , None , h=1 , templateWindowSize=5, searchWindowSize=13 )


            img_gray = cv2.cvtColor ( transformed_image , cv2.COLOR_BGR2GRAY )

            # Split the image horizontally
            height , width = img_gray.shape[:2]
            left_half = img_gray[: , :width // 2]
            right_half = img_gray[: , width // 2 :]

            # Apply different thresholds to the left and right halves
            _ , threshold_left = cv2.threshold ( left_half , 168 , 255 , cv2.THRESH_BINARY )
            _ , threshold_right = cv2.threshold ( right_half , 179 , 255 , cv2.THRESH_BINARY )

            # Combine the thresholded halves
            img_thresholded = np.hstack ( (threshold_left , threshold_right) )
            contours , _ = cv2.findContours ( img_thresholded , cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE )
            lists = []
            dict_crop = {}
            dict_pos = {}
            for cnt in contours :
                area = cv2.contourArea ( cnt )
                #detecting white borders
                if 9300 <= area <= 15000 :
                    x , y , w , h = cv2.boundingRect ( cnt )
                    if 0.97 <= h / w <= 1.03 :
                        img_crop = transformed_image[y :y + h , x :x + w]
                        #cropping image and naming them based on their location
                        lists.append ( img_crop )
                        if x < 300 and y > 540 :
                            dict_crop["A"] = img_crop
                            dict_pos["A"] = [x , y , w , h]
                        elif x < 540 and 540 > y > 400 :
                            dict_crop["D"] = img_crop
                            dict_pos["D"] = [x , y , w , h]
                        elif x < 540 and 300 > y > 0 :
                            dict_crop["E"] = img_crop
                            dict_pos["E"] = [x , y , w , h]
                        elif x > 540 and y < 600 :
                            dict_crop["C"] = img_crop
                            dict_pos["C"] = [x , y , w , h]
                        elif x > 540 and y > 600 :
                            dict_crop["B"] = img_crop
                            dict_pos["B"] = [x , y , w , h]

            for key , crop_img in dict_crop.items ( ) :
                crop_img1=crop_img
                hsv_img = cv2.cvtColor ( crop_img1 , cv2.COLOR_BGR2HSV )

                # Define a green color range in HSV
                upper_green = np.array ( [170 , 140 , 150] )
                lower_green = np.array ( [10 , 3 , 5] )

                # Create a mask using the green color range
                mask = cv2.inRange ( hsv_img , lower_green , upper_green )

                # Calculate the percentage of green area in the white rectangle
                total_pixels = np.sum ( mask == 255 )
                total_area = dict_pos[key][2] * dict_pos[key][3]
                green_percentage = (total_pixels / total_area) * 100
                #check if we have image or not
                if green_percentage < 49 :
                    #applying CLAHE on images
                    clahe = cv2.createCLAHE ( clipLimit=2 )

                    b , g , r = cv2.split ( crop_img )
                    b = clahe.apply ( b )
                    g = clahe.apply ( g )
                    r = clahe.apply ( r )
                    merged_bgr = cv2.merge ( (b , g , r) )
                    image_hsv = cv2.cvtColor ( crop_img , cv2.COLOR_BGR2HSV )
                    h , s , v = cv2.split ( image_hsv )
                    v = clahe.apply ( v )
                    merged_hsv = cv2.merge ( (h , s , v) )
                    bgr_enhanced = cv2.cvtColor ( merged_hsv , cv2.COLOR_HSV2BGR )

                    c = classify_event ( bgr_enhanced )
                    for class_name , probability in c.items ( ) :
                        Probability[key][class_name] += probability
                    #Based on the location, add frame of that location
                    if key == "A" :
                        frameA += 1
                        frame_count = frameA
                    elif key == "B" :
                        frameB += 1
                        frame_count = frameB
                    elif key == "C" :
                        frameC += 1
                        frame_count = frameC
                    elif key == "D" :
                        frameD += 1
                        frame_count = frameD
                    elif key == "E" :
                        frameE += 1
                        frame_count = frameE

                    if frame_count > 5 :
                        Prob = {class_name : probability / frame_count for class_name , probability in
                                Probability[key].items ( )}
                        max_class = max ( Prob , key=Prob.get )
                        #putting text on screen
                        cv2.putText ( transformed_image , max_class , (dict_pos[key][0] , dict_pos[key][1] - 10) ,
                                      cv2.FONT_HERSHEY_SIMPLEX , 0.9 , (0 , 255 , 0) , 2 )
                        cv2.rectangle ( transformed_image , (dict_pos[key][0] , dict_pos[key][1]) ,
                                        (dict_pos[key][0] + dict_pos[key][2] , dict_pos[key][1] + dict_pos[key][3]) ,
                                        (0 , 255 , 0) , 2 )

                    else :
                        break

            resized_transformed_image = cv2.resize ( transformed_image , (960 , 960) )
            cv2.imshow ( "Transformed Image" , resized_transformed_image )
            cv2.moveWindow ( "Transformed Image" , 0 , 0 )

        if cv2.waitKey ( 1 ) & 0xFF == ord ( 'q' ) :
            break

    cap.release ( )
    cv2.destroyAllWindows ( )
    identified_labels = task_4a_return()
    print(identified_labels)
    tracker(identified_labels)
    dict_with_pref=read_csv("priority.csv")

#fire, destroyedbuilding, humanitarianaid, militaryvehicles, combat