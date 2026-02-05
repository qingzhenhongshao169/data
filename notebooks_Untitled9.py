import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression  #逻辑回归
from sklearn.ensemble import RandomForestClassifier 
import matplotlib.pyplot as plt
from sklearn.model_selection import cross_val_score

data = pd.read_csv('clean_feature.csv')
train = pd.read_csv('train.csv')
X = data
y = train['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y,stratify=y, test_size=0.25, random_state=42)

X_train['Age'] = X_train['Age'].fillna(X_train['Age'].median())

X['Age'] = X['Age'].fillna(X_train['Age'].median())

X_test['Age'] = X_test['Age'].fillna(X_test['Age'].median())   #为什么清洗时候没有把年龄给存进去

X.to_csv('clean_feature.csv')

a = pd.read_csv('clean_feature.csv')


lr = LogisticRegression(max_iter = 100)
lr.fit(X_train, y_train)
score = cross_val_score(lr,X_train,y_train,cv = 10)
score.mean()

lr1 = LogisticRegression(max_iter = 100)
lr1.fit(X_test, y_test)
score1 = cross_val_score(lr1,X_test,y_test,cv = 10)
score1.mean()

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report   #导入混淆矩阵来评估分类的准确性

lr = LogisticRegression().fit(X_train,y_train)
y_pred = lr.predict(X_train)
confusion_matrix(y_train,y_pred, labels=[0,1])

lr1= LogisticRegression().fit(X_test,y_test)
y_pred = lr.predict(X_test)
confusion_matrix(y_test,y_pred, labels=[0,1])

y_train.value_counts(),360+52,80+176

y_test.value_counts()

print(classification_report(y_train,y_pred))   #减少计算过程

2/(1/0.82+1/0.87)

176/(176+52)

from sklearn.metrics import roc_curve

fpr,tpr,thresholds = roc_curve(y_test,lr.decision_function(X_test))
fpr,tpr,thresholds

plt.plot(fpr,tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')

close_zero = np.argmin(np.abs(thresholds))
plt.plot(fpr[close_zero],tpr[close_zero],'o')
plt.plot(fpr,tpr)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('LR ROC')

preditions = lr.predict(X_test)

test_df = pd.read_csv('test.csv')

submission = pd.DataFrame({'Survived':preditions})

submission.to_csv('titanic_submission.csv',index=False)

submission.shape





