import os
import csv 

# Function to construct full image path
def construct_image_path(image_name):
    # Assuming that images are stored in the 'Food Images' folder in the app/static/images directory
    return os.path.join('images', 'Food Images', image_name)

# Read the CSV file
csv_file = 'food.csv'
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

# Update the CSV file with the relative image paths
for row in rows:
    image_name = row['image_name']  # Assuming 'image_name' is the column containing the image name
    relative_image_path = construct_image_path(image_name)
    row['image_path'] = relative_image_path  # Assuming 'image_path' is the new column to store relative image paths

# Write updated rows back to CSV file
fieldnames = reader.fieldnames + ['image_path']
output_csv_file = 'food_with_image_paths.csv'
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(f"Image paths have been added to '{output_csv_file}' successfully.")
