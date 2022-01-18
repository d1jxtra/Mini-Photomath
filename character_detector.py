import cv2
import numpy as np


def character_detector(image):
    """returns list of characters detected from image of equation in np.array form"""
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = gray.shape
    area = height*width
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    thresh_size = int(height/6)
    thresh_size = thresh_size if thresh_size%2 else thresh_size+1
    thresh = cv2.adaptiveThreshold(blurred,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,thresh_size,5)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]


    #Taking boundaries of contours that are big enough
    boundaries=[]
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if w>0.07*height or h>0.1*height:
            boundaries.append((x,y,w,h))

    boundaries = sorted(boundaries)

    #We remove contour of picture edge if it exists
    if boundaries[0][0]==0 and boundaries[0][1]==0:
        del(boundaries[0])

    #Some contours can be part of already existing contours. For example 2 circles in number 8. We remove those.
    indices=[]
    for i in range(len(boundaries)):
        for j in range(i):
            if j in indices:
                continue
            x_in = (boundaries[i][0]>boundaries[j][0]) and (boundaries[i][0]+boundaries[i][2]<boundaries[j][0]+boundaries[j][2])
            y_in = (boundaries[i][1]>boundaries[j][1]) and (boundaries[i][1]+boundaries[i][3]<boundaries[j][1]+boundaries[j][3])
            if x_in and y_in:
                indices.append(i)

    ba = np.asarray(boundaries)
    ba = np.delete(ba,indices,0)
    characters=[thresh[ba[i,1]:ba[i,1]+ba[i,3],ba[i,0]:ba[i,0]+ba[i,2]] for i in range(ba.shape[0])]
    
    return characters


def ImageToSquare(image: np.ndarray):
    """Adding padding to an image to make it square"""
    
    height = image.shape[0]
    width = image.shape[1]
    if height==width:
        pass
    
    diff = max(height, width) - min(height, width)
    size = int(diff/2)
    
    if height>width:
        padding = np.zeros((height, size))
        square=np.hstack((padding, image, padding))
    else:
        padding = np.zeros((size, width))
        square = np.vstack((padding, image, padding))
    
    return square

def ImageResizer(image: np.ndarray, dimensions: (int,int)):
    """Resizing image to given dimensions"""
    resized = cv2.resize(image.astype('uint8'), (28,28), interpolation = cv2.INTER_AREA) 
    return resized

def ImageToBinary(image: np.ndarray):
    """Converting image to look as an image from training set"""
    
    # because training set contains two types of value we transform resized picture in that way
    _,binary=cv2.threshold(image,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # scaling to 0,1
    image= binary/255.0
    
    return image


# class for transforming image to list of characters
class CharacterTransformer:
    def __init__(self, dim: int):
        self.dim = dim
        
    def transform_one(self, image: np.ndarray):
        square = ImageToSquare(image)
        resized = ImageResizer(square, (self.dim,self.dim))
        transformed = ImageToBinary(resized)
        return transformed

    def transform(self, images):
        return [self.transform_one(image) for image in images]

