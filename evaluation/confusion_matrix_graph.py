import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd

df = pd.read_csv("evaluation/mapped_results.csv")

y_true = df["expected_severity"]
y_pred = df["predicted_severity"]

labels = ["low", "medium", "high"]

cm = confusion_matrix(
    y_true,
    y_pred,
    labels=labels
)

fig, ax = plt.subplots(figsize=(7, 6))

im = ax.imshow(cm)

ax.set_xticks(np.arange(len(labels)))
ax.set_yticks(np.arange(len(labels)))

ax.set_xticklabels(labels)
ax.set_yticklabels(labels)

plt.xlabel("Predicted Severity")
plt.ylabel("Actual Severity")

plt.title("Confusion Matrix")

for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )

plt.colorbar(im)

plt.tight_layout()

plt.show()