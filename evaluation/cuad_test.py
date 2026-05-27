from datasets import load_dataset

dataset = load_dataset(
    "theatticusproject/cuad",
    cache_dir="C:/hf"
)

print(dataset)

print(dataset["train"][0].keys())