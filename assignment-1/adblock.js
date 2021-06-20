function checkForAd(val) {
    //  console.log("checking url",val);
     return (
        val.match(/pagead.*/gi) || val.match(/googlead*=/gi)
     );
 }
 
 chrome.webRequest.onBeforeRequest.addListener(
     function(details){
        var blockOrNot = false;
        // console.log(details.url);
        var url = details.url;
        if(checkForAd(url)){
            blockOrNot = true;
            console.log("ad detected in "+url);
        }
        return {cancel:blockOrNot};
     },
    {urls: ["<all_urls>"]},
     ["blocking"]
 );
 