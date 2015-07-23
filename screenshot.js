console.log("start");
userAgentMap = {
    pcChrome : "Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30",
    pcFirefox : "Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0",
    pcIe8 : "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)",
    android : "Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
    // iphone safria
    iphone : "Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3"
}

var webPage = require('webpage');
var page = webPage.create();
system = require('system');
// var url = 'http://www.dianping.com';
var url;
var outPutImg;
var userAgentType;
    

if (system.args.length < 3) {
    console.log('Usage: phantomjs screenshot.js url outPutImg userAgentType');
    phantom.exit();
} else {
    // system.args[0] 为此JS本身
    url = system.args[1];
    outPutImg = system.args[2];
    userAgentType = system.args[3];
    console.log(userAgentType);
    console.log(userAgentMap[userAgentType]);

    // page.viewportSize = { width: 1024, height: 2000 };
    // page.clipRect = { top: 0, left: 0, width: 1024, height: 2000 };
    page.settings = {
      javascriptEnabled: true,
      loadImages: true,
      userAgent: userAgentMap[userAgentType]
    };

    page.open(url, function (status) 
    {
        if (status != "success") 
        {
            console.log('FAIL to load the address');
            phantom.exit();
        }
        
        page.evaluate(function()
        {
            // 此函数在目标页面执行的，上下文环境非本phantomjs，所以不能用到这个js中其他变量
            window.scrollTo(0,10000);//滚动到底部
            // window.document.body.scrollTop = document.body.scrollHeight;

            window.setTimeout(function()
            {
                var plist = document.querySelectorAll("a");
                var len = plist.length;
                while(len)
                {
                    len--;
                    var el = plist[len];
                    el.style.border = "1px solid red";
                }
            },5000);
        });
        
        window.setTimeout(function () 
        {
            page.render(outPutImg);
            phantom.exit();
        }, 5000+500);
    });
}