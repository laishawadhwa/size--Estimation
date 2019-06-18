import csv 
import requests 
import cv2
import os
import xml.etree.ElementTree as ET 
from scipy.spatial import distance as dist
import argparse


#utilities for size estimation usign two views
def checkOrientation(pts):
    val=(pts[1][1] - pts[0][1])*(pts[2][0] - pts[1][0]) - (pts[2][1] - pts[1][1])*(pts[1][0] - pts[0][0])
    if val>0:
        return 1 # counterclockwise
    else:
        return 2 # clockwise

def direction(array):
    dist1=dist.euclidean(array[0],array[1])
    dist2= dist.euclidean(array[0],array[3])
    print(dist1,dist2)
    return dist1 < dist2

def midpointCalc(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# refernce object coordinates-> to calculate pixels per metric


def refrenceSizeEstimator(ti,array,lenreal):
    orientation=checkOrientation(array)
    slopecheck= direction(array)
    #print(slopecheck)
    if (orientation==2 and slopecheck==True) or ( orientation==1 and slopecheck==True):
        #print('reference true case')
        mp1=midpointCalc(array[0],array[1])
        mp2=midpointCalc(array[2],array[3])
        
        lenreal=8.6 #inches
        lenpixref=dist.euclidean(mp1,mp2)
       	pixelsPerMetric = lenpixref / lenreal
        print('pixels per metric',pixelsPerMetric)
        width=(dist.euclidean(array[0],array[1])/pixelsPerMetric)
        cv2.line(ti,(array[0][0],array[0][1]),(array[1][0],array[1][1]),(255,0,0),5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(width)[:4],(array[0][0]+10,array[0][1]+15), font, 4,(0,0,0),12,cv2.LINE_AA)
        print('width of strip',width)
        return pixelsPerMetric
        
    elif (orientation==2 and slopecheck==False) or ( orientation==1 and slopecheck==False):
        #print('reference false case')
        mp1=midpointCalc(array[0],array[3])
        mp2=midpointCalc(array[1],array[2])
       	lenpixref=dist.euclidean(mp1,mp2)
        #print('len pix',lenpixref)
        pixelsPerMetric = lenpixref / lenreal
        print('pixels per metric',pixelsPerMetric)
        width=(dist.euclidean(array[0],array[3])/pixelsPerMetric)
        cv2.line(ti,(array[0][0],array[0][1]),(array[3][0],array[3][1]),(255,0,0),5)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(width)[:4],(array[0][0]+10,array[0][1]+15), font, 4,(0,0,0),12,cv2.LINE_AA)
        print('width of strip',width)
        return pixelsPerMetric


# Object dimension estimator


def objectSizeEstimation(ti,array,refer,outputPath,lenreal):
    orientation=checkOrientation(array)
    slopecheck= direction(array)
    pixelsPerMetric=refrenceSizeEstimator(ti,refer,lenreal)

    if (orientation==2 and slopecheck==True) or ( orientation==1 and slopecheck==True):
        #print("object true case")
        #width Estimation
        mp1=midpointCalc(array[0],array[3])
        mp2=midpointCalc(array[1],array[2])
        widthpix=dist.euclidean(mp1,mp2)
        width=widthpix/pixelsPerMetric
        
        #length Estimation
        mp1=midpointCalc(array[0],array[1])
        mp2=midpointCalc(array[2],array[2])
        length=(dist.euclidean(mp1,mp2)/pixelsPerMetric)
        print("length of object",length)
        print("width of object",width)
        
        cv2.line(ti,(array[0][0],array[0][1]),(array[3][0],array[3][1]),(255,0,0),10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(length)[:4],((array[3][0]+array[0][0])//2,(array[3][1]+array[0][1])//2), font, 6,(0,0,255),3,cv2.LINE_AA)
        
        cv2.line(ti,(array[0][0],array[0][1]),(array[1][0],array[1][1]),(255,0,0),10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(width)[:4],((array[0][0]+array[1][0])//2,(array[0][1]+array[1][1])//2), font, 6,(0,0,255),3,cv2.LINE_AA)
        cv2.imwrite(outputPath,ti)
        
    elif (orientation==2 and slopecheck==False) or ( orientation==1 and slopecheck==False):
        #print("object false case")
        mp1=midpointCalc(array[0],array[1])
        mp2=midpointCalc(array[2],array[3])
        
        widthpix=dist.euclidean(mp1,mp2)
        width=widthpix/pixelsPerMetric
        
        #length estimation
        mp1=midpointCalc(array[0],array[3])
        mp2=midpointCalc(array[2],array[1])
        #length=(dist.euclidean(mp1,mp2)/pixelsPerMetric)
        length=dist.euclidean(array[0],array[1])/pixelsPerMetric
        print("length of object",length)
        print("width of object",width)
        
        cv2.line(ti,(array[0][0],array[0][1]),(array[3][0],array[3][1]),(255,0,0),10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(width)[:4],((array[3][0]+array[0][0])//2,(array[3][1]+array[0][1])//2), font, 6,(0,0,255),3,cv2.LINE_AA)
        
        cv2.line(ti,(array[0][0],array[0][1]),(array[1][0],array[1][1]),(255,0,0),10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(ti,str(length)[:4],((array[0][0]+array[1][0])//2,(array[0][1]+array[1][1])//2), font, 6,(0,0,255),3,cv2.LINE_AA)
        cv2.imwrite(outputPath,ti)

