import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report 
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression  #逻辑回归
from sklearn.ensemble import RandomForestClassifier 

test = pd.read_csv('test.csv')

train = pd.read_csv('train.csv')

train.head()

#1
age_median = train['Age'].median()
fare_median = train['Fare'].median()
embarked_mode = train['Embarked'].mode()[0]
#2
train['Age'] = train['Age'].fillna(test['Age'].median())
#test['Age'] = test['Age'].fillna(test['Age'].median())
train['Fare'] = train['Fare'].fillna(test['Fare'].median())
train['Embarked'] = train['Embarked'].fillna(embarked_mode)
#test['Fare'] = test['Fare'].fillna(test['Fare'].median())


#3
test['Age'] = test['Age'].fillna(age_median)
test['Fare'] = test['Fare'].fillna(fare_median)

#分离
train = pd.get_dummies(train,columns=['Sex','Embarked'],drop_first=False)

train = train.astype(int,errors = 'ignore')
test = test.astype(int,errors = 'ignore')

#训练前删除无法使用的非数值列
features = ['Pclass', 'Sex_male', 'Sex_female', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked_C', 'Embarked_Q', 'Embarked_S']
X = train[features]
y = train['Survived']

# 1. 划分训练集和验证集 (Validation Set)
from sklearn.model_selection import train_test_split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. 初始化并训练模型
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
model.fit(X_train, y_train)

# 3. 评估模型
print(f"验证集准确率: {model.score(X_val, y_val)}")

# 对 test 做同样的 One-Hot Encoding
test = pd.get_dummies(test, columns=['Sex', 'Embarked'], drop_first=False)

# 再次确保 test 里面没有非数值类型 (和第42行对应)
test = test.astype(int, errors='ignore')

X_test= test[features]
print(X_test.isnull().sum())

# 使用训练好的 model 进行预测
predictions = model.predict(X_test)

# 构建提交的 DataFrame
output = pd.DataFrame({
    'PassengerId': test['PassengerId'],
    'Survived': predictions
})

# 保存为 CSV 文件
output.to_csv('submission.csv', index=False)
print("保存成功！快去提交 submission.csv 吧！")



