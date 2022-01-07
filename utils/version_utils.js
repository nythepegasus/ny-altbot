const semverCoerce = require('semver/functions/coerce')
const semverLt = require('semver/functions/lt')
const fetch = require("node-fetch");

module.exports = {
    compareVersions : function (current_version, newer_version) {
        // Compare current_version and newer_version, true if current_version is lower and false if newer_version is lower
        let semcurrent_version = semverCoerce(current_version);
        let semnewer_version = semverCoerce(newer_version);
        if (semcurrent_version == semnewer_version) {
            if (current_version.includes("a") && newer_version.includes("b")) {
                return true
            } else if (current_version.includes("b") && !newer_version.includes("b")) {
                return true
            } else {
                return false
            }
        }
        return semverLt(semcurrent_version, semnewer_version);
    },
    getVersions : async function (url) {
        return await fetch(url, {method:"Get"})
            .then(res => res.json())
    },
    updateVersions : async function (collection, sources) {
        console.log("Running updateVersions..");
        let updatedApps = [];
        for (url of sources) {
            
            let res = await this.getVersions(url);

            for (app of res.apps) {
                let bundleIdentifier = app.bundleIdentifier;
                let newVersion = app.version;
                let curVersion = await collection.findOne({app: bundleIdentifier});
                if (!this.compareVersions(curVersion?.version ?? "0.0.0", newVersion)) continue;
                let insertResult = await collection.findOneAndUpdate({app: bundleIdentifier}, {$set: {version: newVersion}}, {upsert: true});
                if (newVersion != insertResult.value?.version) {
                    updatedApps.push([app, curVersion]);
                }
            }
        }
        return updatedApps;
    }
}