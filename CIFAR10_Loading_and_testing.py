#
#
# Initial tests on CIFAR10 data. how to read/load data and handle it.

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K
import matplotlib.pyplot as plt


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

def transform_CIFAR(cifar_file):
    y_label = cifar_file[b'labels']
    X_flat = cifar_file[b'data']
    X = [np.swapaxes(np.reshape(x, CIFAR_input_size, order='F'), 0, 1) for x in X_flat]
    y = y_label

    return X, y


def view_test_data(X_data, y_data):
    import random
    ncols = 10
    nrows = 5
    idx = random.sample(range(1, 9999), ncols*nrows)
    y_pred = model.predict(X_data[idx])
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
    ctr = 0
    for ax in axes.flatten():
        im = ax.imshow(X_data[idx[ctr]])
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        ax.set_title('Pred:' + str(np.argmax(y_pred[ctr])) + ' True:' + str(np.argmax(y_data[idx[ctr]])))
        ctr += 1
    fig.show()


# Hyper params
batch_size = 128
num_classes = 10
epochs = 1
CIFAR_input_size = (32, 32, 3)


# Read in the CIFAR data
cifar_path = './cifar-10-batches-py/'
X1, y1 = transform_CIFAR(unpickle(cifar_path + 'data_batch_1'))
X2, y2 = transform_CIFAR(unpickle(cifar_path + 'data_batch_2'))
X3, y3 = transform_CIFAR(unpickle(cifar_path + 'data_batch_3'))
X4, y4 = transform_CIFAR(unpickle(cifar_path + 'data_batch_4'))
X_val, y_val = transform_CIFAR(unpickle(cifar_path + 'data_batch_5'))

X_test, y_test = transform_CIFAR(unpickle(cifar_path + 'test_batch'))
X = X1 + X2 + X3 + X4
y = y1 + y2 + y3 + y4

# Convert data to 0-1 floats, and to categorical.
X = np.array(X1).astype('float32')
X /= 255
y = keras.utils.to_categorical(y1, num_classes=num_classes)

X_test = np.array(X_test).astype('float32')
X_test /= 255
y_test = keras.utils.to_categorical(y_test, num_classes=num_classes)

X_val = np.array(X_val).astype('float32')
X_val /= 255
y_val = keras.utils.to_categorical(y_val, num_classes=num_classes)


# Create a test model.
model = Sequential()
model.add(Conv2D(32, kernel_size=(3, 3), strides=(1, 1), activation='relu', input_shape=CIFAR_input_size))
model.add(Dropout(0.25))
model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

# Flat parts
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.50))
model.add(Dense(num_classes, activation='softmax'))

# Compile mdoel
model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])


model.fit(np.array(X), y, batch_size=batch_size, epochs=epochs, validation_data=(X_val, y_val))



score = model.evaluate(X_test, y_test, verbose=1)
print('')
print("Test loss:", score[0])
print("Test accuracy:", score[1])

view_test_data(X_test, y_test)
