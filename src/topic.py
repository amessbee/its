import xml.etree.ElementTree as ET

## Replace topic_name with topic
# **In some older questions, we had topic_name instead of topic - fixing that here.**
def update_topic_tags(bank_file):
    # Parse the XML file
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # To replace 'topic_name' with 'topic', we need to collect these elements first to avoid modifying the tree while iterating.
    topics_to_replace = []
    for topic_name_elem in bank_root.iter():
        for child in list(topic_name_elem):
            if child.tag == 'topic_name':
                topics_to_replace.append((topic_name_elem, child))

    # Now replace each 'topic_name' with 'topic'
    for parent, topic_name_elem in topics_to_replace:
        # Create a new 'topic' element with the same content
        topic_elem = ET.Element('topic')
        topic_elem.text = topic_name_elem.text

        # Insert the new 'topic' element right before the 'topic_name' element
        parent.insert(list(parent).index(topic_name_elem), topic_elem)

        # Remove the old 'topic_name' element
        parent.remove(topic_name_elem)

    # Save the updated XML back to the file
    bank_tree.write(bank_file)

# Example usage
# bank_file_path = 'bank.xml'
# update_topic_tags(bank_file_path)
