from flask import Flask, request, jsonify
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()  # Loads API keys and config

app = Flask(__name__)

# Command mapping for user input
COMMANDS = {
    'TEXT': 'Simple text message',
    'IMAGE': 'Send image',
    'DOCUMENT': 'Send document',
    'VIDEO': 'Send video',
    'CONTACT': 'Send contact',
    'PRODUCT': 'Send product',
    'GROUP_CREATE': 'Create group',
    'GROUP_TEXT': 'Simple text message for the group',
    'GROUPS_IDS': "Get the id's of your three groups"
}

# File paths for media sending
FILES = {
    'IMAGE': './files/file_example_JPG_100kB.jpg',
    'DOCUMENT': './files/file-example_PDF_500_kB.pdf',
    'VIDEO': './files/file_example_MP4_480_1_5MG.mp4',
    'VCARD': './files/sample-vcard.txt'
}


def send_whapi_request(endpoint, params=None, method='POST'):
    """
    Send a request to the Whapi.Cloud API.
    Handles both JSON and multipart (media) requests.
    """
    headers = {
        'Authorization': f"Bearer {os.getenv('TOKEN')}"
    }
    url = f"{os.getenv('API_URL')}/{endpoint}"
    if params:
        if 'media' in params:
            # Handle file upload for media messages
            details = params.pop('media').split(';')
            with open(details[0], 'rb') as file:
                m = MultipartEncoder(fields={**params, 'media': (details[0], file, details[1])})
                headers['Content-Type'] = m.content_type
                response = requests.request(method, url, data=m, headers=headers)
        elif method == 'GET':
            response = requests.get(url, params=params, headers=headers)
        else:
            headers['Content-Type'] = 'application/json'
            response = requests.request(method, url, json=params, headers=headers)
    else:
        response = requests.request(method, url, headers=headers)
    print('Whapi response:', response.json())  # Debug output
    return response.json()


def set_hook():
    """
    Register webhook URL with Whapi.Cloud if BOT_URL is set.
    """
    if os.getenv('BOT_URL'):
        settings = {
            'webhooks': [
                {
                    'url': os.getenv('BOT_URL'),
                    'events': [
                        {'type': "messages", 'method': "post"}
                    ],
                    'mode': "method"
                }
            ]
        }
        send_whapi_request('settings', settings, 'PATCH')


def ask_openai(prompt):
    """
    Send a prompt to OpenAI ChatGPT and return the response.
    """
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


@app.route('/hook/messages', methods=['POST'])
def handle_new_messages():
    """
    Main webhook handler for incoming WhatsApp messages.
    Determines command and sends appropriate response.
    """
    try:
        messages = request.json.get('messages', [])
        endpoint = None
        for message in messages:
            if message.get('from_me'):
                continue  # Ignore messages sent by the bot itself
            sender = {'to': message.get('chat_id')}
            command_input = message.get('text', {}).get('body', '').strip()
            # Check for AI command
            if command_input.lower().startswith('/ai '):
                user_prompt = command_input[4:].strip()
                if not user_prompt:
                    sender['body'] = 'Please provide a prompt after /AI.'
                else:
                    try:
                        ai_response = ask_openai(user_prompt)
                        sender['body'] = ai_response
                    except Exception as e:
                        sender['body'] = f"OpenAI error: {e}"
                endpoint = 'messages/text'
            else:
                # Map numeric input to command
                command = list(COMMANDS.keys())[int(command_input) - 1] if command_input.isdigit() else None

                if command == 'TEXT':
                    sender['body'] = 'Simple text message'
                    endpoint = 'messages/text'
                elif command == 'IMAGE':
                    sender['caption'] = 'Text under the photo.'
                    sender['media'] = FILES['IMAGE'] + ';image/jpeg'
                    endpoint = 'messages/image'
                elif command == 'DOCUMENT':
                    sender['caption'] = 'Text under the document.'
                    sender['media'] = FILES['DOCUMENT'] + ';application/pdf'
                    endpoint = 'messages/document'
                elif command == 'VIDEO':
                    sender['caption'] = 'Text under the video.'
                    sender['media'] = FILES['VIDEO'] + ';video/mp4'
                    endpoint = 'messages/video'
                elif command == 'CONTACT':
                    sender['name'] = 'Whapi Test'
                    with open(FILES['VCARD'], 'r') as vcard_file:
                        sender['vcard'] = vcard_file.read()
                        endpoint = 'messages/contact'
                elif command == 'PRODUCT':
                    # Send product info (requires valid PRODUCT_ID in .env)
                    product_id = os.getenv('PRODUCT_ID')
                    endpoint = f'business/products/{product_id}'
                elif command == 'GROUP_CREATE':
                    # Create a new WhatsApp group with the sender as participant
                    participants = [message.get('chat_id').split('@')[0]]
                    response = send_whapi_request('groups', {'subject': 'Whapi.Cloud Test', 'participants': participants})
                    sender['body'] = f"Group created. Group id: {response.get('group_id')}" if response.get('group_id') else 'Error'
                    endpoint = 'messages/text'
                elif command == 'GROUP_TEXT':
                    # Send a message to a group (requires GROUP_ID in .env)
                    sender['to'] = os.getenv('GROUP_ID')
                    sender['body'] = 'Simple text message for the group'
                    endpoint = 'messages/text'
                elif command == 'GROUPS_IDS':
                    # Get IDs and names of up to 3 groups
                    groups_response = send_whapi_request('groups', {'count': 3}, 'GET')
                    groups = groups_response.get('groups', [])
                    sender['body'] = ',\n '.join(f"{group['id']} - {group['name']}" for group in groups) if groups else 'No groups'
                    endpoint = 'messages/text'
                else:
                    # Default reply with command list
                    sender['body'] = (
                        "Hi. Send me a number from the list to try a command, or use /AI <your message> to chat with ChatGPT.\n\n"
                        + '\n'.join(f"{i + 1}. {text}" for i, text in enumerate(COMMANDS.values()))
                    )
                    endpoint = 'messages/text'

        if endpoint is None:
            return 'Ok', 200  # No valid command found
        response = send_whapi_request(endpoint, sender)
        print(f"Response from Whapi: {response}")  # Debug output
        return 'Ok', 200
    
    except Exception as e:
        print(e)
        return str(e), 500


@app.route('/', methods=['GET'])
def index():
    """
    Health check endpoint.
    """
    return 'Bot is running'


if __name__ == '__main__':
    set_hook()  # Register webhook on startup
    port = os.getenv('PORT') or (443 if os.getenv('BOT_URL', '').startswith('https:') else 80)
    app.run(port=port, debug=True)
