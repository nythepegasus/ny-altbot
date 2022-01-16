# Ny AltBot
This is Nythepegasus's implementation of AltBot for the Delta servers. This bot attempts to implement all the commands the old bot had, and introduce more features. 

## Features
 * Verification before entry to the server using captcha
 * Sending of AltStore source updates to update channels
 * Get Apple server statuses

## Installation
Make sure you have Node v16.6 or higher, as this bot uses discord.js v13.
Also make sure you have npm installed, then run the following line inside the project directory:

```
npm install
```

Then you'll have to fill out `config.json` with the required credentials (use `example-config.json` as a template).

Finally to run your bot, you can either run `node index.js` or `npm start` and your bot should start up! 

## Contributing
If you want to contribute to the bot in any way, feel free! I'll try and throw together some Github templates for pull requests and issues eventually. 

### Credits

[DeltaBot](https://github.com/deltadiscordbot/deltabot) by Jimmy#9999

For the creation of the original bot.

[Joelle (Lonkle)](https://github.com/lonkle)

For giving me the inspiration to continue creating the bot.
