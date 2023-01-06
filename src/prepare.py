from pathlib import Path

import pandas as pd

# Generate a csv to look like this

# filename, label
# full/path/to/data-version-control/raw/n03445777/n03445777_5768.JPEG,golf ball
# full/path/to/data-version-control/raw/n03445777/n03445777_5768,golf ball
# full/path/to/data-version-control/raw/n03445777/n03445777_11967.JPEG,golf ball

FOLDERS_TO_LABELS = {"n03445777": "golf ball", "n03888257": "parachute"}

#  Get a list of a the file name and all the labels of data path
def get_files_and_labels(source_path):
    images = []
    labels = []
    for image_path in source_path.rglob("*/*.JPEG"):
        filename = image_path.absolute()
        folder = image_path.parent.name
        if folder in FOLDERS_TO_LABELS:
            images.append(filename)
            label = FOLDERS_TO_LABELS[folder]
            labels.append(label)
    return images, labels

#Save them as a csv
def save_as_csv(filenames, labels, destination):
    data_dictionary = {"filename": filenames, "label": labels}
    data_frame = pd.DataFrame(data_dictionary)
    data_frame.to_csv(destination)


def main(repo_path):
    data_path = repo_path / "data"
    train_path = data_path / "raw/train"
    test_path = data_path / "raw/val"
    train_files, train_labels = get_files_and_labels(train_path)
    test_files, test_labels = get_files_and_labels(test_path)
    prepared = data_path / "prepared"
    save_as_csv(train_files, train_labels, prepared / "train.csv")
    save_as_csv(test_files, test_labels, prepared / "test.csv")


if __name__ == "__main__":
    repo_path = Path(__file__).parent.parent
    main(repo_path)
