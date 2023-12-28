from app.analytics import cifar_cnn
import sys
cifar_cnn.evaluate_model(model_name=sys.argv[1], model_flavor=sys.argv[2])
