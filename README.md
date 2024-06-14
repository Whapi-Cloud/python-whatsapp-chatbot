# Python Whatsapp ChatBot
WhatsApp Python Bot. The basic functionality you will need when developing a bot: sending and receiving messages, sending a picture, file, document, video, as well as creating a group and sending a message to the WhatsApp group

## WhatsApp Python Bot (Whapi.Cloud WhatsApp API)
This example of the WhatsApp bot implementation touches in detail on the most frequently used functionality: send message, send file, create group, send message to WhatsApp Group. This will allow you to adapt WhatsApp API and source code to your tasks and needs, or take it as a basis for creating any other integration.
In the source code of the bot you will find the following functionality:
<ul>
  <li class="d-flex">Respond to an unfamiliar command, this could be an instruction or your welcome message;</li>
  <li class="d-flex">Send regular message;</li>
  <li class="d-flex">Send image;</li>
  <li class="d-flex">Send file;</li>
  <li class="d-flex">Send video;</li>
  <li class="d-flex">Send contact (vCard);</li>
  <li class="d-flex">Send product;</li>
  <li class="d-flex">Create new group, send an invitation and send message to the group;</li>
  <li class="d-flex">Receive and reading incoming messages;</li>
</ul>

<em>For the bot to work, it is <b>NOT REQUIRED</b> that the phone is turned on or online. Connect the number and test the integration comfortably!</em> <br/> And if you need any help, just write to us in the support chat on any page of the site: https://whapi.cloud/features

## Getting Started

### Step 1: Install Python and pip
1. Download and install Python from the official website https://python.org.
2. Verify that pip is installed along with Python.

### Step 2: Install Dependencies
Install the necessary libraries listed in requirements.txt:
1. Open the command line or terminal.
2. Navigate to your project directory.
3. Run the command:
```sh
pip install -r requirements.txt
```
This installs all libraries specified in the requirements.txt file.

### Step 3: Configure the Project
Configure your project settings: Open the <b>.env</b> file in your IDE. Set up configurations such as your API token and webhook URL

### Step 4: Run the Bot
Launch your bot using Python:
1. Ensure you are in the project directory in your terminal.
2. Execute the command:
```sh
python index.py
```

Learn more about how to configure the webhook to work locally here: https://support.whapi.cloud/help-desk/receiving/webhooks/how-to-check-the-webhook#how-to-test-webhook-locally 

### How to Connect to Whapi.Cloud and get API Token
Registration: https://panel.whapi.cloud/register
The first step is to register on the Whapi.Cloud website and create an account. <b>It's free and doesn't require you to enter a credit card.</b>
After registration you will immediately have access to a test channel with a small limitation. Wait for it to start (it usually takes about a minute). You will need to connect your phone for Whatsapp automation. It is from the connected phone that messages will be sent. The big advantage of the service is that it takes only a couple of minutes to launch and start working.

![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ep3pc4jsna9pzagfouj8.png)

To connect your phone, use the QR code available when you click on your trial channel in your personal account. Then open WhatsApp on your mobile device, go to Settings -> Connected devices -> Connect device -> Scan QR code.

In the second and third steps, the service will ask you to customize the channel: write its name for your convenience, set webhooks, change settings. All these steps can be skipped, and we will come back to webhooks a little later. After launching, you will find in the center block under the information about limits, your API KEY, that is Token. This token will be used to authenticate your API requests. Generally, it's added to the request headers as a Bearer Token or simply as a request parameter, depending on the API method you're using.

