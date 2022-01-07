const { MongoClient } = require("mongodb");
const version_utils = require("../utils/version_utils.js")
const { mongoURL, mongodbName, mongoCollection, sources } = require("../config.json");

module.exports = {
    name: 'ready',
    once: true,
    async execute(client) {
        console.log(`Ready! Logged in as ${client.user.tag}`);
        const mongoClient = new MongoClient(mongoURL);
        await mongoClient.connect();
        client.dbInstance = mongoClient.db(mongodbName);
        client.tracked_apps = client.dbInstance.collection(mongoCollection);
        let updatedApps = await version_utils.updateVersions(client.tracked_apps, sources);
        console.log(updatedApps);
        if (updatedApps.length != 0) {
            for (app of updatedApps) {

            }
        }
        setInterval(async () => {
            updatedApps = await version_utils.updateVersions(client.tracked_apps, sources);
            console.log(updatedApps);
            if (updatedApps.length != 0) {
                for (app of updatedApps) {

                }
            }
        }, 10000);
        console.log(`Connected to MongoDB, using database ${mongodbName}`);
    },
};
