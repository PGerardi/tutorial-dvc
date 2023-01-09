# Data Version Control Tutorial

Example repository for Data Version Control

Clone the forked repository to your computer with the `git clone` command

```console
git clone git@gitlab.portofantwerp.com:data-analytics/data-science/tutorial-data-vesion-control.git
```

Happy coding!


# Tutorial

## Set-up project

1. Set-up virtual environment

    ```sh
    pip install virtualenv
    virtualenv tutorial-data-version-control
    source tutorial-data-version-control/venv/bin/activate
    pip -r requirements.txt
    ```

2. Make change to the virtual environment
    ```sh
    python -m pip install dvc scikit-learn scikit-image pandas numpy
    pip freeze > requirements.txt
    ```

3. Download the data
    ```sh
    curl https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz -O imagenette2-160.tgz
    mv imagenette2-160/train data/raw/train
    mv imagenette2-160/val data/raw/val
    rm -rf imagenette2-160
    rm imagenette2-160.tgz
    ```


## Set-up dvc

1.  Initialize dvc
    ```sh
    dvc init
    ```
2. Create container in Azure storage account.

3. Connect to the dvc remote
    ```sh
    dvc remote add -d remote_storage azure://tutorialpierre
    dvc remote modify remote_storage account_name 'pocazureml7275011038'
    dvc remote modify --local remote_storage connection_string '<connection_string>'
    ```

   
## Add data to dvc control

1. Add data to dvc control
   ```sh
    dvc add data/raw/train
    dvc add data/raw/val
    ```
2. add dvc to git control
    ```sh
    git add .
    git commit -m 'feat: add dvc integration'
    ```
    
3. Push the data to the remote storage
    ```sh
    dvc push
    ```

## Manual process
### First experiment
1. Perform prepare step
    ```sh
    python src/prepare.py
    dvc add data/prepared/train.csv data/prepared/test.csv
    git add .
    git commit -m "Created train and test CSV files"
    ```

2. Perform train step
   ```sh
    python src/train.py
    dvc add model/model.joblib
    git add .
    git commit -m "Trained an SGD classifier"
    ```

3. Perfrom evaluate step
   ```sh
    python src/evaluate.py
    git add .
    git commit -m "Evaluate the SGD model accuracy"
    ```

4. Push to git and dvc
   ```sh
   git push
   dvc push
   git tag -a sgd-classifier -m "SGDClassifier with accuracy 67.06%"
   ```

### Second experiment (100 iterations)
It is good practice to create a seperate branch for every experiment.

1. Checkout to new branch
    ```sh
    git checkout -b "sgd-100-iterations"
    ````
2. Change hyperparameter in train.py
3. Execute the training and evaluation step
    ```sh
    python src/train.py
    python src/evaluate.py
    ```
4. Commit the change model in dvc (stores data in cache and change dvc lock files)
    ```sh
    dvc commit
    ```
5. Commit the model in git
    ```sh
    git add .
    git commit -m "Change SGD max_iter to 100" 
    ```

6. Tag and push
    ```sh
    git tag -a sgd-100-iter -m "Trained an SGD Classifier for 100 iterations"
    git push origin --tags

    git push --set-upstream origin sgd-100-iter
    dvc push

    ```
7. Swith to previous model
    ```sh
    git checkout main
    dvc checkout
    ```

## Create a reproducible pipeline
You fetched the data manually and added it to remote storage. 
You can now get it with dvc checkout or dvc pull. 
The other steps were executed by running various Python files. 
These can be chained together into a single execution called a DVC pipeline that requires only one command.

1. New branch
    ```sh
    git checkout -b sgd-pipeline
    ```
2. Remove dvc tracking from the output files
    ```sh
    dvc remove data/prepared/train.csv.dvc \
        data/prepared/test.csv.dvc \
        model/model.joblib.dvc --outs
    ```
3. Create pipeline stages:
   1. Prepare stage
        ```sh
        dvc run -n prepare \
            -d src/prepare.py -d data/raw \
            -o data/prepared/train.csv -o data/prepared/test.csv \
            python src/prepare.py
        ```

    2. Train stage
        ```sh
        dvc run -n train \
            -d src/train.py -d data/prepared/train.csv \
            -o model/model.joblib \
            python src/train.py
        ```

    3. Train stage
        ```sh
        dvc run -n evaluate \
            -d src/evaluate.py -d model/model.joblib \
            -M metrics/accuracy.json \
            python src/evaluate.py
        ```
4. Add pipeline to git
    ```sh
    git add .
    git commit -m "Rerun SGD as pipeline"
    dvc commit
    git push --set-upstream origin sgd-pipeline
    git tag -a sgd-pipeline -m "Trained SGD as DVC pipeline."
    git push origin --tags
    dvc push
    ```
    
5. Make change to the pipeline
    ```sh
    git checkout -b "random_forest"
    ```

6. CHANGE to random forrest => DETECT THE CHANGE
    ```sh
    dvc status
    ```
7. Execute pipeline
    ```sh
    dvc repro
    ```

8.  add to git
    ```sh
    git add .
    git commit -m "Train Random Forrest classifier"
    dvc commit
    git push --set-upstream origin random-forest
    git tag -a random-forest -m "Random Forest classifier with 80.99% accuracy."
    git push origin --tags
    dvc push
    ```

9. Compare the runs
    ```sh
    dvc metrics show -T
    ```






