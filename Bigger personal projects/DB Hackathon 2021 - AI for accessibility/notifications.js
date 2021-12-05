// Recent purchase recorded toast notification
function loggedPurchaseToast(item, price, category, remaining) {
    const poundSymbol = "\u{A3}"
    const shoppingSymbol = "\u{1F6D2}"
    var toastOpt = {
        type: "basic",
        title: `${shoppingSymbol}Recent purchase recorded`,
        message: `The purchase of '${item}' you just made cost you ${poundSymbol}${price} out of your ${category} pot.\nYou now have ${poundSymbol}${remaining} remaining in this pot.`,
        iconUrl: "imgs/purchaseNotification.png",
        priority: 2,
        buttons: [{
            title: "Show me my dashboard."
        }]
    }
    chrome.notifications.create("loggedPurchase", toastOpt, function (id) { })
}

// potentially impulsive - requireInteraction, NotificationButton[]
function impulsiveToast() {
    const poundSymbol = "\u{A3}"
    const warningSymbol = "\u{26A0}"
    var toastOpt = {
        type: "basic",
        title: `${warningSymbol}This is a potentially impulsive purchase`,
        message: "Our systems have detected that this item you are viewing matches those often bought impulsively.",
        iconUrl: "imgs/purchaseNotification.png",
        priority: 2,
        buttons: [{
            title: "Take me back!"
        }]
    }
    chrome.notifications.create("potentiallyImpulsivePurchase", toastOpt, function (id) { })
}

// avoided a purchase - chrome.history?

// page overlay/alert (use window.confirm()?)

// register click/button events
chrome.notifications.onButtonClicked.addListener(function (notifId, btnIdx) {
    if (notifId === "loggedPurchase") {
        if (btnIdx === 0) {
            chrome.tabs.create({ 'url': 'chrome://extensions/?options=' + chrome.runtime.id });
        }
    } else if (notifId === "potentiallyImpulsivePurchase") {
        if (btnIdx === 0) {
            chrome.tabs.executeScript(null, { "code": "window.history.back()" });
        }
    }
});