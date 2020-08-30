# A Telegram ChatBot that reminds you of birthdays

This is a chatbot that can remind you of birthdays that has been scraped from facebook.

>Since the Web API is unable to give access to your friends' birthdays, a tool called [fb2cal](https://github.com/mobeigi/fb2cal) has been used, which was written by mobeigi(with changes made to accomodate multiple users at a time). Since it uses web scraping, unfortunately usage of the update command can prompt a change password req from facebook. The readme of fb2cal is given inside the fb2cal subfolder.

## How to deploy the bot
1. Install all the required modules using
`pip install -r requirements.txt`
2. Put you telegram chatbot's credentials in a `config.cfg` file, under `[CREDS]` section under the field `token` 
3. Run the python script
`python server_V2.py `


## Things this has:

- a config.cfg file to save the token details
> Under the creds tag, create a token field with your chatbot api in it.
- a bot.py file that has all the script related to the bot
- a server_V2.py file for server deployment
- a ics2python.py file that handles the interface with .ics file
- fb2cal that does all the hard work

## Supported Commands

* `/start` to display the start message
* `/update` to update the .ics file
* `/uname` to configure the credentials
 

## Known Shortcomings
* Cannot properly handle error flags put up by the fb2cal app
* Has to automate a lot of stuff, including auto updation and auto reminding
* Has to be able to send messages to people in your contacts
* The username/ password combo is stored without any kind of encryption