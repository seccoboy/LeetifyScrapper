import os
import pandas as pd

folder_path = "parsed/"
output_file = "links.txt"

# Set to store unique links
unique_links = set()

# Loop through each file in the directory
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    
    # Check if the file is a CSV file
    if filename.endswith(".csv"):
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Extract links from the "Links" column and add them to the set
        links = df["Link"].tolist()
        unique_links.update(links)

# Save the unique links in a text file
with open(output_file, "w") as file:
    file.write("\n".join(unique_links))

print("Links saved in", output_file)
