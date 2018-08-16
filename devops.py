"""
devops.py
~~~
Script that checks each JSON intent to make sure the intent is properly configured.
"""

import os
from os import listdir
from os.path import isfile, join
import json


def write_output(current_agent: str, end_intent_present: str, no_webhook_list: list, no_default_fulfillment: list,
                 greater_640_fulfillment: list, no_default_front: list):
    """
    Writes the output of the script to a file (output_summary.txt).

    Args:
        current_agent (str): The current agent.
        end_intent_present: Whether an end intent is present.
        no_webhook_list: List of intents with no webhook call.
        no_default_fulfillment: List of intents with no default fulfillment message.
        greater_640_fulfillment: List of intents with default fulfillment or simple responses with > 640 characters.
        no_default_front: List of intents with no default fulfillment message in front.
    Returns:
        None
    """
    # Writes the output of the script to another file
    with open(output_file, file_mode) as output_write:
        output_write.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n")
        output_write.write("Results for {agent_name}\n".format(agent_name=current_agent))
        output_write.write("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n")

        output_write.write("Have end of conversation intent? {}".format(end_intent_present))

        output_write.write("\n\n")

        if no_webhook_list:
            output_write.write("--------\n")
            output_write.write("INTENTS WITH NO WEBHOOK ENABLED\n")
            output_write.write("--------\n\n")
            for intent in no_webhook_list:
                output_write.write(intent + "\n")
            output_write.write("\n")

        if no_default_fulfillment:
            output_write.write("--------\n")
            output_write.write("INTENTS WITH NO DEFAULT FULFILLMENT TEXT\n")
            output_write.write("--------\n\n")
            for intent in no_default_fulfillment:
                output_write.write(intent + "\n")
            output_write.write("\n")

        if greater_640_fulfillment:
            output_write.write("--------\n")
            output_write.write("INTENTS WITH FULFILLMENT TEXT LONGER THAN 640 CHARACTERS\n")
            output_write.write("--------\n\n")
            for intent in greater_640_fulfillment:
                output_write.write(intent + "\n")
            output_write.write("\n")

        if no_default_front:
            output_write.write("--------\n")
            output_write.write("INTENTS WITH DEFAULT FULFILLMENT TEXT NOT SET TO THE FRONT OF RICH RESPONSES\n")
            output_write.write("--------\n\n")
            for intent in no_default_front:
                output_write.write(intent + '\n')
            output_write.write("\n")

        if no_accessibility_text:
            output_write.write("--------\n")
            output_write.write("INTENTS WITH NO ACCESSIBILITY TEXT\n")
            output_write.write("--------\n\n")
            for intent in no_accessibility_text:
                output_write.write(intent + '\n')
            output_write.write("\n")

        if not no_default_front and not no_default_fulfillment and not no_webhook_list and not greater_640_fulfillment:
            output_write.write("No problems found in any of the intents! Good job!")
            output_write.write("\n\n")

        output_write.write("--------\n")
        output_write.write("ALL INTENTS \n")
        output_write.write("--------\n\n")
        for intent in all_intents:
            output_write.write(intent + "\n")
        output_write.write("\n")

        output_write.write("\n\n\n")


# MAKE SURE TO CHANGE WHEN TESTING DIFFERENT AGENTS
# current_agent = 'Test (2) 2'

current_directory = os.path.dirname(os.path.realpath(__file__))
projects_path = join(current_directory, 'project_files')
output_file = join(current_directory, 'output_summary.txt')

file_mode = "w+"

