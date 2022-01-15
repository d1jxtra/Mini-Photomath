import cv2
import numpy as np


def character_detector(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    
    kernel = np.ones((3, 3), np.uint8)
    img_eroded = cv2.erode(thresh1, kernel, iterations = 1)
    
    contours, hierarchy = cv2.findContours(img_eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    boundaries=[]
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        boundaries.append((x,y,w,h))
    boundaries_array=np.asarray(boundaries)
    bs=boundaries_array[boundaries_array[:,0].argsort()]  #boundaries_array sortirana po x-evima
    characters=[thresh1[bs[i,1]:bs[i,1]+bs[i,3],bs[i,0]:bs[i,0]+bs[i,2]] for i in range(bs.shape[0])]
    
    return characters


def ImageToSquare(image: np.ndarray):
    height = image.shape[0]
    width = image.shape[1]
    if height==width:
        pass
    
    diff = max(height, width) - min(height, width)
    size = int(diff/2)
    
    if height>width:
        padding = np.full((height, size),255)
        square=np.hstack((padding, image, padding))
    else:
        padding = np.full((size, width),255)
        square = np.vstack((padding, image, padding))
    
    return square


def ImageResizer(image: np.ndarray, dimensions: (int,int)):
    temp = cv2.resize(image.astype('uint8'), (28,28), interpolation = cv2.INTER_AREA) 
    # s obzirom da slike za treniranje imaju samo dvije vrste piksela tako transformiramo i danu sliku
    _,binary=cv2.threshold(temp,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return binary


def ImageToBinary(image: np.ndarray):
    image = cv2.bitwise_not(image.astype('uint8'))
    image = image/255.0
    return image



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

