
browser.webRequest.onBeforeRequest.addListener(
    function(details) {
        if (details.url.includes(".m3u8")) {
            browser.runtime.sendNativeMessage("sniffer_port", { type: "m3u8", url: details.url });
        }
    },
    {urls: ["<all_urls>"]}
);

browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === "epg_data") {
        browser.runtime.sendNativeMessage("sniffer_port", { type: "epg", data: message.data });
    }
});