for project in listdir(projects_path):
    # Get the agent name
    current_agent = project
    intents_directory = join(current_directory, 'project_files/', current_agent, 'intents')
    agent_f_path = join(current_directory, 'project_files/', current_agent, 'agent.json')

    # Create the output lists
    endIntentPresent = True
    no_webhook_list = []
    no_default_fulfillment = []
    greater_640_fulfillment = []
    no_default_front = []
    no_accessibility_text = []
    all_intents = []

    # Check for end of conversation intents
    with open(file=agent_f_path, mode='r') as f:
        j = f.read()

        agent_d = json.loads(j)
        end_intents = agent_d["googleAssistant"]["endIntentIds"]

        if not end_intents:
            print("There are no end intents, probably because Google integration is missing. You need end "
                  "intents both Google and Alexa.")
            endIntentPresent = False

    intent_files = [f for f in listdir(intents_directory) if isfile(join(intents_directory, f))]

    # Make sure we are running the script, not importing it and then calling it from another script
    if __name__ == '__main__':
        # Iterate through all intents
        for i, intent_f_name in enumerate(intent_files):
            # Skip all of the files containing usersays_en.json, those are the training phrases
            if 'usersays_en.json' in intent_f_name:
                continue

            f_path = join(intents_directory, intent_f_name)

            with open(file=f_path, mode='r') as f:
                j = f.read()

            intent_d = json.loads(j)
            intent_name = intent_d.get("name")
            all_intents.append(intent_name)
            print("Processing intent {i}".format(i=i))

            # Checks that the webhook call is enabled
            if not intent_d.get("webhookUsed"):
                print("This intent {intent_name} does not have webhook. ".format(intent_name=intent_name))
                no_webhook_list.append(intent_name)

            # Checks that the default fulfillment text exists and the default fulfillment text is less than 640 characters
            responses = intent_d["responses"][0]
            messages = responses["messages"]
            default_fulfillment = list(filter(lambda d: d.get("type") == 0
                                              and d.get("platform") != "facebook"
                                              and d.get("platform") != "google",
                                              messages))

            if not len(default_fulfillment) or not default_fulfillment[0]["speech"]:
                print("The intent {intent_name} does not have a default fulfillment.")
                no_default_fulfillment.append(intent_name)
            else:
                for df in default_fulfillment:
                    # the speech is either a list or a string
                    if type(df.get("speech")) == list:
                        for text in df.get("speech"):
                            if len(text) >= 640:
                                print("This intent {intent_name} has a fulfillment response greater than 640 characters."
                                      .format(intent_name=intent_name))
                                greater_640_fulfillment.append(intent_name)
                                break
                    else:
                        if len(df.get("speech")) > 640:
                            print("This intent {intent_name} has a fulfillment response greater than 640 characters."
                                  .format(intent_name=intent_name))
                            greater_640_fulfillment.append(intent_name)

            # Checks to make sure the default response is set to appear in front of the rich responses for Google
            # Assistant
            default_response_platform = responses["defaultResponsePlatforms"]
            if not default_response_platform.get("google"):
                print("This intent {intent_name} has a default response not set to the beginning of the GA rich response.")
                no_default_front.append(intent_name)

            # Checks for accessibility text in lists
            list_elements = list(filter(lambda d: d["type"] == "list_card" and d["platform"] == "google", messages))
            for le in list_elements:
                le_items = le["items"]
                for item in le_items:
                    if not item.get("image").get("accessibilityText"):
                        print("This intent {intent_name} has no accessibility text.".format(intent_name=intent_name))
                        no_accessibility_text.append(intent_name)
                        break

            # Checks the simple responses of the Google Assistant for text that is greater than 640 characters
            simple_responses = list(filter(lambda d: d["type"] == "simple_response" and d["platform"] == "google",
                                           messages))
            for sr in simple_responses:
                # the text is either in the string "textToSpeech" or in multiple strings "textToSpeech" in "items" list
                if sr.get("textToSpeech"):
                    if len(sr["textToSpeech"]) > 640:
                        print("This intent {intent_name} has a fulfillment response greater than 640 characters."
                              .format(intent_name=intent_name))
                        if intent_name not in greater_640_fulfillment:
                            greater_640_fulfillment.append(intent_name)
                else:
                    for item in sr.get("items"):
                        if len(item["textToSpeech"]) > 640:
                            print("This intent {intent_name} has a fulfillment response greater than 640 characters."
                                  .format(intent_name=intent_name))
                            if intent_name not in greater_640_fulfillment:
                                greater_640_fulfillment.append(intent_name)
                            break

        # Write output to another file
        write_output(current_agent, endIntentPresent, no_webhook_list, no_default_fulfillment, greater_640_fulfillment,
                     no_default_front)

        # Change the file write mode to append
        file_mode = "a"

    else:
        print("Please run the script file.")
