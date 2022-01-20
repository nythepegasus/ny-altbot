const fs = require('fs');
const { REST } = require('@discordjs/rest');
const { Routes } = require('discord-api-types/v9');
const { clientId, guildId, token } = require('../config.json');

const commandList = [];
const commandFiles = fs.readdirSync('./commands').filter(file => file.endsWith('.js'));

for (const file of commandFiles) {
	const command = require(`../commands/${file}`);
	commandList.push(command.data.toJSON());
}


const rest = new REST({ version: '9' }).setToken(token);

rest.put(Routes.applicationGuildCommands(clientId, guildId), { body: commandList })
	.then(response => {
		console.log('Successfully registered application commands.');
		console.log(response);
		const commands = [];
		for (const command of response) {
			commands.push({ 'name': command.name, 'id': command.id });
		}
		fs.writeFile('commands.json', JSON.stringify(commands, null, 2), 'utf-8', (err) => {
			if (err) console.error(err);
		});
	})
	.catch(console.error);

