const { MessageEmbed } = require("discord.js");
const { SlashCommandBuilder } = require("@discordjs/builders");
const all_roles = require("../utils/all-roles");

module.exports = {
    needsMod: true,
    data: new SlashCommandBuilder()
        .setName("sendreactmsgs")
        .setDescription("Sends the react messages for reaction roles."),
    async execute(interaction) {
       await interaction.deferReply({ ephemeral: true });
        const macEmbed = new MessageEmbed()
            .setTitle("Do you use macOS?")
            .addField("Platform", all_roles.macPre_roles.map(r => `${r.emoji} ${r.name}`).join("\n"))
            .addField("Version", all_roles.macOS_roles.map(r => `${r.emoji} ${r.name}`).join("\n"))
            .addField("Beta", all_roles.macPost_roles.map(r => `${r.emoji} ${r.name}`).join("\n"));
        const winEmbed = new MessageEmbed()
            .setTitle("Do you use Windows?")
            .addField("Version", all_roles.win_roles.map(r => `${r.emoji} ${r.name}`).join("\n"));
        const modEmbed = new MessageEmbed()
            .setTitle("Which iPhone do you have?")
            .addField("Model", all_roles.model_roles.map(r => `${r.emoji} ${r.name}`).join("\n"));
        const iOSEmbed = new MessageEmbed()
            .setTitle("Which iOS do you have?")
            .addField("Jailbroken", all_roles.model_pre_roles.map(r => `${r.emoji} ${r.name}`).join("\n"))
            .addField("Version", all_roles.iOS_roles.map(r => `${r.emoji} ${r.name}`).join("\n"))
            .addField("Beta", all_roles.iOS_post_roles.map(r => `${r.emoji} ${r.name}`).join("\n"));
        const etcEmbed = new MessageEmbed()
            .setTitle("Etc Roles")
            .addField("Roles", all_roles.etc_roles.map(r => `${r.emoji} ${r.name}`).join("\n"));
        
        const macMsg = await interaction.channel.send({embeds: [macEmbed]});
        const winMsg = await interaction.channel.send({embeds: [winEmbed]});
        const modMsg = await interaction.channel.send({embeds: [modEmbed]});
        const iOSmsg = await interaction.channel.send({embeds: [iOSEmbed]});
        const etcmsg = await interaction.channel.send({embeds: [etcEmbed]});

        for (const emoji of all_roles.macPre_roles.concat(all_roles.macOS_roles, all_roles.macPost_roles).map(r => `${r.emoji}`)) {
            await macMsg.react(emoji);
        }
        for (const emoji of all_roles.win_roles.map(r => `${r.emoji}`)) {
            await winMsg.react(emoji);
        }
        for (const emoji of all_roles.model_roles.map(r => `${r.emoji}`)) {
            await modMsg.react(emoji);
        }
        for (const emoji of all_roles.model_pre_roles.concat(all_roles.iOS_roles, all_roles.iOS_post_roles).map(r => `${r.emoji}`)) {
            await iOSmsg.react(emoji);
        }
        for (const emoji of all_roles.etc_roles.map(r => `${r.emoji}`)) {
            await etcmsg.react(emoji);
        }
        await interaction.editReply({ content: "Sent messages!" });
    }
}