from app.analytics import cifar_cnn
import hickle as hkl
import sys

dataset_path = cifar_cnn.download_dataset(artifact=sys.argv[1])
data = hkl.load(dataset_path)
cifar_cnn.train_model(model_name=sys.argv[2], model_flavor=sys.argv[3], model_stage=sys.argv[4], data=data, epochs=int(sys.argv[5]))
