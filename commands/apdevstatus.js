const { SlashCommandBuilder } = require("@discordjs/builders");
const webshot = require("node-webshot");
const fs = require("fs");

module.exports = {
    cooldown: 5 * 60 * 1000,
    data: new SlashCommandBuilder()
    .setName("apdevstatus")
    .setDescription("Sends a screenshot of Apple Developer services statuses."),
    async execute(interaction) {
        interaction.deferReply();
        webshot("https://developer.apple.com/system-status/", "devstatus.jpeg", { screenSize: { width: 1920, height: 1080 }, shotSize: { width: 992, height: 837 }, shotOffset: { left: 462, top: 96 } }, function () {
            interaction.editReply({ files: ["devstatus.jpeg"] });
            setTimeout(() => {
                try {
                    fs.unlinkSync("devstatus.jpeg");
                } catch (error) {
                    console.log(error);
                }
            }, 5000);
        });
    },
};
