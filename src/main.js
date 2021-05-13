const {net, app, BrowserWindow } = require('electron')
const request = require('request');
const {dialog} = require('electron');
const {ipcMain} = require('electron');
const fs = require('fs');
let win=null
//const ip='127.0.0.1:5000';
const ip='147.175.106.115:7799';

function createWindow () {
    win = new BrowserWindow({
        width: 1200,
        height: 900,
        show:false,
        webPreferences: {
            enableRemoteModule: true,
            nodeIntegration: true
        }
    })
    win.show();
    win.loadFile('index.html')
}

app.whenReady().then(createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
    }
})

console.log('Server-side code running');

// receive message from index.html html-tree
ipcMain.on('url',function (event, arg) {
    var url;
    if(arg.url.substring(4,5)=="s") {
        var prefix = arg.url.substring(0,5);
        url = arg.url.substring(8);
        url = url.replaceAll("/", "X");
        url = url.replaceAll("?", "YZ");
        url = url.replaceAll("#","KO");
    }else{
        var prefix = arg.url.substring(0,4);
        url = arg.url.substring(7);
        url = url.replaceAll("/", "X");
        url = url.replaceAll("?", "YZ");
        url = url.replaceAll("#","KO");
    }
    if(url.endsWith("/")){
        url.replace("/","");
    }

    request({
        body: arg,
        followAllRedirects: true,
        headers: {'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'},
        method: 'GET',
        json: true,
        url: 'http://'+ip+'/api/elements/'+url+'/'+prefix+'/'+arg.check}, callback);
    function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
                let data = body.toString().replaceAll("'", '"');
                const json = JSON.parse(data);
                //console.log(json);
                event.sender.send("finished", json);
            }else{
                let json = {Error : "Something is wrong"};
                event.sender.send("finished", json);
            }
        }
});

//recieve message from index.html scraping
ipcMain.on('scrap',function (event, arg) {
    if(arg.url.substring(4,5)=="s") {
        var prefix = arg.url.substring(0,5);
        var url = arg.url.substring(8);
        url = url.replaceAll("/", "X");
        url = url.replaceAll("?", "YZ");
        url = url.replaceAll("#","KO");
    }else{
        var prefix = arg.url.substring(0,4);
        var url = arg.url.substring(7);
        url = url.replaceAll("/", "X");
        url = url.replaceAll("?", "YZ");
        url = url.replaceAll("#","KO");
    }

    console.log(url);
    const  req = net.request({
        method:'GET',
        protocol:'http:',
        host:ip,
        path:'/api/scrap/'+url+'/'+prefix+'/'+arg.check
    });
    req.on('response',(response) => {
        console.log(response.statusCode)
        if(response.statusCode===200){
            response.on('data', (chunk) => {
                var data = JSON.stringify(chunk);
                var json = JSON.parse(data);
                //console.log(json);
                event.sender.send("finished",json);
            });
        }else{
            let json = {Error : "Something is wrong"};
            event.sender.send("finished", json);
        }
    });
    req.on('finish', () => {
        console.log('Request is Finished')
    });
    req.on('abort', () => {
        console.log('Request is Aborted')
    });
    req.on('error', (error) => {
        console.log(`ERROR: ${JSON.stringify(error)}`)
    });
    req.end();
});

//recieve message from index.html scraping via tag
ipcMain.on('scrap_tag',function (event, arg) {
    console.log(arg);
    request({
        body: arg,
        followAllRedirects: true,
        headers: {'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'},
        method: 'POST',
        json: true,
        url: 'http://'+ip+'/api/scrap/tag'}, callback);
    function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
            var json = JSON.parse(response.body);
            win.loadURL('./scrap.html');
            win.webContents.on('did-finish-load', ()=>{
                win.webContents.send('data',json);
            })
        }
    }
});

//recieve message from scrap.html download
ipcMain.on('download',function (event, arg) {
//send json for download data
 request({
     body: arg,
     followAllRedirects: true,
     headers: {'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'},
     method: 'POST',
     json: true,
     url: 'http://'+ip+'/api/download'}, callback);

    function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
            dialog.showSaveDialog({
                title: 'Select the File Path to save',
                buttonLabel: 'Save',
                filters: [
                    {
                        name: 'CSV Files',
                        extensions: ['csv']
                    }, ],
                properties: []
            }).then(body => {
                if (!body.canceled) {
                    fs.writeFile(body.filePath.toString(), response.body, function (err) {
                        if (err) throw err;
                        console.log('Saved!');
                    })
                }
            }).catch(err => {
                console.log(err)
            });

        } else {
            console.log("Error: \n"+body);
        }
    };
});

/*
//test table
ipcMain.on('scrap_tag',function (event, arg) {
     var json =require('./localJson.json');
    //var json = JSON.parse(response.body);
    //console.log(json);
    //event.sender.send("data", json);
    //event.reply('data', "json");
    win.loadURL('./scrap.html');
    win.webContents.on('did-finish-load', ()=>{
        win.webContents.send('data',json);
    })
});
/*
//test list
ipcMain.on('url',function (event, arg) {
    var json = require('./localJsonTree.json');
    //var json = JSON.parse(chunk);
   // console.log(json);
    event.sender.send("finished", json);
});
*/