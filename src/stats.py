import os
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

## Stats: Parse raw files and print frequency stats.
# Go through raw files and create simple stats as per need to see if there is something off and needs to be fixed.

def pullStatsFromNewRawQuestions(directory):
    global_stats = {
        'total_number_of_questions': 0,
        'global_topics': set(),
        'global_answer_distribution': Counter(),
        'global_difficulty_distribution': Counter(),
        'global_author_distribution': Counter(),
        'global_year_distribution': Counter()
    }
    
    stats = defaultdict(lambda: {
        'number_of_questions': 0,
        'topics': set(),
        'answer_distribution': Counter(),
        'difficulty_distribution': Counter(),
        'author_distribution': Counter(),
        'year_distribution': Counter()
    })
    
    # List all files in the specified directory
    for filename in os.listdir(directory):
        if filename.endswith(".xml"):  # Ensures we are only reading XML files
            path = os.path.join(directory, filename)
            tree = ET.parse(path)
            root = tree.getroot()
            
            # Process each question in the file
            for question in root.findall('.//question'):  # Use XPath to find questions regardless of parent
                stats[filename]['number_of_questions'] += 1
                global_stats['total_number_of_questions'] += 1
                
                topic_element = question.find('topic')
                if topic_element is not None:
                    topic = topic_element.text.strip()
                    stats[filename]['topics'].add(topic)
                    global_stats['global_topics'].add(topic)
                
                answer_element = question.find('answer')
                if answer_element is not None:
                    answer = answer_element.text.strip()
                    stats[filename]['answer_distribution'][answer] += 1
                    global_stats['global_answer_distribution'][answer] += 1
                
                difficulty_element = question.find('difficulty')
                if difficulty_element is not None:
                    difficulty = difficulty_element.text.strip()
                    stats[filename]['difficulty_distribution'][difficulty] += 1
                    global_stats['global_difficulty_distribution'][difficulty] += 1
                
                author_element = question.find('author')
                if author_element is not None:
                    author = author_element.text.strip()
                    stats[filename]['author_distribution'][author] += 1
                    global_stats['global_author_distribution'][author] += 1
                
                year_element = question.find('year')
                if year_element is not None:
                    year = year_element.text.strip()
                    stats[filename]['year_distribution'][year] += 1
                    global_stats['global_year_distribution'][year] += 1

    # Print the statistics for each file
    for file, data in stats.items():
        print(f"Stats for {file}:")
        print(f"  Number of Questions: {data['number_of_questions']}")
        print(f"  Topics: {', '.join(data['topics'])}")
        print(f"  Answer Distribution: {dict(data['answer_distribution'])}")
        print(f"  Difficulty Distribution: {dict(data['difficulty_distribution'])}")
        print(f"  Author Distribution: {dict(data['author_distribution'])}")
        print(f"  Year Distribution: {dict(data['year_distribution'])}")
        print("")

    # Print the aggregated global statistics
    print("Global Stats:")
    print(f"  Total Number of Questions: {global_stats['total_number_of_questions']}")
    print(f"  Global Topics: {', '.join(global_stats['global_topics'])}")
    print(f"  Global Answer Distribution: {dict(global_stats['global_answer_distribution'])}")
    print(f"  Global Difficulty Distribution: {dict(global_stats['global_difficulty_distribution'])}")

# Example usage
# parse_mcqs('new_files')


## Stats: Print questions of each topic
# Frequency of questions of each topic in bank.xml
# When asking people to create new questions, send them this list of topics.

def count_questions_by_topic(bank_file):
    # Parse the XML file
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # Dictionary to store topic counts
    topic_counts = {}

    # Helper function to increment count for a topic
    def increment_topic_count(topic):
        if topic in topic_counts:
            topic_counts[topic] += 1
        else:
            topic_counts[topic] = 1

    # Process each question and count topics
    for question_elem in bank_root.findall('.//question'):
        # Extract the topic from the question or from the parent group if available
        topic_elem = question_elem.find('topic')
        if topic_elem is not None:
            increment_topic_count(topic_elem.text.strip())
        else:
            # Check if this question is part of a group and get the group's topic
            parent_group = question_elem.find('../topic')
            if parent_group is not None:
                increment_topic_count(parent_group.text.strip())

    return topic_counts

# Example usage
# bank_file_path = 'bank.xml'
# topic_counts = count_questions_by_topic(bank_file_path)
# print(topic_counts)


## Stats: Print number of questions on each type in the bank.
# **This should help guide proportion of new questions each type needed to make bank.xml balanced as per test needs.**

def count_questions_by_type(bank_file):
    # Parse the XML file
    bank_tree = ET.parse(bank_file)
    bank_root = bank_tree.getroot()

    # Initialize counters for each type
    type_counts = {'1': 0, '2': 0, '3':0}

    # Iterate through all question elements
    for question_elem in bank_root.findall('.//question'):
        # Find the type element within each question
        type_elem = question_elem.find('type')
        if type_elem is not None:
            # Increment the count for the corresponding type
            if type_elem.text in type_counts:
                type_counts[type_elem.text] += 1
            else:
                # If a new type number is found, start counting it
                type_counts[type_elem.text] = 1
        else:
            type_counts['3'] += 1

    # Print the counts for each type
    for type_id, count in type_counts.items():
        print(f"Type {type_id}: {count} questions")

# Example usage
# bank_file_path = 'bank.xml'
# count_questions_by_type(bank_file_path)
