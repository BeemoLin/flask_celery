import numpy
import os, datetime
import gc
from sklearn.model_selection import train_test_split
from absl import app, flags, logging
from yolov4.tf import YOLOv4, SaveWeightsCallback
from tensorflow.keras import callbacks, optimizers, backend
from numba import cuda

def predict():
    yolo = YOLOv4(tiny=True)
    yolo.classes = "./data/classes/coco.names"
    yolo.make_model()
    yolo.load_weights("./models/yolov4-tiny.weights", weights_type="yolo")
    # yolo.inference(media_path="./data/kite.jpg")
    yolo.inference(media_path="./data/road.mp4", is_image=False)

def dataset(data_path="./data/dataset/val2017.txt", train_path="./data/dataset/val2017_train.txt", test_path="./data/dataset/val2017_test.txt"): 

    with open(data_path, "rb") as f:
        data = str(f.read(), encoding="utf-8").split("\n")
        data = numpy.array(data)  #convert array to numpy type array
    print(len(data))
    x_train ,x_test = train_test_split(data,test_size=0.5)
    
    # x_train = '\n'.join(x_train)
    # x_test = '\n'.join(x_test)

    with open(train_path, "w") as txt_file:
        txt = '\n'.join(x_train)
        txt_file.write(txt)

    with open(test_path, "w") as txt_file:
        txt = '\n'.join(x_test)
        txt_file.write(txt)

    return train_path, test_path

def clear_gpu():
    cuda.select_device(0)
    cuda.close()

def create_log_dir():
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def get_log_path(log_dir):
    return os.path.join("./models/logs/fit/", log_dir)

def get_train_log_path(log_dir):
    return os.path.join(get_log_path(log_dir), "training.log")

def training(log_dir, epochs = 1, lr = 1e-4):
    train_path, test_path = dataset()

    yolo = YOLOv4(tiny=True)
    yolo.classes = "./data/classes/coco.names"
    yolo.input_size = 608
    yolo.batch = 32
    
    yolo.make_model(activation1="relu")
    yolo.load_weights(
        "./models/yolov4-tiny.weights",
        weights_type="yolo"
    )

    train_data_set = yolo.load_dataset(
        train_path,
        image_path_prefix="./data/dataset/val2017",
        label_smoothing=0.05
    )

    val_data_set = yolo.load_dataset(
        test_path,
        image_path_prefix="./data/dataset/val2017",
        training=False
    )

    optimizer = optimizers.Adam(learning_rate=lr)
    yolo.compile(optimizer=optimizer, loss_iou_type="ciou")

    def lr_scheduler(epoch):
        if epoch < int(epochs * 0.5):
            return lr
        if epoch < int(epochs * 0.8):
            return lr * 0.5
        if epoch < int(epochs * 0.9):
            return lr * 0.1
        return lr * 0.01

    if log_dir is None:
        log_dir = create_log_dir()

    log_path = get_log_path(log_dir)
    
    _callbacks = [
        callbacks.LearningRateScheduler(lr_scheduler),
        callbacks.TerminateOnNaN(),
        callbacks.TensorBoard(
            log_dir=log_path,
        ),
        SaveWeightsCallback(
            yolo=yolo, dir_path="./models",
            weights_type="yolo", epoch_per_save=1
        ),
        callbacks.CSVLogger(get_train_log_path(log_dir)),
    ]

    yolo.fit(
        train_data_set,
        epochs=epochs,
        callbacks=_callbacks,
        validation_data=val_data_set,
        validation_steps=1,
        validation_freq=1,
        steps_per_epoch=10,
    )

    del yolo
    backend.clear_session()
    gc.collect()

    return

# def main(_argv):
#     # x, y = dataset()
#     training()

# if __name__ == '__main__':
#     try:
#         app.run(main)
#     except SystemExit:
#         pass