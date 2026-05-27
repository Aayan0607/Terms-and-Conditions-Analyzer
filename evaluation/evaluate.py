import json

with open(r"C:\CUAD\cuad-main\data\CUADv1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(type(data))
print(data.keys())

print("Number of contracts:", len(data["data"]))