from datasets import load_from_disk

INPUT = "data/raw"

TRAIN_OUTPUT = "data/train"
TEST_OUTPUT = "data/test"


# Load dataset
dataset = load_from_disk(INPUT)

print("Original dataset:")
print(dataset)


# Split
split = dataset.train_test_split(
    test_size=0.2,
    seed=42
)


train_dataset = split["train"]
test_dataset = split["test"]


print("\nTrain:")
print(train_dataset)

print("\nTest:")
print(test_dataset)


# Save
train_dataset.save_to_disk(TRAIN_OUTPUT)
test_dataset.save_to_disk(TEST_OUTPUT)

print("\nSaved train/test datasets.")