import cv2
import numpy as np
#python.exe lanes.py
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    'cv2.Canny(image, low_threashold, high_threashold)'
    canny = cv2.Canny(blur, 50, 150)
    return canny

def make_coordinates(image,line_parameters):
    slope, intercept = line_parameters
    y1 = image.shape[0]
    y2 = int(y1*(3/5))
    x1 = int((y1 - intercept)/slope)
    x2 = int((y2 - intercept)/slope)
    return np.array([x1, y1, x2, y2])


def average_slope_intercept(image, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        # print(line)
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        # print(slope, 'slope')
        # print(intercept)
        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))
    # print(left_fit)
    # print(right_fit)
    left_fit_average = np.average(left_fit, axis=0)
    print(left_fit_average)
    right_fit_average = np.average(right_fit, axis=0)
    print(right_fit_average)
    left_line = make_coordinates(image, left_fit_average)
    right_line = make_coordinates(image, right_fit_average)
    return np.array([left_line, right_line])


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            #print(line)
            x1, y1, x2, y2 = line.reshape(4)        #convert into 1D array
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)  #Line in blue colour with thickness 10
    return line_image
def region_of_interest(image):
    height = image.shape[0]
    polygons = np.array([[(200, height), (1100, height), (550, 250)]])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, polygons, 255)  #filled polygon with white colour(255)
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

# image = cv2.imread('test_image.jpg')
# lane_image = np.copy(image)
# canny_image = canny(lane_image)
# cropped_image = region_of_interest(canny_image)
# lines = cv2.HoughLinesP(cropped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
# 'this line converts the lines into solid line considering given attributes which is in 2d array'
# averaged_lines = average_slope_intercept(lane_image, lines)
# line_image = display_lines(lane_image, averaged_lines)
# combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
# # cv2.imshow('result', image)
# # cv2.imshow('result', canny)
# # cv2.imshow('result', cropped_image)
# # cv2.imshow('result', line_image)
# cv2.imshow('result', combo_image)
# cv2.waitKey(0)

'Lane detection for a video'

cap = cv2.VideoCapture('test.mp4')
while(cap.isOpened()):
    _, frame = cap.read()
    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 2, np.pi / 180, 100, np.array([]), minLineLength=40, maxLineGap=5)
    'this line converts the lines into solid line considering given attributes which is in 2d array'
    averaged_lines = average_slope_intercept(frame, lines)
    line_image = display_lines(frame, averaged_lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('result', combo_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()