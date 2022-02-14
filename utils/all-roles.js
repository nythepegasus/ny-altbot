module.exports.macPre_roles = [
    {
        name: "Intel",
        color: "1795fc",
        emoji: "🇮"
    },
    {
        name: "Apple Silicon",
        color: "1795fc",
        emoji: "🇦"
    }
];
module.exports.macOS_roles = [
    {
        name: "<= macOS 10.15",
        color: "1795fc",
        emoji: "1️⃣"
    },
    {
        name: "macOS 11",
        color: "1795fc",
        emoji: "2️⃣"
    },
    {
        name: "macOS 12",
        color: "1795fc", 
        emoji: "3️⃣"
    }
];
module.exports.macPost_roles = [
    {
        name: "Beta",
        color: "1795fc",
        emoji: "🛠"
    }
];

module.exports.win_roles = [
    {
        name: "<= Windows 8",
        color: "255fff",
        emoji: "1️⃣"
    },
    {
        name: "Windows 10",
        color: "255fff",
        emoji: "2️⃣"
    },
    {
        name: "Windows 11",
        color: "255fff",
        emoji: "3️⃣"
    }
];

module.exports.com_roles = module.exports.macOS_roles.concat(module.exports.macPost_roles, module.exports.win_roles);

module.exports.model_pre_roles = [
    {
        name: "Jailbroken",
        color: null,
        emoji: "⚙️"
    }
];
module.exports.model_roles = [
    {
        name: "iPhone 5s",
        color: null,
        emoji: "1️⃣"
    },
    {
        name: "iPhone 6/Plus",
        color: null,
        emoji: "2️⃣"
    },
    {
        name: "iPhone 7/Plus",
        color: null,
        emoji: "3️⃣"
    },
    {
        name: "iPhone X/8/Plus",
        color: null,
        emoji: "4️⃣"
    },
    {
        name: "iPhone SE (1st)",
        color: null,
        emoji: "5️⃣"
    },
    {
        name: "iPhone XR/XS/Max",
        color: null,
        emoji: "6️⃣"
    },
    {
        name: "iPhone 11",
        color: null,
        emoji: "7️⃣"
    },
    {
        name: "iPhone SE (2nd)",
        color: null,
        emoji: "8️⃣"
    },
    {
        name: "iPhone 12",
        color: null,
        emoji: "9️⃣"
    },
    {
        name: "iPhone 13",
        color: null,
        emoji: "🔟"
    }
];
module.exports.iOS_roles = [
    {
        name: "<= iOS 12",
        color: null,
        emoji: "1️⃣"
    },
    {
        name: "iOS 13.0-13.3.1",
        color: null,
        emoji: "2️⃣"
    },
    {
        name: "iOS 13.4-13.7",
        color: null,
        emoji: "3️⃣"
    },
    {
        name: "iOS 14.0-14.3",
        color: null,
        emoji: "4️⃣"
    },
    {
        name: "iOS 14.4-14.8.1",
        color: null,
        emoji: "5️⃣"
    },
    {
        name: "iOS 15",
        color: null,
        emoji: "6️⃣"
    },
];
module.exports.iOS_post_roles = [
    {
        name: "beta",
        color: null,
        emoji: "🛠"
    }
];

module.exports.etc_roles = [
    {
        name: "Casual User",
        color: "3b7e6d",
        emoji: "🦾"
    },
    {
        name: "iOS Beginner",
        color: "0a528a",
        emoji: "🆕"
    },
    {
        name: "iOS Veteran",
        color: "0a528a",
        emoji: "🧑‍💻"
    },
    {
        name: "iPadOS",
        color: "fad3cc",
        emoji: "📱"
    },
    {
        name: "tvOS",
        color: "444b4e",
        emoji: "📺"
    },
];

module.exports.all_roles = module.exports.macPre_roles.concat(module.exports.com_roles, module.exports.model_pre_roles, module.exports.model_roles,
                                                              module.exports.iOS_roles, module.exports.iOS_post_roles, module.exports.etc_roles);
