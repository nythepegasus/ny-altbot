const Discord = require('discord.js');
const { MongoClient } = require("mongodb");
const version_utils = require("../utils/version_utils.js");
const { guildId, mongoURL, mongodbName, mongoCollection, sources, update_channels } = require("../config.json");
const commandIds = require("../commands.json");

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        console.log(`Ready! Logged in as ${client.user.tag}`);
        const guild = await client.guilds.cache.get(guildId);

        client.modRole = await guild.roles.cache.find(r => r.name == "Mods");
        client.helperRole = await guild.roles.cache.find(r => r.name == "Helpers");
        client.unverifiedRole = await guild.roles.cache.find(r => r.name == "Unverified");
        
        for (com of commandIds) {
            const command = await guild?.commands.fetch(com.id);
            const c = client.commands.get(com.name);
            let permissions = [];
            if (c?.unverified) permissions.push({id: client.unverifiedRole.id, type: "ROLE", permission: true});
            if (c?.needsHelper) permissions.push({id: client.helperRole.id, type: "ROLE", permission: true});
            if (c?.needsMod || c?.needsHelper) permissions.push({id: guild.ownerId, type: "USER", permission: true}, 
                                                                {id: client.modRole.id, type: "ROLE", permission: true});
            if (!c?.unverified) permissions.push({id: client.unverifiedRole.id, type: "ROLE", permission: false});
            await command.permissions.set({ permissions });
        }

        client.update_channels = update_channels;
        const mongoClient = new MongoClient(mongoURL);
        await mongoClient.connect();
        client.dbInstance = mongoClient.db(mongodbName);
        client.tracked_apps = client.dbInstance.collection(mongoCollection);
        let updatedApps = await version_utils.updateVersions(client.tracked_apps, sources);
        if (updatedApps.length != 0) {
            for (app of updatedApps) {
                let curApp = app[0];
                let oldVer = app[1];
                let updEmbed = new Discord.MessageEmbed()
                    .setColor(`#${curApp.tintColor}`)
                    .setThumbnail(curApp.iconURL)
                    .addField("Version:", `${oldVer} -> ${curApp.version}`, true)
                    .addField("What's New:", curApp.versionDescription.substring(0, 1024))
                    .setTimestamp();
                for (channel of client.update_channels) {
                    let upChannel = client.channels.cache.get(channel);
                    upChannel.send({ embeds : [updEmbed] })
                }
            }
        }
        setInterval(async () => {
            updatedApps = await version_utils.updateVersions(client.tracked_apps, sources);
            if (updatedApps.length != 0) {
                for (app of updatedApps) {
                    let curApp = app[0];
                    let oldVer = app[1];
                    let updEmbed = new Discord.MessageEmbed()
                        .setColor(`#${curApp.tintColor}`)
                        .setThumbnail(curApp.iconURL)
                        .addField("Version:", `${oldVer} -> ${curApp.version}`, true)
                        .addField("What's New:", curApp.versionDescription.substring(0, 1024))
                        .setTimestamp();
                    for (channel of client.update_channels) {
                        let upChannel = client.channels.cache.get(channel);
                        upChannel.send({ embeds : [updEmbed] })
                    }
                }
            }
        }, 60000);
        console.log(`Connected to MongoDB, using database ${mongodbName}`);
    },
};
