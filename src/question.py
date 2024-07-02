import xml.etree.ElementTree as ET

## Remove Question Number attribute from question Element in bank.xml
# **We use question_number tag. If there is an attribute then let us remove it.**
def remove_question_number_attribute(bank_file):
    # Parse the existing question bank XML
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # Iterate over each question in the bank
    for question_elem in bank_root.iter('question'):
        # Check if the question_number attribute exists
        if 'question_number' in question_elem.attrib:
            # Remove the question_number attribute
            del question_elem.attrib['question_number']

    # Save the modified XML back to the file
    bank_tree.write(bank_file, xml_declaration=True, encoding='utf-8')

# Example usage
bank_file_path = 'bank.xml'
remove_question_number_attribute(bank_file_path)
