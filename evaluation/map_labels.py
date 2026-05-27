import pandas as pd

df = pd.read_csv("evaluation/classified_results.csv")

RISK_MAPPING = {

    # -------------------------
    # HIGH RISK
    # -------------------------

    "termination": "high",
    "uncapped liability": "high",
    "cap on liability": "high",
    "liability": "high",
    "non-compete": "high",
    "no-solicit": "high",
    "covenant not to sue": "high",
    "exclusive": "high",
    "exclusivity": "high",
    "liquidated damages": "high",
    "irrevocable": "high",
    "perpetual license": "high",
    "ip ownership": "high",
    "joint ip ownership": "high",
    "anti-assignment": "high",
    "change of control": "high",

    # -------------------------
    # MEDIUM RISK
    # -------------------------

    "license": "medium",
    "audit": "medium",
    "insurance": "medium",
    "renewal": "medium",
    "notice period": "medium",
    "minimum commitment": "medium",
    "price restriction": "medium",
    "revenue/profit sharing": "medium",
    "volume restriction": "medium",
    "warranty": "medium",
    "governing law": "medium",
    "third party beneficiary": "medium",
    "post-termination": "medium",
    "rofr": "medium",
    "rofo": "medium",
    "rofn": "medium",

    # -------------------------
    # LOW RISK
    # -------------------------

    "agreement date": "low",
    "effective date": "low",
    "expiration date": "low",
    "document name": "low",
    "parties": "low"
}

def map_expected_risk(label):

    label = str(label).lower()

    for key, value in RISK_MAPPING.items():

        if key in label:
            return value

    return "low"


df["expected_severity"] = df["cuad_label"].apply(
    map_expected_risk
)

print(
    df[
        [
            "cuad_label",
            "expected_severity",
            "predicted_severity"
        ]
    ].head(20)
)

df.to_csv(
    "evaluation/mapped_results.csv",
    index=False
)

print("Saved mapped results.")