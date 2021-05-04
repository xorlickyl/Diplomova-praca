const {net, app, BrowserWindow } = require('electron')
const request = require('request');
const {dialog} = require('electron');
const {ipcMain} = require('electron');
const fs = require('fs');

const ip='127.0.0.1:5000';

function createWindow () {
    const win = new BrowserWindow({
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
    const  req = net.request({
        method:'GET',
        protocol:'http:',
        host:ip,
        path:"/elements/"+url+"/"+prefix+"/"+arg.check
    });
    req.on('response',(response) => {
        console.log(response.statusCode)
        if(response.statusCode ===200){
            response.on('data', (chunk) => {
                var json = JSON.parse(chunk);
                console.log(json);
                event.sender.send("finished", json);

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
        path:'/scrap/'+url+'/'+prefix+'/'+arg.check
    });
    req.on('response',(response) => {
        console.log(response.statusCode)
        if(response.statusCode===200){
            response.on('data', (chunk) => {
                var json = JSON.parse(chunk);
               // console.log(json);
                event.sender.send("data",json);
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
//https://android.mpage.sk/index.php
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
        url: 'http://'+ip+'/scrap/tag'}, callback);
    function callback(error, response, body) {
        if (!error && response.statusCode == 200) {
            var json = JSON.parse(response.body);
            console.log(json);
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
     url: 'http://'+ip+'/download'}, callback);

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

