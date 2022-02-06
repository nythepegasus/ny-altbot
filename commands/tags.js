const { MessageEmbed } = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    data: new SlashCommandBuilder()
        .setName("tags")
        .setDescription("Get all current tags."),
    async execute(interaction) {
        await interaction.deferReply({ephemeral: true});
        const client = interaction.client;
        const items = await client.dbInstance.collection("tags").find().toArray();
        if (items == null) return await interaction.editReply("No tags exist.");
        let tagNames = items.map(i => i.name)
        const retEmbed = new MessageEmbed()
            .setColor("#8A28F7")
            .setTitle("Current Tags:")
            .setDescription(tagNames.join(", "))
            .setTimestamp()
        await interaction.editReply({embeds: [retEmbed]});
    }
}