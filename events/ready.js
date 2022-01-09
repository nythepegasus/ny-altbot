const Discord = require('discord.js');
const { MongoClient } = require("mongodb");
const version_utils = require("../utils/version_utils.js")
const { mongoURL, mongodbName, mongoCollection, sources, update_channels } = require("../config.json");

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        console.log(`Ready! Logged in as ${client.user.tag}`);
        client.update_channels = update_channels;
        const mongoClient = new MongoClient(mongoURL);
        await mongoClient.connect();
        client.dbInstance = mongoClient.db(mongodbName);
        client.tracked_apps = client.dbInstance.collection(mongoCollection);
        let updatedApps = await version_utils.updateVersions(client.tracked_apps, sources);
        console.log(updatedApps);
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
            console.log(updatedApps);
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
