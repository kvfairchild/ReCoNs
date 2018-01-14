# Function approximator

**Takes images of handwritten algebra functions as input and outputs the numeric value of the evaluated function.** 

This is a showcase program for [Request Confirmation Networks (ReCoNs)](https://pdfs.semanticscholar.org/a7ac/e80b84c64329501a3a9906314c80c3614997.pdf), an experimental network architecture designed to model neural execution of sensorimotor scripts.

![Image](https://github.com/kvgallagher/nodenet/blob/master/data/datasets/functions/function_data/0+1*2+3.png?raw=true)

A function image is first parsed into images of its component digits and symbols. These subcomponent images are then prepped according to [MNIST preprocessing directives](http://yann.lecun.com/exdb/mnist/) and fed into an *n*-layer perceptron pretrained on a combination of MNIST and mathematical operators (+, -, ×, ÷) adapted from [this Kaggle handwritten math symbols dataset](https://www.kaggle.com/xainano/handwrittenmathsymbols).

The perceptron returns the predicted values for each function's digits and symbols in an array representing that function.  This array is used to build a ReCoN that renders the function in its structure:

<img src="https://github.com/kvgallagher/nodenet/blob/master/images/ReCoN%20structure.png" alt="recon structure" raw=true height="50%" width="50%">

Activation spreads through the ReCoN based on a hierarchical system of requests and confirmations.  Node pairs are connected by a pair of "sub/sur" links, denoting a parent/child relationship, or a pair of "por/ret" links, denoting a predecessor/successor relationship.

Parent nodes request confirmation from their child nodes via "sub" links, and receive in return a "wait" signal, followed by either confirmation or failure of the request via "sur" links.  A successor node that requires confirmation from predecessor nodes before executing its own sequence will receive an "inhibit request" signal via "por" links until that confirmation is available, and will send back an "inhibit confirm" signal via "ret" links while its sequence executes. 

At any time, ReCoN nodes can have one of the following states: inactive, requested, active, suppressed, waiting, true, confirmed, failed.

The last unit in a sequence will validate a parent request by changing its state to "confirmed", or it will fail and change its state to "failed".  In this implementation, each sequence represents an operation in the function expressed by the ReCoN, and the last unit of each sequence represents either a digit or symbol operator.

The final output of the program is the numeric value of the function, which is currently evaluated from left to right without regard for operator precedence.  In the example function, 0+1×2+3, if all digits and symbols have been correctly identified, program output will be 5.  


![Image](https://github.com/kvgallagher/nodenet/blob/master/images/learned_images.png?raw=true)
\
*Learned images derived from the weights of a trained 2-layer [784,60,14] classifier.*

## Run

Requires [dill](https://pypi.python.org/pypi/dill), which can be quickly acquired via `pip`:

    pip install dill  

Use the following command to build and run a function approximator:

#### ./main.py

Available pretrained classifiers:

* 784,240,60,14 *(~94.5% accuracy)*
* 784,60,14 *(~93.3% accuracy)*
* 784,14 *(~89.3% accuracy)*

The default is set to a 3-layer classifier with 784 input nodes, 60 hidden nodes, and 14 output nodes representing digits 0-9 and algebra operators +, -, ×, ÷.

Number of layers and number of nodes per layer can be set in main.py:

    network_dimensions = [784, 60, 14]

Uncomment the following code block in nodenet/control.py to create a folder of final learned representations (works for 2 layers only):

	# # print images of final learned digits
	# if run_type == "test" and image_index == 0:
	# 	_create_images(nodenet)

## Dataset Creation

In `data/datasets/math_ops` is a file named `math_ops_data_prep.py` that takes in two (train/test) folders of images depicting handwritten math operation symbols derived from [this Kaggle handwritten math symbols dataset](https://www.kaggle.com/xainano/handwrittenmathsymbols) and generates two sets of numpy arrays: testing and training data and their respective one hot encoded labels. Labels are based on filename start character. 

In `data/datasets/functions` is a file named `symbols_image_prep.py` that takes in a folder of images depicting handwritten algebra functions and splits them into individual images of their component symbols. Images are prepared [MNIST-style](http://yann.lecun.com/exdb/mnist/): 20x20 symbols centered on a 28x28 canvas.

## Unit Test
#### python -m unittest discover -v

(Requires mock 1.0.1)
