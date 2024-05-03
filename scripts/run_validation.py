import json
import openai
import re
import csv
import os
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
# Set up your OpenAI API key
openai.api_key = 'sk-proj-95TEYaya4g0Tg3yyUC6qT3BlbkFJjH0lAVsfqNerC7fvlbN0'

mistral_api_key = "Rk4s7EYksi0A8zi7l56ZFO2PjzLq7rnZ"

def read_json_from_file(file_path):
    """Reads a JSON file and returns the data."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def read_text_from_file(file_path):
    """Reads a text file and returns the content as a string."""
    with open(file_path, 'r') as file:
        content = file.read().strip()
    return content

def save_json_to_file(data, file_path):
    """Saves the given data to a JSON file."""
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def ask_gpt(system_prompt, user_prompt, model):
    """Asks a question to the GPT API and returns the response."""

    if model[:3] == "gpt":
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages= [{
                    "role": "system",
                    "content": system_prompt
                }, {
                    "role": "user",
                    "content": user_prompt
                }],
                # max_tokens=150
            )
            # print(response)
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    elif model[:7] == "mistral" or model[:4] == "open":
        client = MistralClient(api_key=mistral_api_key)

        chat_response = client.chat(
            model=model,
            messages=[
                ChatMessage(role="system", content=system_prompt),
                ChatMessage(role="user", content=user_prompt)]
        )
        return chat_response.choices[0].message.content
    
def extract_response_data(interactions):
    """Extracts non-calendar response data from system_actual fields and keeps user queries."""
    cal_pattern = re.compile(r"<CAL>.*?</CAL>", re.DOTALL)
    extracted_data = []

    for interaction in interactions:
        new_interaction = []
        for entry in interaction:
            extracted_entry = {}
            if 'user' in entry:
                extracted_entry['user'] = entry['user']  # Carry over the user query
            if 'system_actual' in entry:
                # Remove <CAL> tags and content between them
                cleaned_response = cal_pattern.sub("", entry['system_actual']).strip()
                if cleaned_response:
                    extracted_entry['response'] = cleaned_response
            if extracted_entry:
                new_interaction.append(extracted_entry)
        extracted_data.append(new_interaction)

    return extracted_data

def extract_calendar_data(interactions):
    """Extracts calendar data from system and system_actual fields."""
    cal_pattern = re.compile(r"<CAL>(.*?)</CAL>", re.DOTALL)
    extracted_data = []

    for interaction in interactions:
        new_interaction = []
        for entry in interaction:
            if 'system' in entry or 'system_actual' in entry:
                calendar_data = {}
                if 'system' in entry:
                    match = cal_pattern.search(entry['system'])
                    if match:
                        try:
                            calendar_data['system'] = json.loads(match.group(1).strip())
                        except json.JSONDecodeError as e:
                            print("Error parsing JSON from system field:", e)
                            print("Data causing issue:", match.group(1).strip())
                if 'system_actual' in entry:
                    match = cal_pattern.search(entry['system_actual'])
                    if match:
                        try:
                            calendar_data['system_actual'] = json.loads(match.group(1).strip())
                        except json.JSONDecodeError as e:
                            print("Error parsing JSON from system_actual field:", e)
                            print("Data causing issue:", match.group(1).strip())
                new_interaction.append(calendar_data)
        extracted_data.append(new_interaction)

    return extracted_data
def save_text_to_file(text, file_path):
    """Saves the given text to a text file."""
    with open(file_path, 'w') as file:

        file.write(text)

def extract_scores(data, keys):
    """Extracts specified scores from the JSON data."""
    scores = []
    for item in data:
        entry_scores = [item[key] for key in keys if key in item]
        scores.append(entry_scores)
    return scores

def save_scores_to_csv(scores, headers, filepath):
    """Saves the scores to a CSV file."""
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(scores)
def run_val(model, system_prompt_directory, new_dir_name):

    system_prompt_file_path = system_prompt_directory + r"\prompt.txt"
    system_prompt = read_text_from_file(system_prompt_file_path)
    questions_file_path = system_prompt_directory + new_dir_name + r"\QA.txt"
    questions_and_answers = read_json_from_file(questions_file_path)

    # Iterate through each list of user-system interactions
    for interaction in questions_and_answers:
        for entry in interaction:
            if entry.get('user'):
                user_question = entry['user']
                # full_prompt = f"{system_prompt} {user_question}".strip()
                # print(f"Full Prompt: {full_prompt}")
                answer = ask_gpt(system_prompt, user_question, model)
                # print(f"Answer: {answer}")
                # Add the GPT-generated answer to the JSON structure
                interaction.append({'system_actual': answer})

    # Save the modified data to a new file
    new_file_path = questions_file_path.replace('.txt', '_answered.txt')
    save_json_to_file(questions_and_answers, new_file_path)
    print(f"QA answers saved to {new_file_path}")

    # Load data from file
    interactions = read_json_from_file(new_file_path)
    
    # Extract response data
    extracted_data = extract_response_data(interactions)
    reasoning_output_file_path = new_file_path.replace('.txt', '_reasoning.txt')
    # Save the extracted data to a new JSON file
    save_json_to_file(extracted_data, reasoning_output_file_path)
    print(f"Extracted response data saved to {reasoning_output_file_path}")

    calendar_output_file_path = new_file_path.replace('.txt', '_calendars.txt')
    
    # Load data from file
    interactions = read_json_from_file(new_file_path)
    
    # Extract calendar data
    extracted_data = extract_calendar_data(interactions)
    
    # Save the extracted data to a new JSON file
    save_json_to_file(extracted_data, calendar_output_file_path)
    print(f"Extracted calendar data saved to {calendar_output_file_path}")

    calendar_compare_system_prompt_file_path = r'C:\Users\deckerza\Desktop\Rose-Hulman\Senior_Year\Spring\GENAI\CalendarAssistant\AI_Calendar_Assistant\validation\calendar_comparison_prompt.txt'
    # Read prompts from files
    system_prompt = read_text_from_file(calendar_compare_system_prompt_file_path)
    calendars = read_text_from_file(calendar_output_file_path)
    
    # Make API call
    response = ask_gpt(system_prompt, calendars, "gpt-4-turbo")
    
    # Save the response to a specified directory
    cal_ratings_output = system_prompt_directory + new_dir_name + r"\calendar_ratings.txt"
    save_text_to_file(response, cal_ratings_output)
    print(f"calendar ratings saved to {cal_ratings_output}")


    reasoning_compare_system_prompt_file_path = r'C:\Users\deckerza\Desktop\Rose-Hulman\Senior_Year\Spring\GENAI\CalendarAssistant\AI_Calendar_Assistant\validation\reasoning_rating_prompt.txt'
    # Read prompts from files
    system_prompt = read_text_from_file(reasoning_compare_system_prompt_file_path)
    user_prompt = read_text_from_file(reasoning_output_file_path)
    
    # Make API call
    response = ask_gpt(system_prompt, user_prompt, "gpt-4-turbo")
    res_ratings_outputs = system_prompt_directory + new_dir_name + r"\reasoning_ratings.txt"
    # Save the response to a specified directory
    save_text_to_file(response, res_ratings_outputs)
    print(f"resoning ratings saved to {res_ratings_outputs}")


    output_csv_path = system_prompt_directory + new_dir_name + r'\scores.csv'

    # Read data from files
    data1 = read_json_from_file(cal_ratings_output)
    data2 = read_json_from_file(res_ratings_outputs)

    # Extract scores
    scores1 = extract_scores(data1, ['score'])
    scores2 = extract_scores(data2, ['clarity', 'accuracy'])

    # Combine scores from both files
    combined_scores = [s1 + s2 for s1, s2 in zip(scores1, scores2)]

    # Save to CSV
    headers = ['score', 'clarity', 'accuracy']
    save_scores_to_csv(combined_scores, headers, output_csv_path)
    print("complete")

def main():
    system_prompt_directory = r'C:\Users\deckerza\Desktop\Rose-Hulman\Senior_Year\Spring\GENAI\CalendarAssistant\AI_Calendar_Assistant\validation\template_and_fewshot'  # Update this with the path to your system prompt file
    all_dirs = [item for item in os.listdir(system_prompt_directory) if os.path.isdir(os.path.join(system_prompt_directory, item))]
    for dir in all_dirs:
        parts = dir.split('_')
        model = parts[1]
        run_val(model, system_prompt_directory, "\\" + dir)

if __name__ == "__main__":
    main()
