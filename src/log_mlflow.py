import json
import os

import mlflow
from azureml.core import Workspace
from azureml.core.authentication import ServicePrincipalAuthentication


def mlflow_logging() -> None:
    """Log metrics and params in mlflow."""
    with open("metrics/accuracy.json") as metrics_file:
        metrics = json.load(metrics_file)
    metrics_file.close()
    mlflow.log_metrics(metrics)
    mlflow.log_param("model_type", "sgd")
    mlflow.log_param("iterations", 100)
    mlflow.log_artifact("dvc.lock")
    mlflow.log_artifact("metrics/accuracy.json")


with open(".azureml/config.json") as azure_config_file:
    azure_config = json.load(azure_config_file)
try:
    sv_user_id = os.environ["AZURE_CLIENT_ID"]
    sv_tenant_id = os.environ["AZURE_TENANT_ID"]
    sv_secret_password = os.environ["AZURE_CLIENT_SECRET"]
    svc_pr = ServicePrincipalAuthentication(
        tenant_id=sv_tenant_id,
        service_principal_id=sv_user_id,
        service_principal_password=sv_secret_password,
    )
    ws = Workspace.from_config(auth=svc_pr)

except KeyError:
    ws = Workspace.from_config()

azureml_mlflow_uri = ws.get_mlflow_tracking_uri()
mlflow.set_tracking_uri(azureml_mlflow_uri)
mlflow.set_experiment("tutorial_logging")
with mlflow.start_run() as mlflow_run:
    mlflow_logging()


