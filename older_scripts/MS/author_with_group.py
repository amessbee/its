import xml.etree.ElementTree as ET
import re
import os

def question_exists(question_text, bank_tree):
    root = bank_tree.getroot()
    for question_elem in root.iter('question'):
        text_elem = question_elem.find('text')
        if text_elem is not None and text_elem.text.strip() == question_text.strip():
            return True
    return False

def add_author_to_questions(input_file, output_file, author_name='Dr. Umar Suleman', topic_name1=None, topic_name2=None):
    # Load the input XML file
    input_tree = ET.parse(input_file)
    input_root = input_tree.getroot()

    # Load the output XML file or create a new one if it doesn't exist
    try:
        output_tree = ET.parse(output_file)
        output_root = output_tree.getroot()
    except FileNotFoundError:
        output_root = ET.Element('questions')
        output_tree = ET.ElementTree(output_root)

    # Get the existing question count in the output XML
    question_count = len(output_root.findall('question'))

    # Determine the new question number
    if question_count == 0:
        question_number = 1
    else:
        question_numbers = [int(q.find('question_number').text) for q in output_root.findall('question')]
        question_number = max(question_numbers) + 1

    # Iterate over each question_group element in the input XML
    for i, question_group_elem in enumerate(input_root.iter('question_group')):
        # Create a new question_group element in the output XML
        output_question_group_elem = ET.SubElement(output_root, 'question_group')

        # Assign topic_name based on question index
        if i is not None and i < 5 and topic_name1 is not None:
            topic_name = topic_name1
        elif i is not None and i >= 5 and topic_name2 is not None:
            topic_name = topic_name2
        else:
            topic_name = None

        # Add topic_name element if provided and not already existing
        question_topic_elem = output_question_group_elem.find('topic_name')
        if question_topic_elem is None and topic_name is not None:
            topic_elem = ET.Element('topic_name')
            topic_elem.text = topic_name
            output_question_group_elem.append(topic_elem)

        # Copy any additional text or figure elements within the question_group to the output
        for text_elem in question_group_elem.findall('text'):
            output_text_elem = ET.SubElement(output_question_group_elem, 'text')
            output_text_elem.text = text_elem.text
        for figure_elem in question_group_elem.findall('figure'):
            output_figure_elem = ET.SubElement(output_question_group_elem, 'figure')
            output_figure_elem.text = figure_elem.text

        # Iterate over each question within the question_group
        for question_elem in question_group_elem.findall('question'):
            process_question_elem(question_elem, output_question_group_elem, output_tree, question_number, author_name, topic_name1, topic_name2, i)
            question_number += 1

    # Iterate over each question element not part of any question_group
    #for question_elem in input_root.findall('question'):
    for i, question_elem in enumerate(input_root.iter('question')):
        process_question_elem(question_elem, output_root, output_tree, question_number, author_name, topic_name1, topic_name2, i)
        question_number += 1

    # Save the modified output XML file
    output_tree.write(output_file)

def process_question_elem(question_elem, output_parent_elem, output_tree, question_number, author_name, topic_name1, topic_name2, i):
    # Check if <text> element already exists
    text_elem = question_elem.find('text')
    if text_elem is None:
        return
    question_text = text_elem.text.strip()

    # Check if the question already exists in the bank
    if question_exists(question_text, output_tree):
        return

    # Check if <author> element already exists
    author_elem = question_elem.find('author')
    if author_elem is None:
        # Create the <author> element if it doesn't exist
        author_elem = ET.Element('author')
        author_elem.text = author_name
        question_elem.append(author_elem)

    # Check if <question_number> element already exists
    question_number_elem = question_elem.find('question_number')
    if question_number_elem is None:
        # Create the <question_number> element if it doesn't exist
        question_number_elem = ET.Element('question_number')
        question_number_elem.text = str(question_number)
        question_elem.insert(0, question_number_elem)

    # Assign topic_name based on question index
    if i is not None and i < 5 and topic_name1 is not None:
        topic_name = topic_name1
    elif i is not None and i >= 5 and topic_name2 is not None:
        topic_name = topic_name2
    else:
        topic_name = None

    # Add topic_name element if provided and not already existing
    question_topic_elem = question_elem.find('topic_name')
    if question_topic_elem is None and topic_name is not None:
        topic_elem = ET.Element('topic_name')
        topic_elem.text = topic_name
        question_elem.append(topic_elem)

    # Append the question to the output XML
    output_parent_elem.append(question_elem)


def process_files_in_directory(directory, xml_file = 'bank.xml'):
    # Get a list of all files in the directory
    files = os.listdir(directory)

    # Iterate over each file
    for filename in files:
        # Check if the file is in the desired format
        if not filename.endswith('.xml'):
            continue
        parts = filename.split('_')
        if len(parts) != 5:
            continue
        # Extract the author name and topic names from the filename
        author_name = parts[0] + ' ' + parts[1] + ' ' + parts[2]
        topic_name1 = parts[3]
        topic_name2 = parts[4].split('.')[0]

        # Call add_author_to_questions with the extracted values
        input_file = os.path.join(directory, filename)
        output_file = xml_file
        add_author_to_questions(input_file, output_file, author_name, topic_name1, topic_name2)

def parse_options_with_numeric_values(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Iterate over each question element
    for question_elem in root.findall('question'):
        # Iterate over each option element within the question
        for option_elem in question_elem.findall('options/option'):
            option_text = option_elem.text

            # Check if the option text already contains a dollar sign
            if '$' not in option_text:
                # Extract the numeric value from the option text
                numeric_value = re.findall(r'-?\d+(?:\.\d+)?', option_text)

                # Check if a numeric value is found
                if numeric_value:
                    # Enclose the numeric value with '$' signs
                    modified_option_text = option_text.replace(numeric_value[0], '$' + numeric_value[0] + '$')
                    option_elem.text = modified_option_text

    # Save the modified XML file
    tree.write(xml_file)

import xml.etree.ElementTree as ET

def remove_question_number(input_file):
    # Read the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Find all question elements with question_number attribute
    questions = root.findall('.//question[@question_number]')

    # Remove the question_number attribute from each question element
    for question in questions:
        del question.attrib['question_number']

    # Save the modified XML tree to the same input file
    tree.write(input_file)

# Example usage
directory = 'XMLsMS'
#directory = 'test'
xml_file = 'MSbank.xml'
#directory = 'test'
process_files_in_directory(directory, xml_file)

# Example usage
#parse_options_with_numeric_values(xml_file)

# Remove the question_number attribute from the input file and save in the same file
# remove_question_number(xml_file)
