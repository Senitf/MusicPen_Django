from tensorflow.keras.models import load_model

def getModel():
    model = load_model('/Users/seni/Desktop/Projects/GIT/Museic/Museic/Music/score/Model/weights/CNN.h5')
    #print(model.summary())
    return model