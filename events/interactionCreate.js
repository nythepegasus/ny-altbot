module.exports = {
    name: 'interactionCreate',
    async execute(interaction) {
        const client = interaction.client;
        if (!interaction.isCommand() && !interaction.isContextMenu()) return;
        const command = client.commands.get(interaction.commandName);
        if (!command) return;
        try {
            const commandCooldowns = client.cooldowns.get(interaction.commandName);
            if (commandCooldowns) {
                const now = new Date();
                const cooldown = commandCooldowns.get(interaction.user.id);
                if (!cooldown || now - cooldown > command.cooldown) {
                    commandCooldowns.set(interaction.user.id, now);
                    await command.execute(interaction);
                } else {
                    const diff = new Date(new Date(cooldown.getTime() + command.cooldown) - now).getTime() / 1000;
                    let hours = diff / 3600, minutes = (hours % 1) * 60, seconds = (minutes % 1) * 60;
                    hours = Math.floor(hours); minutes = Math.floor(minutes); seconds = Math.round(seconds);
                    let ret_str = "You're being ratelimited!\nPlease wait ";
                    ret_str += hours != 0 ? `${hours} hour(s)` : "";
                    ret_str += minutes != 0 && (minutes != 0 || seconds != 0) ? " and " : "";
                    ret_str += minutes != 0 ? `${minutes} minute(s)` : "";
                    ret_str += minutes != 0 && seconds != 0 ? " and " : "";
                    ret_str += seconds != 0 ? `${seconds} second(s)` : "";
                    await interaction.reply({ content: ret_str, ephemeral: true });
                }
            }
        } catch (error) {
            console.error(error);
            await interaction.reply({ content: "There was an error executing this command!", ephemeral: true });
        }
    },
};
