import cv2
import numpy as np
from character_detector import character_detector, CharacterTransformer
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
import pickle
from parser_and_solver import parse_and_solve

app = Flask(__name__)

model = load_model('models/model_1.h5')
with open("codes", "rb") as fp:   
    codes = pickle.load(fp)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    imagefile = request.files['imagefile']
    image_path = "./app images/" + imagefile.filename
    imagefile.save(image_path)
    
    image = cv2.imread(image_path)
    characters = character_detector(image)
    dim = 28
    transformer = CharacterTransformer(dim)
    chars=transformer.transform(characters)
    
    equation=""
    for i in range(len(chars)):
        prediction = model.predict(chars[i].reshape((dim,dim,1))[np.newaxis])
        label=codes[np.argmax(prediction)]
        equation+=label
    
    equation = equation.replace('[','(').replace(']',')')
    evaluation = parse_and_solve(equation)
    equation = equation + ' = ' + str(evaluation)
    
    return render_template('index.html', equation = equation)

if __name__ == "__main__":
    app.run(debug = True)