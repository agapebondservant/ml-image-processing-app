from app.analytics import cifar_cnn_greenplum
import sys
cifar_cnn_greenplum.evaluate_model(model_name=sys.argv[1], model_flavor=sys.argv[2])