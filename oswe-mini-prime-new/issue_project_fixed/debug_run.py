import pandas as pd
from src.customer_segmentation import CustomerSegmentation

data = pd.read_csv('data/customers.csv')

all_labels = []
for i in range(5):
    s = CustomerSegmentation(n_clusters=3)
    labels = s.fit_predict(data)
    print(f'run {i+1} labels:', labels)
    all_labels.append(labels)

# Check consistency
first = all_labels[0]
for i, lab in enumerate(all_labels[1:], start=2):
    print(f'run1 == run{i}:', (first == lab).all())

