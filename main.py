"""Everardo Marquez
    Feb 18, 2023

Just a small and simple program to take a picture using the webcam with OpenCV and applying some style filters
to the captured image. Created it for use in account profile pictures.
"""

import cv2
import sys

def main():
    style_option = input("What style option would you like: 1 or 2? ")
    file_name = input("What would you like to call the file? Do not enter the file extension: ")
    file_name += ".jpg"

    #capture the original image to style
    capture_image(file_name)

    #apply the selected style
    if style_option == "1":
        style_one(file_name)
    elif style_option == "2":
        style_two(file_name)
    else:
        print("Invalid option for Style: Only original picture taken.")
        sys.exit()


def capture_image(file_name):
    #access the built-in webcam
    capture = cv2.VideoCapture(0)

    #Set the webcam resolution
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    #run the webcam capturing images
    while True:
        ret, frame = capture.read()
        cv2.imshow("Webcam Feed (Press Space Bar to take picture)", frame)

        #wait for a key press, if space bar is pressed break out of loop
        key_pressed = cv2.waitKey(1) & 0xFF
        if key_pressed == ord(" "):
            break
    
    #release back the camera resources
    capture.release()

    #if a frame capture was successful, save the image to the currend directory
    if ret:
        cv2.imwrite(file_name, frame)
    else:
        print("Error Capturing image")
        sys.exi()



def style_one(file_name):
    image = cv2.imread(file_name)

    #use openCV built-in method for stylizing an image
    stylized = cv2.stylization(image, sigma_s=100, sigma_r=0.5)
    save_show_image(file_name, stylized)



def style_two(file_name):
    image = cv2.imread(file_name)

    #create a grayscale of the image
    gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #apply non-linear filtering to reduce noise and blur the image
    gray_blurred = cv2.medianBlur(gray_scale, 13)

    #get the edges through an adaptive threshold to create a binary image
    edges = cv2.adaptiveThreshold(gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    #smooth out the image while preserving the edges
    blurred = cv2.bilateralFilter(image, d=15, sigmaColor=150, sigmaSpace=150)

    #apply binary mask to the image
    stylized = cv2.bitwise_and(blurred, blurred, mask=edges)

    save_show_image(file_name, stylized)



def save_show_image(file_name: str, image):
    #update the file name and save/ show the styled image
    filename_dot = file_name.find(".")
    file_name = file_name[:filename_dot]
    cv2.imwrite(f"{file_name}_styled.jpg", image)
    cv2.imshow("Styled Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()