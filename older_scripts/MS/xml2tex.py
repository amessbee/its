import xml.etree.ElementTree as ET

def process_question(question, f, ans_f, question_count):
    question_text = question.find('text').text
    options = question.find('options')
    answer = question.find('answer').text
    author = question.find('author').text

    # Write the question text and author
    f.write('\\noindent \\textbf{' + str(question_count) + '}. ' + question_text + '\n')
    #f.write('\\textit{Author: ' + author + '}\n')

    # Write the figure if available
    figure = question.find('figure')
    if figure is not None:
        figure_path = figure.text
        f.write('\\begin{figure}[!h]\n')
        f.write('\\centering\n')
        f.write('\\includegraphics[width=0.5\\textwidth]{' + figure_path + '}\n')
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
    # Read the questions from the XML file
    tree = ET.parse(questions_file)
    root = tree.getroot()

    # Separate questions based on topic_name
    analytical_questions = []
    other_questions = []
    analytical_groups = []
    other_groups = []
    

    for question in root.iterfind('./question'):
        topic_name = question.find('topic_name').text
        if topic_name == 'Analytical':
            analytical_questions.append(question)
        else:
            other_questions.append(question)
    
    for group in root.iterfind('./question_group'):
        topic_name = group.find('topic_name').text
        if topic_name == 'Analytical':
            analytical_groups.append(group)
        else:
            other_groups.append(group)

    # Open the output file in write mode
    with open(output_file, 'w') as f, open(answers_file, 'w') as ans_f:
        #f.write('\\documentclass{article}\n')
        f.write('\\documentclass[8pt]{extarticle}\n')  # Set the font size to 8pt
        f.write('\\usepackage{amsmath}\n')
        f.write('\\usepackage{enumitem}\n')
        f.write('\\usepackage{graphicx}\n')
        f.write('\\usepackage{titlesec}\n')
        f.write('\\usepackage{geometry}\n')
        f.write('\\geometry{margin=1.5cm}\n')  # Set the reduced margins
        f.write('\\titleformat{\\section}[block]{\\Large\\bfseries\\filcenter}{}{1em}{}\n\n')
        f.write('\\usepackage{fancyhdr}\n')
        f.write('\\pagestyle{fancy}\n')
        f.write('\\fancyhf{}\n')
        f.write('\\renewcommand{\\headrulewidth}{0pt}\n')
        f.write('\\fancyhead[R]{\\bf{\\MakeUppercase{\\leftmark}}}\n')
        f.write('\\begin{document}\n')

        
        question_count = 0  # Track the overall question count

        # Section for Analytical questions
        f.write('\\section{Analytical Section}\n')

        
        # Iterate over the analytical questions
        for group in analytical_groups:
            
            group_text = group.find('./text').text
            
            f.write(str(group_text) + ' \\\\')
            f.write('\n')
            # Write the figure if available
            figure = group.find('figure')
            if figure is not None:
                figure_path = figure.text
                f.write('\\begin{figure}[!h]\n')
                f.write('\\centering\n')
                f.write('\\includegraphics[width=0.45\\textwidth]{' + figure_path + '}\n')
                f.write('\\end{figure}\n\n')
                
            for question in group.iterfind('./question'):
                question_count += 1
                process_question(question, f, ans_f, question_count)  
            

        for question in analytical_questions:
            question_count += 1
            process_question(question, f, ans_f, question_count)

        # Section for Other questions
        f.write('\\section{Computer Science Section}\n')

        # Iterate over the other questions
        for group in other_groups:
            
            group_text = group.find('./text').text
            #f.write(' \\textbf{' + str(group_text) + '}. \\\\')
            f.write(str(group_text) + ' \\\\')
            f.write('\n')
            # Write the figure if available
            figure = group.find('figure')
            if figure is not None:
                figure_path = figure.text
                f.write('\\begin{figure}[!h]\n')
                f.write('\\centering\n')
                f.write('\\includegraphics[width=0.45\\textwidth]{' + figure_path + '}\n')
                f.write('\\end{figure}\n\n')

            for question in group.iterfind('./question'):
                question_count += 1
                process_question(question, f, ans_f, question_count)

        for question in other_questions:
            question_count += 1
            process_question(question, f, ans_f, question_count)

        f.write('\\end{document}\n')

    print('LaTeX files generated successfully.')

# Example usage
# questions_file = 'MSbank.xml'
# output_file = 'MSquestions.tex'
# answers_file = 'MSanswers.tex'
# generate_latex_files(questions_file, output_file, answers_file)


# Example usage
# questions_file = 'test1.xml'
# output_file = 'questions1.tex'
# answers_file = 'answers1.tex'
# generate_latex_files(questions_file, output_file, answers_file)


# questions_file = 'test2.xml'
# output_file = 'questions2.tex'
# answers_file = 'answers2.tex'
# generate_latex_files(questions_file, output_file, answers_file)
