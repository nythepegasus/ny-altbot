const { SlashCommandBuilder } = require("@discordjs/builders");

module.exports = {
    needsHelper: true,
    data: new SlashCommandBuilder()
        .setName("tag")
        .setDescription("Send or reply to user message with specific help tag")
        .setDefaultPermission(false)
        .addStringOption(option =>
            option.setName("name")
            .setDescription("Name of the help tag you want to use.")
            .setRequired(true))
        .addUserOption(option =>
            option.setName("target")
            .setDescription("Target user to mention (optional)"))
        .addStringOption(option =>
            option.setName("messageid")
            .setDescription("Message id to reply to (optional)")),
    async execute(interaction) {
        await interaction.deferReply({ephemeral: true});
        const client = interaction.client;
        const tagName = interaction.options.getString("name");
        const targetUser = interaction.options.getUser("target");
        const msgId = interaction.options.getString("messageid");
        const item = await client.dbInstance.collection("tags").findOne({ name: tagName });
        if (!item) return await interaction.editReply(`Tag ${tagName} doesn't exist.`);
        let ret_str = "";
        if (targetUser) ret_str += `*Advice for <@${targetUser.id}>*\n`;
        ret_str += item.description;
        if (msgId) {
            const msg = await interaction.channel.messages.fetch(msgId);
            await msg.reply(ret_str);
        } else {
            await interaction.channel.send({content: ret_str});
        }
        await interaction.editReply({content: "Sent advice!"});
    }
}