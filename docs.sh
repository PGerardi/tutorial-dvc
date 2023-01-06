# Setting up the virtualenv

pip install virtualenv
virtualenv myproject
source tutorial-data-version-control/venv/bin/activate
python -m pip install dvc scikit-learn scikit-image pandas numpy
pip freeze > requirements.txt

# Use the virtualenv
pip -r requirements.txt

# The docs url
https://realpython.com/python-data-version-control/#share-a-development-machine


# Download the training data

curl https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz -O imagenette2-160.tgz
mv imagenette2-160/train data/raw/train
mv imagenette2-160/val data/raw/val
rm -rf imagenette2-160
rm imagenette2-160.tgz


# Set up dvc 
dvc init

Create a remote container in Azure

# Add the config to the remote container

dvc remote add -d remote_storage azure://tutorialpierre
dvc remote modify remote_storage account_name 'pocazureml7275011038'
# Copy the connection string
dvc remote modify --local remote_storage connection_string 'DefaultEndpointsProtocol=https;AccountName=pocazureml7275011038;AccountKey=AYg9Gq6i2AGK18uxPj7aRYlxVqdftm+BxilUogfLFFDQY7rqWPgtId4OPBiigDTZR8tvt9goNGSCyBa5fT2rKA==;EndpointSuffix=core.windows.net'




# dvc track the data

dvc add data/raw/train
dvc add data/raw/val

git add .
git commit -m 'feat: add dvc integration'
dvc push




# Prepare the data

python src/prepare.py
dvc add data/prepared/train.csv data/prepared/test.csv
git add .
git commit -m "Created train and test CSV files"
