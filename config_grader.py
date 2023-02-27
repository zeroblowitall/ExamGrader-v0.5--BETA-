import json
import re

def grade_configuration(config_file, criteria_file):
    # Load the criteria from the criteria file
    with open(criteria_file, 'r') as f:
        criteria_dict = json.load(f)

    # Open the configuration file and read its contents
    with open(config_file, 'r') as f:
        config = f.read()

    # Grade the configuration based on the criteria
    # 10 marks for device erasure. -10 allocated in criteria.json file i parser view still in config file
    #total_weight = 10.0
    score = 10.0
    
    matched_criteria = set()  # keep track of matched criteria

    for criterion, criteria_details in criteria_dict.items():
        answer = criteria_details['answer']
        weight = criteria_details['weight']
        is_regex = criteria_details.get('regex', False)
        if is_regex:
            matches = re.search(answer, config, flags=re.DOTALL)
            if matches:
                score += weight
                matched_criteria.add(criterion)  # add matched criterion to set
                print(f"Regex pattern '{answer}' matched in criterion '{criterion}'")
        else:
            if answer in config:
                score += weight
                matched_criteria.add(criterion)  # add matched criterion to set

    # Calculate the percentage grade
    grade = score
    return grade, matched_criteria  # return set of matched criteria

def get_matched_criteria(config, criteria_dict):
    # Find which criteria match the configuration
    matched_criteria = set()

    for criterion, criteria_details in criteria_dict.items():
        answer = criteria_details['answer']
        is_regex = criteria_details.get('regex', False)
        if is_regex:
            matches = re.search(answer, config, flags=re.DOTALL)
            if matches:
                matched_criteria.add(criterion)
        else:
            if answer in config:
                matched_criteria.add(criterion)

    return matched_criteria
             
    # Calculate the percentage grade
    grade = score

    return grade
