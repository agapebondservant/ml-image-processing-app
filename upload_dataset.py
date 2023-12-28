from app.analytics import cifar_cnn_greenplum, mlflow_utils
import mlflow
import sys
mlflow_utils.start_new_root_run()
cifar_cnn_greenplum.upload_dataset(dataset=sys.argv[1])