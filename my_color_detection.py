import numpy as np
import pandas as pd
import cv2
import argparse

#create the argument parser to take parameter inputs from CLI
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required = True, help = "Input-image")
args = vars(ap.parse_args())
imgPath = args['image']


#Reading the image
img = cv2.imread(imgPath)

#Reading the colors dataset
df = pd.read_csv('colors.csv')

#However, the csv file has no column names i.e. Headers. We need to fix this by manually naming the columns.
col_names = ['Color', 'Color_Name', 'HEXcode', 'R', 'G', 'B']
df = pd.read_csv('colors.csv', header = None, names = col_names)

#Calculating the "distance" of the pixel values from that of the dataset color values.
def calulate_distance(i,R,G,B):
	dist = abs(R - int(df.loc[i,'R'])) + abs(G - int(df.loc[i,'G'])) + abs(B - int(df.loc[i,'B']))
	return dist

#Get the color name based on the nearest possible choice out of the given dataset.
def getColorName(R,G,B):
	min = 9999999
	for i in range(len(df.index)):
		d = calulate_distance(i,R,G,B)
		if(d < min):
			min = d
			name = df.loc[i,'Color_Name']
	return name

#declaring global variables
r = g = b = 0
x_pos = y_pos = 0
click = False

#Reading the pixel values from a specific location in the image.
def read_rgb(event, x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global r,g,b,x_pos,y_pos,click
		click = True
		x_pos = x
		y_pos = y
		b,g,r = img[y_pos, x_pos]
		b = int(b)
		g = int(g)
		r = int(r)


#Creating a window to display the image
cv2.namedWindow('image')
cv2.setMouseCallback('image', read_rgb)

#Setting up the display text about the identified color and its RGB value.
while(1):
	cv2.imshow("image",img)
	#Exit if 'ESC' key is pressed
	if cv2.waitKey(20) & 0xFF ==27:
		break

	if (click):

		cv2.rectangle(img, (20, 20), (750, 60), (b,g,r), -1)
		text = getColorName(r,g,b) + ' (R, G, B) = (' + str(r) + ", " + str(g) + ", " + str(b) + ")"
		cv2.putText(img, text, (50,50), 2, 0.8, (255,255,255), 2, cv2.LINE_AA)

		#for light colors, let's display the text in black
		if (r+b+g >= 550):	
			cv2.putText(img, text, (50,50), 2, 0.8, (0,0,0), 2, cv2.LINE_AA)

		click = False

cv2.destroyAllWindows()





