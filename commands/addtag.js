const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    needsMod: true,
    data: new SlashCommandBuilder()
        .setName("addtag")
        .setDescription("Add a new help tag.")
        .setDefaultPermission(false)
        .addStringOption(option =>
            option.setName("name")
            .setDescription("The name of the tag")
            .setRequired(true))
        .addStringOption(option =>
            option.setName("description")
            .setDescription("The description of the tag.")
            .setRequired(true)),
    async execute(interaction) {
        await interaction.deferReply({ephemeral: true});
        const client = interaction.client;
        const tagName = interaction.options.getString("name");
        const tagDesc = interaction.options.getString("description");
        console.log(`${tagName}:\n${tagDesc}`);
        const items = await client.dbInstance.collection("tags").findOne({ name: tagName });
        console.log(items);
        if (items != null) return await interaction.editReply(`Tag ${tagName} already exists!`);
        client.dbInstance.collection("tags").insertOne({name: tagName, description: tagDesc}, (err, res) => {
            if (err) throw err;
        });
        await interaction.editReply(`Tag ${tagName} has been successfully registered!`);
    }
}