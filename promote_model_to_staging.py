from app.analytics import cifar_cnn
import sys

cifar_cnn.promote_model_to_staging(base_model_name=sys.argv[1], candidate_model_name=sys.argv[2], evaluation_dataset_name=sys.argv[3], model_flavor=sys.argv[4])
