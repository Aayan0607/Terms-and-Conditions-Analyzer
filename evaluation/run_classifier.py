import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

import pandas as pd

from modules.classifier import classify_clause

import pandas as pd

from modules.classifier import classify_clause

df = pd.read_csv("evaluation/cuad_clauses.csv")

results = []

LIMIT = 500

for i, row in df.head(LIMIT).iterrows():

    clause = str(row["clause"])
    actual_label = str(row["label"])

    prediction = classify_clause(clause)

    results.append({
        "clause": clause,
        "cuad_label": actual_label,
        "predicted_category": prediction["category"],
        "predicted_severity": prediction["severity"],
        "similarity_score": prediction["similarity_score"],
        "intent": prediction["intent"]
    })

    if i % 50 == 0:
        print(f"Processed {i}")

output_df = pd.DataFrame(results)

output_df.to_csv(
    "evaluation/classified_results.csv",
    index=False
)

print("Done.")
print(output_df.head())