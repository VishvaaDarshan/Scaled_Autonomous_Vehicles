import os
import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras import backend as K
from keras.models import Model, Sequential
from keras.layers import Dense, GlobalAveragePooling2D, MaxPooling2D, Lambda, Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.core import Flatten, Dense, Dropout, SpatialDropout2D
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.layers import LSTM
from keras.layers.wrappers import TimeDistributed as TD

import sklearn
from sklearn.model_selection import train_test_split

import toolz
from toolz.itertoolz import sliding_window

def create_sequence(size,data):
    sequence = list(sliding_window(size, data))
    sequence = np.array(sequence)
    return sequence

seq = []
seq_length = 3
count = 0
seq_count = 0
sequences = []

with open('/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/interpolated.csv') as csvfile:
    reader = csv.reader(csvfile)
    row_count = sum(1 for row in reader)

samples = []
with open('/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/interpolated.csv') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        samples.append(line)

# sklearn.utils.shuffle(samples)
train_samples, validation_samples = train_test_split(samples, shuffle=False, test_size=0.2)

train = create_sequence(seq_length, train_samples)
test = create_sequence(seq_length, validation_samples)

print("Number of traing samples: ", (train.shape))
print("Number of validation samples: ", (test.shape))

#   if count == row_count-seq_length-1:
#     # print(count)
#     break

#   seq.append(line)
#   if len(seq) == 3:
#     sequences.append(seq)
#     seq = []

# print(len(sequences))


#         samples.append(line)

# sklearn.utils.shuffle(samples)
# train_samples, validation_samples = train_test_split(samples, test_size=0.3)

# print("Number of traing samples: ", len(train_samples))
# print("Number of validation samples: ", len(validation_samples))
# /home/ajith/sav_ws/src/diy_driverless_car_ROS/rover_ml/utils/center
big_arr = np.arange(32*3*180*320*3).reshape(32,3,180,320,3)

def generator(samples, batch_size, aug):
    num_samples = len(train)
    small_arr = np.arange(3*180*320*3).reshape(3,180,320,3)
    global big_arr

    while 1:

        for offset in  range(0, num_samples, batch_size):
            batch_samples = train[offset:offset + batch_size]                           #array of seq
            inputs = []
            count2 = 0
            for batch_sample in batch_samples:                                          #seq in seqs
                # print("c2", count2)
                count1 = 0
                for image in batch_sample:                                              #img in seq
                    if image[5] != "filename":
                        # print("c1",count1)
                        path = os.path.normpath(image[5]).split(os.path.sep)
                        name = '/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/center/'+path[1].split('\\')[-1]
            
                        center_image = cv2.imread(name)
                        center_image = cv2.resize(center_image, (320,180))
                        small_arr[count1] = center_image
                        count1 += 1
                
                big_arr[count2] = small_arr
                count2 += 1
                angle = float(batch_sample[-1][6])
                speed = float(batch_sample[-1][7])
                choice = [angle, speed]
                inputs.append(choice)
            # print("bigarrayshape", big_arr.shape)
            y_train = np.array(inputs).reshape(batch_size,2)
            # print(big_arr[0][0])
            yield (big_arr, y_train)


# compile and train the model using the generator function
batch_size = 32
n_epoch = 2
batch_size_value = batch_size

train_generator = generator(train_samples, batch_size=batch_size_value, aug=0)
validation_generator = generator(validation_samples, batch_size=batch_size_value, aug=0)

img_shape=(180,320,3)
img_seq_shape = (seq_length,) + img_shape
# print(img_seq_shape)
#img_in = Input(batch_shape = img_seq_shape, name='img_in')

model = Sequential()
# trim image to only see section with road
model.add(TD(Cropping2D(cropping=((75,0), (0,0))), input_shape=img_seq_shape))
#LSTM model
model.add(TD(Convolution2D(24, (5, 5), activation="relu", name="conv_1", strides=(2, 2))))
model.add(TD(Convolution2D(36, (5, 5), activation="relu", name="conv_2", strides=(2, 2))))
model.add(TD(Convolution2D(48, (5, 5), activation="relu", name="conv_3", strides=(2, 2))))
#model.add(SpatialDropout2D(.5, dim_ordering='default'))
model.add(TD(Convolution2D(64, (3, 3), activation="relu", name="conv_4", strides=(2, 2))))
model.add(TD(Convolution2D(64, (3, 3), activation="relu", name="conv_5", strides=(1, 1))))

model.add(TD(MaxPooling2D(pool_size=(2, 2))))

model.add(TD(Flatten(name='flattened')))

model.add(TD(Dense(100, activation='relu')))
model.add(TD(Dropout(.1)))

model.add(LSTM(128, return_sequences=True, name="LSTM_seq"))
model.add(Dropout(.1))
model.add(LSTM(128, return_sequences=False, name="LSTM_out"))
model.add(Dropout(.1))
model.add(Dense(128, activation='relu'))
model.add(Dropout(.1))
model.add(Dense(64, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(2, activation='linear', name='model_outputs'))

model.compile(optimizer='rmsprop', loss='mse')
model.summary()

filepath="/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/weights/weights-improvement-{epoch:02d}-{val_loss:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='auto', period=1)

early_stop = EarlyStopping(monitor='val_loss', patience=10)

callbacks_list = [checkpoint, early_stop]

# Fit the model
history_object = model.fit_generator(train_generator, steps_per_epoch=(len(train_samples) / batch_size_value), validation_data=validation_generator, validation_steps=(len(validation_samples)/batch_size_value), callbacks=callbacks_list, epochs=n_epoch)

# Save model
model.save('/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/weights/model.h5')
with open('/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/weights/model.json', 'w') as output_json:
    output_json.write(model.to_json())

# Save TensorFlow model
tf.train.write_graph(K.get_session().graph.as_graph_def(), logdir='.', name='model.pb', as_text=False)

# Plot the training and validation loss for each epoch
print('Generating loss chart...')
plt.plot(history_object.history['loss'])
plt.plot(history_object.history['val_loss'])
plt.title('model mean squared error loss')
plt.ylabel('mean squared error loss')
plt.xlabel('epoch')
plt.legend(['training set', 'validation set'], loc='upper right')
plt.savefig('/home/prajval/end_to_end_learning/src/diy_driverless_car_ROS-master/rover_ml/output/weights/model.png')

# Done
print('Done.')



