from openai import OpenAI
import csv
import pandas as pd

# Set your OpenRouter API client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

# Define the number of runs
# num_runs = 3
num_runs = 1 # 先只测试1次，跑通代码

# Iterate over each attribute and process the corresponding CSV file
xlsx_filename = f"./question.xlsx"

# Read the questions
questions_list = []
df = pd.read_excel(xlsx_filename)
for index, row in df.iterrows():
    questions_list.append((row['Role'], row['Question Type'], row['Question']))

# Send each question and get the answer
for run in range(1, num_runs + 1):
    output_filename = f"./answers/llama4_answers_0{run}.csv"
    
    with open(output_filename, 'w', newline='') as response_file:
        response_writer = csv.writer(response_file)
        response_writer.writerow(['Role', 'Question Type', 'Question', 'Answer - llama4'])
        
        for role, question_type, question in questions_list:
            # if question_type == "Yes/No":
            #     message = question + """\nPlease **only answer yes/no.**\n
            #             Answer Format (You MUST follow this):\n
            #             Yes/No.\n""" 
            # elif question_type == "Choice":
            #     message = question + """\nPlease **only make one choice** from all options.**\n
            #             Answer Format (You MUST follow this):\n
            #             Your choice.\n"""
            # elif question_type == "Wh":
            #     message = question + "\nProvide the answer in no more than 100 words."
            message = question
            print(message)
            
            try:
                response = client.chat.completions.create(
                    model="meta-llama/llama-4-maverick",
                    messages=[
                        {"role": "system", "content": f"You are a {role}"},
                        {"role": "user", "content": message}
                    ],
                    stream=False
                )
                answer = response.choices[0].message.content.strip()
            except Exception as e:
                answer = "Error: " + str(e)
            
            response_writer.writerow([role, question_type, question, answer])