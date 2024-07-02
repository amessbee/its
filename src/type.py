import xml.etree.ElementTree as ET

## Remove types: Dangerous and irreversible - USE WITH CARE
# **This will remove type tag of each question in the bank.xml. This should not be used unless you know what you are doing. Essentially if you feel that original assignment is wrong, you will have to reassign each topic using above script.**


# Function to prompt the user for confirmation
def ask_for_confirmation():
    prompt = "This code will irreversibly change the bank. Do you really want to run it? Type 'yes' to confirm: "
    user_input = input(prompt)
    return user_input.lower() == 'yes'
    
def remove_type_tags(bank_file):
    if ask_for_confirmation() == False:
        print("Operation canceled by the user.")
        return
    else:
        # Parse the XML file
        bank_tree = ET.parse(bank_file)
        bank_root = bank_tree.getroot()
    
        # Iterate over all question elements and remove 'type' tags
        for question_elem in bank_root.findall('.//question'):
            # Find the 'type' element
            type_elem = question_elem.find('type')
            if type_elem is not None:
                # Remove the 'type' element from the question
                question_elem.remove(type_elem)
    
        # Save the updated XML back to the file
        bank_tree.write(bank_file)

# Example usage
# bank_file_path = 'bank.xml'
# remove_type_tags(bank_file_path)


## ADD TYPES BASED ON TOPIC

# **We will use types to create the actual test. For BS test type 1 represents analytical reasoning questions and type 2 is mathematical. Although there is quite an overlap.**

def normalize_topic(topic):
    """Normalize the topic by converting it to lowercase and removing spaces."""
    return ''.join(topic.lower().split())

def assign_question_types(bank_file):
    # Parse the XML file
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # Dictionary to keep track of topic types already known
    topic_types = {}

    # Process each question to assign a type based on topic
    for question_elem in bank_root.findall('.//question'):
        topic_elem = question_elem.find('topic')
        if topic_elem is not None:
            # Normalize the topic text
            topic = normalize_topic(topic_elem.text)

            # Check if the type is already assigned
            type_elem = question_elem.find('type')
            if type_elem is not None:
                # Skip this question as it already has a type
                continue

            # If the type is new or not assigned, check if known, ask the user if not
            if topic not in topic_types:
                print(f"Enter the type for topic '{topic}' (1 for Type 1, 2 for Type 2):")
                type_input = input()
                type_name = '1' if type_input == '1' else '2'
                topic_types[topic] = type_name

            # Add the type element to the question since it's confirmed not to have one
            type_elem = ET.SubElement(question_elem, 'type')
            type_elem.text = topic_types[topic]

    # Save the updated XML with types assigned
    bank_tree.write(bank_file)

# Example usage, when you're ready to test:
# bank_file_path = 'bank.xml'
# assign_question_types(bank_file_path)
