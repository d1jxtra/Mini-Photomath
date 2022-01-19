# Mini Photomah
---
## Description
---
Returning result from an image of math expression. It is done in 3 steps:
- Detecting characters from the image of an expression
- Building model that classifies recognised characters
- Evaluating mathematical expression

**NOTE**
Expression can consist of digits and operators for addition, subtraction, multiplication, division and brackets. Because of images used in training model for character recognition, you should use following symbols for operators: `+, -, *, /, [, ]`
(! Notice that square brackets should be used).

## How to use
---
This project was made with Python 3.7. You can install all the required packages with
```sh
pip install -r requirements.txt
```
Clone this git repository and inside create a new folder with the name  `app images`. This is where the app will save uploaded images.

**Option 1.**
Run `app.py` from this directory:
```sh
python app.py
```
Visit localhost provided in command line output in your browser. App instructions are given in app itself.

**Option 2**
Run jupyter notebook `Mali Photomath.ipynb`. You can upload your own image path and run through the cells to get better understanding what is done with the image. 


## Files description
---

`character_detector.py` - detecting characters from image of math expression
`parser_and_solver.py` - parsing string of math expression and solving it
`character classifier.ipynb` - jupyter notebook where CNN model for character recognision is built and trained
`character classifier2.ipynb` - same model as in previous file but trained on bigger dataset 
`models/` - folder containing saved models for character classification
`app.py` - flask app that lets you upload image of expression and returns its result
`templates/` - HTML file needed for `app.py`
`equations/` - examples of test images you can try

## Data
---
https://www.kaggle.com/michelheusser/handwritten-digits-and-operators
**Note**
`models/model_1.hp5` uses only validation dataset. Train, test and validation sets are split from it.
`models/model_2.hp5` uses all the data already split.

Even though `models/model_2.hp5` uses more data to train and produces higher accuracy on test set, I found that `models/model_1.hp5` classifies better in practice. So `app.py` and `Mali Photomath.ipynb` use `models/model_1.hp5` for predictions. If u want to try other model, change loaded model in those programs.

