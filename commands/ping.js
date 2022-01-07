const { SlashCommandBuilder } = require("@discordjs/builders");
const wait = require("util").promisify(setTimeout);

module.exports = {
    data: new SlashCommandBuilder()
    .setName("ping")
    .setDescription("Replies with pong!"),
    async execute(interaction) {
        await interaction.deferReply();
        await wait(2000);
        await interaction.editReply("Pong!");
    },
};
