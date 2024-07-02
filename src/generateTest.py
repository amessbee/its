import random
import xml.etree.ElementTree as ET
import xml2tex
import subprocess

TOTAL_QUESTIONS = 100
NUMBER_OF_ANALYTICAL_QUESTIONS = 50
MAX_QUESTION_GROUPS = 2

def move_question_groups(input_file, output_file, filter_tag='type', filter_value = '1', unselected_file = None):
    # Read the questions from the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Get a list of all question groups
    all_question_groups = root.findall('./question_group')
    all_questions = root.findall('./question')
    
    # Find question groups and questions with the specified filter
    filter = filter_tag + '="' +  filter_value + '"'
    question_groups = root.findall('./question_group['+filter + ']')
    questions = root.findall('./question['+filter + ']')

    # Randomly select up to MAX_QUESTION_GROUPS question groups
    number_groups = random.sample(range(MAX_QUESTION_GROUPS),1)[0]
    selected_groups = random.sample(question_groups, min(number_groups, len(question_groups)))

    # Create a new XML tree for the test file
    test_root = ET.Element('questions')
    test_tree = ET.ElementTree(test_root)

    # Move the selected question groups to the test tree
    for group in selected_groups:
        test_root.append(group)

    # Calculate the total count of questions in the selected question groups
    selected_question_count = sum(len(group.findall('./question')) for group in selected_groups)

    # Calculate the remaining count of questions needed
    remaining_ana_count = NUMBER_OF_ANALYTICAL_QUESTIONS - selected_question_count

    if remaining_ana_count > 0:
        # Randomly select additional questions from the selected question groups
        selected_questions = random.sample(questions, min(remaining_ana_count, len(questions)))
        # Move the additional selected questions to the test tree
        for question in selected_questions:
            test_root.append(question)


    # Remove the selected question groups from the list
    other_question_groups = [group for group in all_question_groups if group not in question_groups]
    other_questions = [question for question in all_questions if question not in questions]

    # Calculate the remaining count of questions needed from different topics
    remaining_count = TOTAL_QUESTIONS - NUMBER_OF_ANALYTICAL_QUESTIONS

    if remaining_count > 0:
        # Randomly select additional questions from different question groups
        number_groups = random.sample(range(MAX_QUESTION_GROUPS),1)[0]
        selected_additional_groups = random.sample(other_question_groups, min(number_groups, len(other_question_groups)))
        # Move the additional selected question groups to the test tree
        for group in selected_additional_groups:
            test_root.append(group)

        # Calculate the total count of questions in the selected question groups
        selected_question_count = max(0,sum(len(group.findall('./question')) for group in selected_additional_groups))

        # Calculate the remaining count of questions needed
        remaining_count -= selected_question_count

        # Randomly select additional questions from individual questions
        selected_additional_questions = random.sample(other_questions, min(remaining_count, len(other_questions)))

        # Move the additional selected questions to the test tree
        for question in selected_additional_questions:
            test_root.append(question)

    # Save the test tree to the output XML file
    test_tree.write(output_file)

    if unselected_file != None:
        # Create a new XML tree for the unselected questions
        unselected_root = ET.Element('questions')
        unselected_tree = ET.ElementTree(unselected_root)

        # Remove the selected question groups from the list
        other_question_groups = [group for group in all_question_groups if group not in selected_groups and group not in selected_additional_groups]
        other_questions = [question for question in all_questions if question not in selected_questions and question not in selected_additional_questions]

        #print(len(other_question_groups))
        # Move the unselected question groups to the unselected tree
        for group in other_question_groups:
            unselected_root.append(group)
        #print(len(other_questions))
        # Move the unselected questions to the unselected tree
        for question in other_questions:
            unselected_root.append(question)

        unselected_tree.write(unselected_file)

# Example usage
input_file = 'bank.xml'
test_file1 = 'test1.xml'
test_file2 = 'test2.xml'
filter_tag = 'type'
filter_value = '1'
unselected_file = 'unselected.xml'
test_tex1 = 'test1.tex'
test_tex2 = 'test2.tex'
# Move two question groups and additional questions to the test file
move_question_groups(input_file, test_file1, filter_tag=filter_tag, filter_value=filter_value, unselected_file = unselected_file)
move_question_groups(unselected_file, test_file2, filter_tag=filter_tag, filter_value=filter_value)

xml2tex.generate_latex_files(test_file1,'test1.tex', 'answers1.tex')
xml2tex.generate_latex_files(test_file2,'test2.tex', 'answers2.tex')


# Execute a shell command
command = "pdflatex "+ test_tex1
result = subprocess.run(command, shell=True)

# Print the output and return code
print("Output:")
print(result.stdout)
print("Return code:", result.returncode)


# Execute a shell command
command = "pdflatex "+ test_tex2
result = subprocess.run(command, shell=True)

# Print the output and return code
print("Output:")
print(result.stdout)
print("Return code:", result.returncode)

# Execute a shell command
command = "latexmk -c "
result = subprocess.run(command, shell=True)

# Print the output and return code
print("Output:")
print(result.stdout)
print("Return code:", result.returncode)
