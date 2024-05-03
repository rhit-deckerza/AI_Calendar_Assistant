import os
import pandas as pd

def gather_scores(root_dir):
    # Prepare a DataFrame to hold all scores, clarity, and accuracy with their corresponding directory path
    all_scores = pd.DataFrame(columns=['directory', 'score', 'clarity', 'accuracy'])

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith("scores.csv"):
                file_path = os.path.join(subdir, file)
                data = pd.read_csv(file_path)
                
                # Check if the necessary columns are present
                if set(['score', 'clarity', 'accuracy']).issubset(data.columns):
                    # Gather data with the full directory path
                    scores_data = pd.DataFrame({
                        'directory': subdir,  # Using the full path as directory identifier
                        'score': data['score'],
                        'clarity': data['clarity'],
                        'accuracy': data['accuracy']
                    })
                    # Append the data of this file to the DataFrame
                    all_scores = pd.concat([all_scores, scores_data], ignore_index=True)
                else:
                    print(f"Skipping {file_path}: Required columns are missing")

    # Save the gathered data to a new CSV file
    all_scores.to_csv('gathered_scores_full_path.csv', index=False)
    print("Gathered scores, clarity, and accuracy CSV with full directory paths created successfully.")

# Usage
root_directory = r'C:\Users\deckerza\Desktop\Rose-Hulman\Senior_Year\Spring\GENAI\CalendarAssistant\AI_Calendar_Assistant\validation'
gather_scores(root_directory)
