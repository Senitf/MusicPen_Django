from tensorflow.keras.models import load_model

model = load_model(r'weights/CNN.h5')
print(model.summary())