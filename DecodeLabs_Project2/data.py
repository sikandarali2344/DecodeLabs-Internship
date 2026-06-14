# save_datasets.py - Run this first to populate your data folder

import pandas as pd
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
import os

os.makedirs('data', exist_ok=True)

# Save Iris dataset
iris = load_iris()
df_iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df_iris['target'] = iris.target
df_iris['target_name'] = df_iris['target'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})
df_iris.to_csv('data/iris_dataset.csv', index=False)
print("✅ Saved: data/iris_dataset.csv")

# Save Wine dataset
wine = load_wine()
df_wine = pd.DataFrame(data=wine.data, columns=wine.feature_names)
df_wine['target'] = wine.target
df_wine['target_name'] = df_wine['target'].map({0: 'class_0', 1: 'class_1', 2: 'class_2'})
df_wine.to_csv('data/wine_dataset.csv', index=False)
print("✅ Saved: data/wine_dataset.csv")

# Save Breast Cancer dataset
cancer = load_breast_cancer()
df_cancer = pd.DataFrame(data=cancer.data, columns=cancer.feature_names)
df_cancer['target'] = cancer.target
df_cancer['target_name'] = df_cancer['target'].map({0: 'malignant', 1: 'benign'})
df_cancer.to_csv('data/breast_cancer_dataset.csv', index=False)
print("✅ Saved: data/breast_cancer_dataset.csv")

print("\n📁 Data folder now contains 3 CSV files!")