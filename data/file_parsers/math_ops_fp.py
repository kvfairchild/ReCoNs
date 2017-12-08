import numpy as np
import os

def read(dataset = "training", path = os.path.abspath("data/datasets/math_ops")):

    if dataset is "training":
        image_file = os.path.join(path, "ops_train_data.npy")
        label_file = os.path.join(path, "ops_train_labels.npy")
    elif dataset is "testing":
        image_file = os.path.join(path, "ops_test_data.npy")
        label_file = os.path.join(path, "ops_test_labels.npy")
    else:
        raise ValueError, "dataset must be 'testing' or 'training'"

    return {
        "images": _extract_images(image_file),
        "labels": _extract_labels(label_file)
    }

def _extract_images(image_file):
    file = np.load(image_file)
    return file

def _extract_labels(label_file):
    file = np.load(label_file)
    return file
