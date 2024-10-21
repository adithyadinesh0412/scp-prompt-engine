# brain/chat-gpt.py
import openai, json , os
import brain.scp_interface as scp
import configparser

#
# Assuming config.ini is in the same directory as this script
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

config = configparser.ConfigParser()
config.read(config_path)



# Set up your OpenAI API key
openai.api_key = config['CHAT_GPT']['API_KEY']


def get_chatgpt_response(message):
    """
    This function sends a message to the ChatGPT API and returns the response.
    """
    try:
        # Send the client's message to OpenAI ChatGPT and get a response
        response = openai.ChatCompletion.create(
            model= "gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an education leadership catalysing expert."},
                {"role": "user", "content": create_prompt(message)}
            ]
        )

        # Get the JSON response content from ChatGPT
        chatgpt_response = response.choices[0].message['content'].strip()
        
        # Pass the JSON response to another function for processing
        project_id = scp.create_project(chatgpt_response)
        return chatgpt_response
    # "A project with id : " + str(project_id) + " has been created. Please check and make relevant changes to submit."  
    except Exception as e:
        return f"Error communicating with ChatGPT: {str(e)}"

def create_prompt(message):
    project_json = scp.construct_project_json()

    # Construct the prompt for ChatGPT
    prompt = f"""
    I want you to help me create a single line JSON response based on the subject prompt I will provide.Remove all additional spaces and tabs , \n \t and \ in the json response. 
    Make sure to have multiple tasks if needed for the project.
    Here is the JSON structure I want you to follow and the meaning of each key is provided as value in the json:
    {json.dumps(project_json, indent=4)}

    Now, based on the subject prompt I will provide, generate a JSON response that fits the above structure. 

    Subject prompt: {message}
    """

    return prompt