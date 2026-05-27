import json

with open(r"C:\CUAD\cuad-main\data\CUADv1.json", "r", encoding="utf-8") as f:
    data = json.load(f)

contracts = data["data"]

first_contract = contracts[0]

paragraphs = first_contract["paragraphs"]

print("Total Paragraphs:", len(paragraphs))

first_para = paragraphs[0]

print("\nParagraph Keys:")
print(first_para.keys())

print("\nQAS Length:")
print(len(first_para["qas"]))

if first_para["qas"]:
    first_qa = first_para["qas"][0]

    print("\nQA Keys:")
    print(first_qa.keys())

    print("\nQuestion:")
    print(first_qa["question"])

    print("\nAnswers:")
    print(first_qa["answers"][:2])