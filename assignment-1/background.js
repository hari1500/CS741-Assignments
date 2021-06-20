chrome.runtime.onInstalled.addListener(function() {
   console.log("Installed");
});

function check(val) {
    // console.log("checking ",val);
    val = val.replace(/\s+/g , "");
    val = val.replace(/\+/g , "");
    val = val.replace(/\\/g , "");
    return (
        val.match(/<script>/gi) || val.match(/<script/gi) || val.match(/%3Cscript/gi) ||
        val.match(/<scripttype="text\/javascript"/gi) || val.match(/javascript:/gi) || val.match(/on.*=/gi)
    );
}

chrome.webRequest.onBeforeRequest.addListener(
    function(details){
        var blockOrNot = false;
        // console.log(details);
        // console.log(details.url);
        
        if(details.method=='GET'){
            var url = details.url;
            var params = (new URLSearchParams(url)).values();

            for (let p of params) {
                if (p!='' && typeof(p) != "undefined" && check(p)){
                    blockOrNot = true;
                    console.log("script detected in "+p);
                    break;
                }
            }
        }
        if(details.method=='POST'){
            // var params = details.requestBody.formData.data.values();
            var p = JSON.stringify(details.requestBody.formData);
            if (p!= '' &&  typeof(p) != "undefined"  && check(p)){
                blockOrNot = true;
                console.log("script detected in "+p);
            }
        }

        return {cancel:blockOrNot};
    },
    // {urls: ["*://www.cse.iitb.ac.in/~surajyadav/*"]}, // TODO: replace with "<all_urls>" after testing
    {urls: ["<all_urls>"]}, // TODO: replace with "<all_urls>" after testing
    ["blocking", "requestBody"]
);
