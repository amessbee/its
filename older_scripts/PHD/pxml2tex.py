import random
import xml.etree.ElementTree as ET
import os

MAX_QUESTIONS_PER_SECTION = 25
MAX_GENERAL_QUESTIONS = 50  # Maximum number of questions in the 'General' section
PRINT_AUTHOR = False  # Set to True if author name should be printed, False otherwise
GENERAL_PREFIX = 'General'
FIGURE_SCALE = 0.1

def process_question(question, f, ans_f, question_count):
    """
    Process a single question element and write it to the output LaTeX file.

    Args:
        question (Element): The question element.
        f (file): The output LaTeX file.
        ans_f (file): The answers file.
        question_count (int): The current question count.
    """
    question_text = question.find('text').text
    options = question.find('options')
    answer = question.find('answer').text
    author = question.find('author').text

    # Write the question text and author
    f.write('\\noindent \\textbf{' + str(question_count) + '}. ' + question_text + '\n')
    # Write the author name if enabled
    if PRINT_AUTHOR:
        f.write('\\textit{Author: ' + author + '}\n')

    # Write the figure if available
    figure = question.find('figure')
    if figure is not None:
        figure_path = figure.text
        f.write('\\begin{figure}[!h]\n')
        f.write('\\centering\n')
        f.write('\\includegraphics[width='+FIGURE_SCALE+'\\textwidth]{' + figure_path + '}\n')
        f.write('\\end{figure}\n')

    # Write the options
    f.write('\\begin{itemize}[label=, itemsep=0pt, parsep=0pt, topsep=0pt]\n')
    for option in options:
        option_text = option.text
        # Exclude "None of the above" option
        if 'None of the above' in option_text:
            f.write('\\item ' + option_text + '\n')
        else:
            f.write('\\item ' + option_text + '\n')
    f.write('\\end{itemize}\n')

    # Write the answer to the answers file
    ans_f.write(str(question_count) + ': ' + answer + '\n')

    # Add some space between questions
    f.write('\\vspace{0.5cm}\n')

def generate_latex_files(questions_file, output_file, answers_file):
    """
    Generate LaTeX files for questions and answers from an input XML file.

    Args:
        questions_file (str): The input XML file containing the questions.
        output_file (str): The output LaTeX file for questions.
        answers_file (str): The output file for answers.
    """
    # Read the questions from the XML file
    tree = ET.parse(questions_file)
    root = tree.getroot()

    # Separate questions based on topic_name
    topics = set()

    for question in root.iterfind('./question'):
        topic_name = question.find('topic_name').text
        if topic_name.startswith(GENERAL_PREFIX):
            topic_name = GENERAL_PREFIX
            question.find('topic_name').text = GENERAL_PREFIX
        topics.add(topic_name)

    # Open the output file in write mode
    with open(output_file, 'w') as f, open(answers_file, 'w') as ans_f:
        
        f.write('\\documentclass[8pt]{extarticle}\n')  # Set the font size to 8pt
        f.write('\\usepackage{amsmath}\n')
        f.write('\\usepackage{enumitem}\n')
        f.write('\\usepackage{graphicx}\n')
        f.write('\\usepackage{titlesec}\n')
        f.write('\\usepackage{geometry}\n')
        f.write('\\usepackage{bm}\n')
        f.write('\\usepackage{amsfonts}\n')
        f.write('\\geometry{margin=1.5cm}\n')  # Set the reduced margins
        f.write('\\titleformat{\\section}[block]{\\Large\\bfseries\\filcenter}{}{1em}{}\n\n')
        f.write('\\usepackage{fancyhdr}\n')
        f.write('\\pagestyle{fancy}\n')
        f.write('\\fancyhf{}\n')
        f.write('\\renewcommand{\\headrulewidth}{0pt}\n')
        f.write('\\fancyhead[R]{\\bf{\\MakeUppercase{\\leftmark}}}\n')
        f.write('\\begin{document}\n')

        # Check if 'General' section is present
        if 'General' in topics:
            # Section for 'General' questions
            f.write('\\section{General Section}\n')

            # Find questions with the topic_name 'General'
            general_questions = root.findall('./question[topic_name="General"]')

            # Shuffle the questions randomly
            random.shuffle(general_questions)

            # Take at most MAX_GENERAL_QUESTIONS questions
            selected_general_questions = general_questions[:MAX_GENERAL_QUESTIONS]

            # Track the question count for 'General' section
            question_count = 0

            # Process the selected 'General' questions
            for question in selected_general_questions:
                question_count += 1
                process_question(question, f, ans_f, question_count)

            # Add some space between sections
            f.write('\\newpage\n')

            # Remove 'General' from topics
            topics.remove('General')
        # Track the question count for each section
        question_count = MAX_GENERAL_QUESTIONS
        # Iterate over topics
        for topic_name in topics:
            # Section for each topic
            f.write('\\section{' + os.path.splitext(topic_name)[0] + ' Section}\n')

            # Find questions with the specified topic_name
            questions = root.findall('./question[topic_name="' + topic_name + '"]')

            # Shuffle the questions randomly
            random.shuffle(questions)

            # Take at most MAX_QUESTIONS_PER_SECTION questions
            selected_questions = questions[:MAX_QUESTIONS_PER_SECTION]

            # Process the selected questions
            for question in selected_questions:
                question_count += 1
                process_question(question, f, ans_f, question_count)

            # Add some space between sections
            f.write('\\newpage\n')

        f.write('\\end{document}\n')

    print('LaTeX files generated successfully.')

# Example usage
questions_file = 'PHDbank.xml'
output_file = 'PHDquestions.tex'
answers_file = 'PHDanswers.tex'
generate_latex_files(questions_file, output_file, answers_file)
