var casper = require('casper').create(); 
var fs =  require('fs');        // 引入 fs 模块，这是 PhantomJS的模块
phantom.outputEncoding="GBK";
var url = 'http://www.baidu.com';
casper.start(url, function () {   
    //this.capture("1.png");   
    this.echo("启动程序...."); 
    this.capture("1.png");   
    var t = this.getTitle();    // 获取网页标题
    this.echo(t);       // 输出到命令窗口  
});   

//输入要查询的数据   
casper.then(function () {   
    this.fill('form[id="form"]', {  
        "wd": "123" //from中标签的name  

    }, false);   
    this.capture("2.png"); 
    this.echo("等待点击查询按钮");   

});   

casper.then(function () {   
    this.click('input[id="su"]');  

    this.echo("已经点击查询按钮, 跳转等待.....");   
    this.wait(3000, function () {   
        this.echo(this.getTitle());   
        this.capture("3.png");   
        this.echo("查询成功");   
    });   
});   
casper.run(); 