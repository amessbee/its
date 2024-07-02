import xml.etree.ElementTree as ET
import os

## Add questions from files in new_files/ to bank.xml. 
### It makes rudimentaary checks whether a question is already there. 
# Also assigns it a unique question_number.

def add_questions_from_directory(bank_file, directory='new_files'):
    # Parse the existing question bank XML
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # Function to find the current highest question number to ensure uniqueness
    def get_next_question_number():
        max_number = 0
        # Check numbers in standalone questions
        for question_elem in bank_root.findall('.//question'):
            q_number_elem = question_elem.find('question_number')
            if q_number_elem is not None and q_number_elem.text.isdigit():
                max_number = max(max_number, int(q_number_elem.text))
        return max_number + 1

    # Function to check if the question already exists
    def question_exists(question_text):
        for question_elem in bank_root.findall('.//question'):
            if question_elem.find('text').text.strip() == question_text.strip():
                return True
        return False

    # Initialize the next question number
    next_question_number = get_next_question_number()

    # Get all XML files in the specified directory
    new_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith('.xml')]

    # Iterate over each new file
    for file_path in new_files:
        new_tree = ET.parse(file_path)
        new_root = new_tree.getroot()

        # Handle standalone questions
        for new_question in new_root.findall('question'):
            new_question_text = new_question.find('text').text

            # Check if the question already exists in the bank
            if not question_exists(new_question_text):
                # Assign a unique question number
                question_number_elem = ET.SubElement(new_question, 'question_number')
                question_number_elem.text = str(next_question_number)
                next_question_number += 1

                # Add the new question to the bank
                bank_root.append(new_question)

        # Handle grouped questions
        for new_group in new_root.findall('question_group'):
            new_group_text = new_group.find('text').text
            # Create a new question group element in the bank
            new_bank_group = ET.SubElement(bank_root, 'question_group')
            new_bank_group_text = ET.SubElement(new_bank_group, 'text')
            new_bank_group_text.text = new_group_text

            for new_question in new_group.findall('question'):
                new_question_text = new_question.find('text').text

                # Check if the question already exists in the bank
                if not question_exists(new_question_text):
                    # Assign a unique question number
                    question_number_elem = ET.SubElement(new_question, 'question_number')
                    question_number_elem.text = str(next_question_number)
                    next_question_number += 1

                    # Add the new question to the created group in the bank
                    new_bank_group.append(new_question)

    # Save the updated XML to the same file
    bank_tree.write(bank_file)

# Example usage
# bank_file_path = 'bank.xml'
# add_questions_from_directory(bank_file_path)
