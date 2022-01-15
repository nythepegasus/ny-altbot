const svgCaptcha = require("svg-captcha");
const sharp = require("sharp");
const { SlashCommandBuilder } = require("@discordjs/builders");

svgCaptcha.options.height = 100
svgCaptcha.options.width = 300

module.exports = {
    data: new SlashCommandBuilder()
    .setName("verify")
    .setDescription("Verify yourself with a captcha to gain access to the server."),
    async execute(interaction) {
        await interaction.deferReply({ ephemeral : true });
        let svgImg = svgCaptcha.create({ size: 8, noise: 2, ignoreChars: "O0o1iIlL", color: true, background: "#ffffff" });
        let pngImg = await sharp(Buffer.from(svgImg.data)).png().toBuffer();
        await interaction.editReply({ content : "Verifying you!", files : [pngImg] });
        console.log(svgImg.text);
        const filter = m => m.content.includes(svgImg.text);
        const collector = interaction.channel.createMessageCollector({ filter, time: 30000 });

        collector.on('collect', m => {
            m.delete();
            console.log(`Collected ${m.content}`);
            interaction.followUp({ content: "Verified!", ephemeral : true });
            return;
        });

        collector.on('end', collected => {
            console.log(`Collected ${collected.size} items`);
        });
    }
}