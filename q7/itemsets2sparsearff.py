# Usage: python itemsets2sparsearff.py kosarak.dat > kosarak.arff
import sys

input_file = sys.argv[1]  # the name of the data file you give on the command line

all_item_ids = set()
for line in open(input_file):
    for item in line.split():
        all_item_ids.add(int(item))

sorted_item_ids = sorted(all_item_ids)  # list of all item IDs in ascending order

# Map each actual item ID to the column index it will have in the ARFF file
item_to_column = {item_id: column_index
                  for column_index, item_id in enumerate(sorted_item_ids)}

print(f"@RELATION {input_file}")
for item_id in sorted_item_ids:
    print(f"@ATTRIBUTE i{item_id} {{0,1}}")
print("@DATA")

for line in open(input_file):
    # Find the column numbers for the items in this line
    present_columns = {item_to_column[int(item)] for item in line.split()}
    # Build a string like {0 1, 3 1}
    sparse_row = ", ".join(f"{col} 1" for col in sorted(present_columns))
    print("{" + sparse_row + "}")
