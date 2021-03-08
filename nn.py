import keras
import numpy
import pickle
import pandas as pd
from keras.models import Sequential
from keras.layers import *
from keras.callbacks import *
from keras.utils.np_utils import to_categorical
from tqdm import tqdm
from main import *


dataset_path = 'dataset'
model_path = 'save_model\\model.pickle'

def save(model, filename):
    with open(filename, "wb") as f:
        pickle.dump(model, f)


def load(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)



model = Sequential()
#model.add(Embedding(3800, 32, input_length=380))
#model.add(Dropout(0.2))
model.add(Dense(128,activation='sigmoid',input_shape=(1,3)))
model.add(GRU(128))
#model.add(Dense(256,activation='relu'))
#model.add(Dropout(0.2))
model.add(Dense(15,activation='softmax'))

model.summary()


data = pd.read_csv('dataset/dataset_onehot.csv')
train = pd.read_csv('dataset/train_onehot.csv')
test = pd.read_csv('dataset/test_onehot.csv')
'''
data = pd.read_csv('/root/paddlejob/workspace/train_data/datasets/data73201/dataset_onehot.csv')
test = pd.read_csv('/root/paddlejob/workspace/train_data/datasets/data73201/test_onehot.csv')
train = pd.read_csv('/root/paddlejob/workspace/train_data/datasets/data73201/train_onehot.csv')
'''


df_train = pd.DataFrame(columns=('feature', 'Genre'))
for index ,item in tqdm(train.iterrows()):
    feature = getfeature(str(item['Path']))
    for l in feature:
        df_train.append([{'feature':l,'Genre':item['Genre']}], ignore_index=True)

df_test = pd.DataFrame(columns=('feature', 'Genre'))
for index ,item in tqdm(test.iterrows()):
    feature = getfeature(str(item['Path']))
    for l in feature:
        df_test.append([{'feature':l,'Genre':item['Genre']}], ignore_index=True)

es = EarlyStopping(monitor = 'val_acc',patience = 10)
model.compile(loss="categorical_crossentropy",optimizer="adam",metrics=['accuracy'])

batch_size = 64
epochs = 20
model.fit(df_train['feature'],df_train['Genre'],
          validation_split=0.2,
          batch_size=batch_size,
          epochs=epochs,
          callbacks=[es],
          shuffle=true
          )

#save(model,model_path)
#model = load(model_path)

scores = model.evaluate(df_test['feature'],df_test['Genre'])
print('GRU:test_loss:%f , accuracy:%f' % (scores[0],scores[1]))

result = pd.DataFrame(scores)
result.to_csv('result.csv')

#result.to_csv('/root/paddlejob/workspace/output/result.csv')
