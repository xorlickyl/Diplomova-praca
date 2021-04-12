const {net, app, BrowserWindow } = require('electron')


function createWindow () {
    const win = new BrowserWindow({
        width: 1200,
        height: 900,
        show:false,
        webPreferences: {
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

const {ipcMain} = require('electron')

// receive message from index.html html-tree
ipcMain.on('url',function (event, arg) {
    console.log( arg );
    var url = arg.substring(8);
    url=url.replace("/","-");

    console.log(url);
    const  req = net.request({
        method:'GET',
        protocol:'http:',
        host:'127.0.0.1:5000',
        path:'/elements/'+url
    });
    req.on('response',(response) => {
        console.log(response.statusCode)

        response.on('data', (chunk) => {
            var json = JSON.parse(chunk);
           // console.log(json);
            event.sender.send("finished",json);
        });
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
    console.log( arg );
    var url = arg.substring(8);
    url=url.replace("/","-");

    console.log(url);
    const  req = net.request({
        method:'GET',
        protocol:'http:',
        host:'127.0.0.1:5000',
        path:'/scrap/'+url
    });
    req.on('response',(response) => {
        console.log(response.statusCode)

        response.on('data', (chunk) => {
            var json = JSON.parse(chunk);
            console.log(json.length);
            event.sender.send("data",json);
        });
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

//recieve message from scrap.html download
ipcMain.on('download',function (event, arg) {

    const  req = net.request({
        method:'POST',
        protocol:'http:',
        host:'127.0.0.1:5000',
        path:'/download',
        headers:{
            'Content-Type': 'application/json'
        },
        body: arg
    });
    req.write(arg);
    req.on('response',(response) => {
        console.log(response.statusCode)

        response.on('csv', (chunk) => {
           // var json = JSON.parse(chunk);
           // console.log(json.length);
            event.sender.send("data",chunk);
        });
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
