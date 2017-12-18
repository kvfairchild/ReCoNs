# Function approximator

**Takes images of handwritten algebra functions as input and outputs the numeric value of the evaluated function.** 

![Image](https://github.com/kvgallagher/nodenet/blob/master/data/datasets/functions/function_data/0+1*2+3.png?raw=true)

A function image is first parsed into images of its component digits and symbols, which are then prepped according to [MNIST preprocessing directives](http://yann.lecun.com/exdb/mnist/) and fed into an *n*-layer perceptron pretrained on a combination of MNIST and mathematical operators (+, -, ×, ÷) adapted from [this Kaggle handwritten math symbols dataset](https://www.kaggle.com/xainano/handwrittenmathsymbols).

The perceptron returns the predicted values of each function's digits and symbols in an array for that function.  This array is used to build a [Request Confirmation Network (ReCoN)](https://pdfs.semanticscholar.org/a7ac/e80b84c64329501a3a9906314c80c3614997.pdf) that represents the function in its structure:

![Image](https://github.com/kvgallagher/nodenet/blob/master/ReCoN_structure_example.png?raw=true)

ReCoNs are an experimental network architecture designed to model neural execution of sensorimotor scripts.  

## Run

Requires [dill](https://pypi.python.org/pypi/dill), which can be quickly acquired via `pip`:

    pip install dill  

Use the following command to build and run a function approximator:

#### ./main.py

Available pretrained classifiers:

* 784,240,60,14 *()*
* 784,60,14 *(93.29% accuracy)*
* 784,14 *(89.3% accuracy)*

The default is set to a 3-layer classifier with 784 input nodes, 60 hidden nodes, and 14 output nodes representing digits 0-9 and algebra operators +, -, ×, ÷.

Number of layers and number of nodes per layer can be set in main.py:

    network_dimensions = [784, 60, 14]

Uncomment the following code block in nodenet/control.py to create a folder of final learned representations (works for 2 layers only):

	# # print images of final learned digits
	# if run_type == "test" and image_index == 0:
	# 	_create_images(nodenet)

## Unit Test
#### python -m unittest discover -v

(Requires mock 1.0.1)
