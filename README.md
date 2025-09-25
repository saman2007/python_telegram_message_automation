# Python Telegram Message Automation

## Note🚨🚨

> ⚠️ **Disclaimer**: This project is created for **educational purposes only**.  
> It is meant to demonstrate how to use the Telegram API with Python in a safe and responsible way.  
> **Do not use this project to send unsolicited messages, spam, or perform any harmful actions.**  
> The author is not responsible for misuse of this code.

## About
This repository provides a terminal UI to send automatic text messages and medias randomly, to a specified person in telegram. The goal of writing this project are:
- Work with the Telegram API.
- Send messages programmatically.
- Understand the basics of automation in Python.

It is **not** a production-suitable bot and must only be used in controlled, private environments for practice and learning purposes.

## Important Notes
- **Telegram Terms of Service** prohibit unsolicited or bulk messaging. Violating these rules can result in account bans.  
- **GitHub Acceptable Use Policy** does not allow harmful software. This project is structured as an educational project to stay compliant.  

## Safe Usage Recommendations
- Use only with **test accounts**.  
- Never use this with real users or in ways that could be considered spam. 

## Usage And Details
Here, I explain all options of the menu and some details in the app.

### How to run the app
1. Clone the app from this repo to your local machine.
2. Open a terminal in the path of the cloned app.
3. Create a `venv` by entering this in the terminal:  
`python -m venv .venv`  
4. After the `venv` is created, activate it by entering this in the terminal:  
`.venv/Scripts/activate`  
5. Then you have to install the packages in `requirements.txt` by entering this in the terminal:  
`pip install -r requirements.txt`  
6. Now you're ready! When your `venv` is activated, enter `python app.py` to run `app.py` which has the main functionality of the project.  
7. After you're done, you can deactivate your `venv` by entering this in the terminal:
`decativate`

### Initialization process
When you start the app, an initialization method will be executed.  
This initialization method creates you a `data` folder(if it is not already existed) that includes these files and folders: 
- `messages.json` for storing your added messages
- `data.json` to store your added accounts
- `media` folder for storing medias you want to send.

### Telegram Account Sessions
There is a folder called `sessions` that will be automatically created in case that it is not existed. After adding an account, the accounts session will be stored in this folder and after deleting an account, the created session will be deleted from this folder.

### Add a Telegram User(menu option)
To start using the app, you must get a telegram api and get its `API ID` and `API Hash` which you can get here: https://my.telegram.org/apps  
After you created a telegram api, select `Add a Telegram User` option from the menu. You will be asked to enter `API ID`, `API Hash` and `Phone Number`. After that, if your entered info are correct, a code will be sent to your telegram PV by telegram itself. after you entered that code and confirming the adding account, the account will be added to the app and a session will be created for your account.

### Show Telegram Users(menu option)
This option simply shows the `username`, `API ID`, `API Hash` and `Phone Number` of added users.

### Delete a Telegram User(menu option)
With this option, you can delete an added telegram user from the app. After deleting a user from the app, its data will be removed and the users session will be removed from the `sessions` folder.

### Add a Message(menu option)
With this option, you can add a message and it will be stored in the `messages.json` file in `data` folder and you can choose the added message later to be sent.

NOTE: This option is only for adding text messages. If you want to add medias, you have to go to `data` folder, then go to `media` folder and place the medias you want to add.

### Show Messages(menu option)
You can see the added text messages and medias with this option.

### Start Messaging(menu option)
This is the main option of this bot. By selecting this, you will be asked to choose the accounts that you want to message with, you can choose one or more account.  
Then, you will be asked to choose the text messages and medias to send. Note that the selected text and media messages will be sent randomly.  
After that, you have to enter the telegram usename of the user that you want to send message.  
Then, you will be asked the number of messages that you want to send. Please note that the selected number is the number of messages that will be send with each account.  
After that, sending messages will be started. To emphasis that this is not a spamming process, after that a message is sent, there will be a pause between 1 to 5 seconds.