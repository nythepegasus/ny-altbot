const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    needsMod: true,
    data: new SlashCommandBuilder()
        .setName("remtag")
        .setDescription("Removes an existing help tag.")
        .setDefaultPermission(false)
        .addStringOption(option =>
            option.setName("name")
            .setDescription("The name of the tag")
            .setRequired(true)),
    async execute(interaction) {
        await interaction.deferReply({ephemeral: true});
        const client = interaction.client;
        const tagName = interaction.options.getString("name");
        console.log(tagName);
        const items = await client.dbInstance.collection("tags").findOne({ name: tagName });
        if (items == null) return await interaction.editReply({content: `Tag ${tagName} doesn't exists!`});
        client.dbInstance.collection("tags").deleteOne({name: tagName}, (err, res) => {
            if (err) throw err; 
        });
        await interaction.editReply({content: `Tag ${tagName} has been successfully deleted!`});
    }
}