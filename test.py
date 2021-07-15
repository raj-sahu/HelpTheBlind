import argparse
from keras.preprocessing.sequence import pad_sequences
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
from keras.models import load_model, Model
import pickle
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')

parser = argparse.ArgumentParser()
parser.add_argument("Image", help="path of Image File")
args = parser.parse_args()
img = args.Image


model = load_model("./model_weights/model19.h5")
with open("./Computed/Word2SeqNumbers.pkl", "rb") as Word2SeqNumbers:
    word_to_idx, idx_to_word = pickle.load(Word2SeqNumbers)

with open("./Computed/encoded_test_images.pkl", "rb") as encoded_pickle:
    encoding_test = pickle.load(encoded_pickle)


max_len = 35


featureExtractorModel = ResNet50(weights="imagenet", input_shape=(224, 224, 3))
featureExtractorModel = Model(
    featureExtractorModel.input, featureExtractorModel.layers[-2].output)


def preprocess_image(img):
    img = image.load_img(img, target_size=(224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    return img


def encode_image(img):
    img = preprocess_image(img)
    feature_vector = featureExtractorModel.predict(img)
    feature_vector = feature_vector.reshape(feature_vector.shape[1],)
    return feature_vector


def predict_caption(photo):
    in_text = "startseq"

    for i in range(max_len):

        sequence = [word_to_idx[w]
                    for w in in_text.split() if w in word_to_idx]
        sequence = pad_sequences([sequence], maxlen=max_len, padding='post')

        ypred = model.predict([photo, sequence])
        ypred = ypred.argmax()
        word = idx_to_word[ypred]
        in_text += ' ' + word

        if word == 'endseq':
            break

    final_caption = in_text.split()
    final_caption = final_caption[1:-1]
    final_caption = ' '.join(final_caption)

    return final_caption


photo = encode_image(img)
photo = photo.reshape((1, 2048))
caption = predict_caption(photo)
print("-------------------------------------"*5,
      caption, "-------------------------------------"*5)
CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'
color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
i = plt.imread(img)
plt.imshow(i)
plt.axis("off")
plt.title(caption,    backgroundcolor='#2CBDFE',
          color='white')
plt.show()
