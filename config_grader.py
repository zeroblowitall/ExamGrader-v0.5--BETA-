import json
import re
import config_grader

def grade_configuration(config_file, criteria_file):
    # Load the criteria from the criteria file
    with open(criteria_file, 'r') as f:
        criteria_dict = json.load(f)

    # Open the configuration file and read its contents
    with open(config_file, 'r') as f:
        config = f.read()

    # Grade the configuration based on the criteria
    total_weight = sum(c['weight'] for c in criteria_dict.values())
    score = 0

    matched_criteria = set()  # keep track of matched criteria

    # Check for shutdown command under G0/0/0
    matches_g0_0_0 = re.search(r"interface GigabitEthernet0/0/0(?:\s+.*)*\s+shutdown\s+!", config, flags=re.DOTALL)
    if matches_g0_0_0:
        score += criteria_dict['has_shutdown_on_GigabitEthernet0/0/0']['weight']
        matched_criteria.add('has_shutdown_on_GigabitEthernet0/0/0')
        print("Shutdown command found under GigabitEthernet0/0/0")

    # Check for shutdown command under G0/0/1
    matches_g0_0_1 = re.search(r"interface GigabitEthernet0/0/1(?:\s+.*)*\s+shutdown\s+!", config, flags=re.DOTALL)
    if matches_g0_0_1:
        score += criteria_dict['has_shutdown_on_GigabitEthernet0/0/1']['weight']
        matched_criteria.add('has_shutdown_on_GigabitEthernet0/0/1')
        print("Shutdown command found under GigabitEthernet0/0/1")

    for criterion, criteria_details in criteria_dict.items():
        if criterion in matched_criteria:
            continue  # already matched this criterion

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
    grade = (score / total_weight) * 100
    return grade, matched_criteria  # return set of matched criteria