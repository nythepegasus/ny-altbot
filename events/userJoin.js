module.exports = {
    name: "guildMemberAdd",
    async execute(member) {
        let guild = member.guild;
        let role = guild.roles.cache.find(role => role.name === "Unverified");
        member.roles.add(role);
    }
}
