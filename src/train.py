from joblib import dump
from pathlib import Path

import numpy as np
import pandas as pd
from skimage.io import imread_collection
from skimage.transform import resize
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier


# Load the images as a list, from a dataframe
def load_images(data_frame, column_name):
    filelist = data_frame[column_name].to_list()
    image_list = imread_collection(filelist)
    return image_list


#  Load the labels as a list, from a dataframe
def load_labels(data_frame, column_name):
    label_list = data_frame[column_name].to_list()
    return label_list


# preprocess the image, rescale and linearize
def preprocess(image):
    resized = resize(image, (100, 100, 3))
    reshaped = resized.reshape((1, 30000))
    return reshaped


# call the data
def load_data(data_path):
    df = pd.read_csv(data_path)
    labels = load_labels(data_frame=df, column_name="label")
    raw_images = load_images(data_frame=df, column_name="filename")
    processed_images = [preprocess(image) for image in raw_images]
    data = np.concatenate(processed_images, axis=0) 
    return data, labels

# RANDOM_FORREST_MODEL
# def main(path_to_repo):
#     train_csv_path = repo_path / "data/prepared/train.csv"
#     train_data, labels = load_data(train_csv_path)
#     rf = RandomForestClassifier()
#     trained_model = rf.fit(train_data, labels)
#     dump(trained_model, repo_path / "model/model.joblib")


# SGD_MODEL
def main(repo_path):
    train_csv_path = repo_path / "data/prepared/train.csv"
    train_data, labels = load_data(train_csv_path)
    sgd = SGDClassifier(max_iter=10)
    trained_model = sgd.fit(train_data, labels)
    dump(trained_model, repo_path / "model/model.joblib")


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
