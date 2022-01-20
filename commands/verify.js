const svgCaptcha = require("svg-captcha");
const sharp = require("sharp");
const { SlashCommandBuilder } = require("@discordjs/builders");

svgCaptcha.options.height = 100
svgCaptcha.options.width = 300

module.exports = {
    unverified: true,
    data: new SlashCommandBuilder()
    .setName("verify")
    .setDescription("Verify yourself with a captcha to gain access to the server.")
    .setDefaultPermission(false),
    async execute(interaction) {
        const member = interaction.member;
        const unverifiedRole = interaction.guild.roles.cache.find(role => role.name === "Unverified");
        await interaction.deferReply({ ephemeral : true });
        let svgImg = svgCaptcha.create({ size: 8, noise: 2, ignoreChars: "O0o1iIlL", color: true, background: "#ffffff" });
        let pngImg = await sharp(Buffer.from(svgImg.data)).png().toBuffer();
        await interaction.editReply({ content : "Verifying you!", files : [pngImg] });
        const filter = m => m.content.includes(svgImg.text);
        const collector = interaction.channel.createMessageCollector({ filter, time: 30000 });

        collector.on('collect', m => {
            m.delete();
            member.roles.remove(unverifiedRole);
            interaction.followUp({ content: "Verified!", ephemeral : true });
            return;
        });

        collector.on('end', collected => {
            console.log(`Collected ${collected.size} items`);
        });
    }
}