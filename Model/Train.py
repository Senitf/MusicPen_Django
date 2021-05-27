from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

MODEL_SAVE = False
target_names = ['half', 'quarter', '8th', '16th',
                'dot_half', 'dot_quarter', 'dot_8th', 'dot_16th']

notes = np.load('Train_x.npy')
labels = np.load('Train_y.npy')

notes = notes.reshape((notes.shape[0], notes.shape[1],
                           notes.shape[2], 1))

X_train, X_test, y_train, y_test = train_test_split(
    notes, labels, test_size=0.25, random_state=42,
    stratify=labels)

y_train = to_categorical(y_train)
model = Sequential()

model.add(Conv2D(input_shape=(X_train.shape[1], X_train.shape[2], X_train.shape[3]),
                 filters=50,
                 kernel_size=(3, 3),
                 strides=(1, 1),
                 padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# prior layer should be flattend to be connected to dense layers
model.add(Flatten())
# dense layer with 50 neurons
model.add(Dense(50, activation='relu'))
# final layer with 10 neurons to classify the instances
model.add(Dense(8, activation='softmax'))

model.compile(optimizer='rmsprop',
             loss='categorical_crossentropy',
             metrics='accuracy')
model.fit(X_train, y_train, epochs=10, batch_size=32)

y_pred_prob = model.predict(X_test)
y_pred = []
for prob in y_pred_prob:
    y_pred.append(np.argmax(prob))

print(classification_report(y_test, y_pred, target_names=target_names))
if MODEL_SAVE:
    model.save(r'weights/CNN.h5')
