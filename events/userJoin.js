module.exports = {
    name: "guildMemberAdd",
    async execute(member, client) {
        let guild = member.guild;
        let role = guild.roles.cache.find(role => role.name === "unverified");
        member.roles.add(role);
    }
}
