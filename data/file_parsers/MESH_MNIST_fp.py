from __future__ import division
import os
import numpy as np

# Adapted from Tensorflow's MNIST tutorial data 
# https://github.com/tensorflow/tensorflow/blob/master/tensorflow/contrib/learn/python/learn/datasets/mnist.py) 

def _read32(bytestream):
    dt = np.dtype(np.uint32).newbyteorder('>')
    return np.frombuffer(bytestream.read(4), dtype=dt)[0]

def read(dataset = "train", path = os.path.abspath("data/datasets/MNIST")):

    if dataset is "train":
        image_file = os.path.join(path, 'train-images.idx3-ubyte')
        label_file = os.path.join(path, 'train-labels.idx1-ubyte')
    elif dataset is "test":
        image_file = os.path.join(path, 't10k-images-idx3-ubyte')
        label_file = os.path.join(path, 't10k-labels.idx1-ubyte')
    else:
        raise ValueError, "dataset must be 'test' or 'train'"

    return {
        "images": _extract_images(image_file),
        "labels": _extract_labels(label_file)
    }

def _extract_images(image_file):
    f = open(image_file, "rb")

    magic = _read32(f)
    if magic != 2051:
      raise ValueError('Invalid magic number %d in MNIST image file: %s' %
                       (magic, f.name))

    num_images = _read32(f)
    rows = _read32(f)
    cols = _read32(f)
    buf = f.read(rows * cols * num_images)
    data = np.frombuffer(buf, dtype=np.uint8)
    data = data.reshape(num_images, rows, cols)
    normalized_data = []
    for image in data:
        image = [pixel * float(1/255) for column in image for pixel in column]
        normalized_data.append(image)
    data = np.array(normalized_data)
    return data    

def _extract_labels(label_file):
    f = open(label_file, "rb")

    magic = _read32(f)
    if magic != 2049:
      raise ValueError('Invalid magic number %d in MNIST image file: %s' %
                       (magic, f.name))
    num_items = _read32(f)
    buf = f.read(num_items)
    labels = np.frombuffer(buf, dtype=np.uint8)
    return _one_hot(labels)

def _one_hot(labels):
    num_labels = labels.shape[0]
    index_offset = np.arange(num_labels) * 10
    labels_one_hot = np.zeros((num_labels, 10))
    labels_one_hot.flat[index_offset + labels.ravel()] = 1

    # add extra values for math operator labels
    labels_extended = []
    for i, label in enumerate(labels_one_hot):
        math_ops_label = np.zeros(4)
        label = np.append(label, [0, 0, 0, 0])

        labels_extended.append(label)
    return labels_extended

    
