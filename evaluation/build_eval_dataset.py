import json
import csv

with open(r"C:\CUAD\cuad-main\data\CUADv1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

contracts = data["data"]

rows = []

for contract in contracts:

    for paragraph in contract["paragraphs"]:

        for qa in paragraph["qas"]:

            question = qa["question"]

            answers = qa["answers"]

            if not answers:
                continue

            for ans in answers:

                clause = ans["text"].strip()

                if len(clause.split()) < 5:
                    continue

                rows.append({
                    "label": question,
                    "clause": clause
                })

print("Extracted clauses:", len(rows))

with open("evaluation/cuad_clauses.csv", "w", newline="", encoding="utf-8") as f:

    writer = csv.DictWriter(
        f,
        fieldnames=["label", "clause"]
    )

    writer.writeheader()
    writer.writerows(rows)

print("Saved to evaluation/cuad_clauses.csv")