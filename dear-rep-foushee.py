#!/usr/bin/env python3

import argparse
import sys
import json
import urllib
import time
import os
import urllib.request

# All the stuff we need to know about the user to send a message, which we save.
FIELDS = {
    "country": "country (probably USA)",
    "street": "street address (like 123 Wherever St.)",
    "city": "city (like Durham)",
    "state": "state (probably NC)",
    "zip": "zip code (like 27713-1234)",
    "prefix": "name prefix (like Mx./Mr./Ms.)",
    "first": "first name",
    "last": "last name",
    "email": "email address"    
}

DEFAULT_SUBJECT = "I urge Rep. Foushee to support a cease-fire"

DEFAULT_MESSAGE = """
Dear Rep. Foushee,

I am once again contacting you to ask you to call for a humanitarian cease-fire
in the ongoing conflict in Gaza, so that civilians do not die.

Sincerely,
- {first} {last}
"""

ENDPOINT = "https://foushee.house.gov/graphql"
# For testing changes to the script, comment out the above line and uncomment
# this line below, to avoid sending nonsense to Rep. Valerie Foushee.
# ENDPOINT = "http://127.0.0.1:8080/"


def collect_field(field_name, human_field_name, db):
    """
    Make sure the key named field_name is in the dictionary db.
    
    If not, prompt for it using human_field_name, confirm the input, and save it.
    """
    if field_name not in db:
        while True:
            db[field_name] = input(f"Enter your {human_field_name}: ")
            print(f"You entered: {db[field_name]}. If correct, type 'y'.")
            if input("Correct [y/n]: ").lower() == "y":
                break
            
def send_message(subject, message, sender_data):
    """
    Send a message to Rep. Valerie Foushee.
    
    sender_data must be a dict with all the keys from FIELDS.
    """
    
    message_dict = {
        # This giant query string is sent by the web site's contact form to define the submission operation.
        "query": "mutation SubmitGravityFormsForm($formId: Int!, $clientMutationId: String, $fieldValues: [FieldValuesInput]) {\n  submitGravityFormsForm(\n    input: {formId: $formId, clientMutationId: $clientMutationId, fieldValues: $fieldValues}\n  ) {\n    entryId\n    errors {\n      id\n      message\n    }\n  }\n}\n",
        "variables": {
            "formId": 21,
            # Rep. Foushee seems to use the time here even though that can collide across clients.
            "clientMutationId": str(int(round(time.time() * 1000))),
            "fieldValues": [
                {
                    "id": 1,
                    "value": subject
                },
                {
                    "id": 2,
                    "value": message
                },
                {
                    "id": 5,
                    "addressValues": {
                        "country": sender_data["country"],
                        "street": sender_data["street"],
                        "city": sender_data["city"],
                        "state": sender_data["state"],
                        "zip": sender_data["zip"]
                    }
                },
                {
                    "id": 7,
                    "nameValues": {
                        "prefix": sender_data["prefix"],
                        "first": sender_data["first"],
                        "last": sender_data["last"]
                    }
                },
                {
                    "id": 8,
                    "emailValues": {
                        "value": sender_data["email"]
                    }
                },
                {
                    "id": 10,
                    "checkboxValues": []
                },
                {
                    # TODO: Right now topic is always international affairs, but it could be other allowed topics.
                    "id":16, "value": "International Affairs"
                }
            ]
        }
    }
    
    # Encode the form data
    json_bytes = json.dumps(message_dict).encode("utf-8")
    # Make the request
    request = urllib.request.Request(
        ENDPOINT,
        method="POST", 
        headers={"User-Agent": "dear-rep-foushee.py 1.0", "Content-Type": "application/json"},
        data=json_bytes
    )
    # Send it
    with urllib.request.urlopen(request) as response:
        if response.status != 200:
            print(f"Error code {response.status}")
            response_data = response.read()
            try:
                response_object = json.loads(response.read().decode("utf-8"))
                print("Entry ID: {}".format(response_object.get("data", {}).get("submitGravityFormsForm", {}).get("entryId", None)))
                print("Errors: {}".format(response_object.get("data", {}).get("submitGravityFormsForm", {}).get("errors", None)))
            except:
                print(f"Uninterpretable response data: {response_data}")
            sys.exit(1)
        else:
            print("Message accepted!")
            response_object = json.loads(response.read().decode("utf-8"))
            print("Entry ID: {}".format(response_object.get("data", {}).get("submitGravityFormsForm", {}).get("entryId", None)))
            print("Errors: {}".format(response_object.get("data", {}).get("submitGravityFormsForm", {}).get("errors", None)))
    
def main():
    
    if os.path.exists("sender-data.json"):
        print("Loading sender-data.json...")
        with open("sender-data.json") as saved_file:
            # Load saved name and address info.
            sender_data = json.load(saved_file)
    else:
        print("Collecting user info to sign message. This will only happen the first time!")
        sender_data = {}
        
    for field_name, human_field_name in FIELDS.items():
        # Make sure all fields are set
        collect_field(field_name, human_field_name, sender_data)
        
    with open("sender-data.json", "w") as h:
        # Save user data
        print("Saving sender-data.json...")
        json.dump(sender_data, h)
        
    if len(sys.argv) == 3:
        # User has set a command line message.
        print("Using message from command line...")
        subject = sys.argv[1]
        message = sys.argv[2]
    else:
        if os.path.exists("subject.txt"):
            print("Loading subject.txt...")
            subject = open("subject.txt").read()
        else:
            subject = DEFAULT_SUBJECT
        if os.path.exists("message.txt"):
            print("Loading message.txt...")
            message = open("message.txt").read()
        else:
            message = DEFAULT_MESSAGE
        
    print("Filling {placeholders} with sender information...")
    subject = subject.format(**sender_data)
    message = message.format(**sender_data)
    
    print("Message ready!")
    print()
    print(f"Subject: {subject}")
    print(f"Message: {message}")
    print()
    
    running_interactive = True
    try:
        if not sys.stdin.isatty():
            # If not running where we can talk to the user, auto-confirm sending.
            running_interactive = False
    except:
        pass
    
    if not running_interactive or input("Send and save [y/n]: ").lower() == "y":
        
        # Save message
        with open("subject.txt", "w") as h:
            print("Saving subject.txt...")
            h.write(subject)
        with open("message.txt", "w") as h:
            print("Saving message.txt...")
            h.write(message)
            
        send_message(subject, message, sender_data)
    else:
        print("Not sending or saving message. Goodbye!")
    
if __name__ == "__main__":
    main()


