const fs = require("fs");
const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    needsMod: true,
    data: new SlashCommandBuilder()
    .setName("removeupdatechannel")
    .setDescription("Remove an update channel to be notified on source updates")
    .setDefaultPermission(false)
    .addChannelOption(option => 
        option.setName("channel")
        .setDescription("Channel to add to the list")
        .setRequired(true)),
    async execute(interaction) {
        let client = interaction.client;
        let channel = interaction.options.getChannel("channel");
        fs.readFile('config.json', 'utf8', (err, data) => {
            if (err) {
                console.log(err);
            } else {
                let prev = JSON.parse(data);
                if (!prev.update_channels.includes(channel.id)) {
                    return interaction.reply({ content : `<#${channel.id}> is not an update channel.`, ephemeral : true });
                } else {
                    interaction.reply({ content : `<#${channel.id}> is removed as an update channel!`, ephemeral : true });
                    client.update_channels.pop(channel.id);
                    prev.update_channels.pop(channel.id);
                }
                let json = JSON.stringify(prev, null, 2);
                fs.writeFile('config.json', json, 'utf8', (err, data) => {
                    if (err) console.log(err);
                    return false;
                });
            }
        })
    }
}
