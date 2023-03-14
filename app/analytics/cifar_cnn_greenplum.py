import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger().addHandler(logging.FileHandler(f"app.log"))

from app.analytics import preloader, cifar_cnn
import greenplumpython


# ## Upload dataset

# Upload dataset to S3 via MlFlow
def upload_dataset(dataset, dataset_url=None):
    return cifar_cnn.upload_dataset(dataset, dataset_url)


# ## Download DataSet
def download_dataset(artifact):
    return cifar_cnn.download_dataset(artifact)


# ## Train Model
def train_model(model_name, model_flavor, model_stage, data, epochs=10):
    return cifar_cnn.train_model(model_name, model_flavor, model_stage, data, epochs)


# ## Evaluate Model
def evaluate_model(model_name, model_flavor):
    return cifar_cnn.evaluate_model(model_name, model_flavor)


# ## Promote Model to Staging
def promote_model_to_staging(base_model_name, candidate_model_name, evaluation_dataset_name, model_flavor,
                             use_prior_version_as_base=False):
    """
    Evaluates the performance of the currently trained candidate model compared to the base model.
    The model that performs better based on specific metrics is then promoted to Staging.
    """
    return cifar_cnn.promote_model_to_staging(base_model_name, candidate_model_name, evaluation_dataset_name, model_flavor,
                                              use_prior_version_as_base)


# ## Make Prediction
def predict(img, model_name, model_stage):
    cifar_cnn.predict(img, model_name, model_stage)