from app.analytics import cifar_cnn, mlflow_utils
import sys

mlflow_utils.start_new_root_run()
cifar_cnn.upload_dataset(dataset=sys.argv[1])
