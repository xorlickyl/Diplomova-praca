const {net, app, BrowserWindow } = require('electron')


function createWindow () {
    const win = new BrowserWindow({
        width: 1200,
        height: 900,
        webPreferences: {
            nodeIntegration: true
        }
    })

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

// receive message from index.html
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
        console.log(`HEADERS: ${JSON.stringify(response.headers)}`);

        response.on('data', (chunk) => {
            console.log(`BODY: ${chunk}`)
            event.sender.send("finished",chunk.toString());
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
    req.on('close', (error) => {
        console.log('Last Transaction has occured')
    });
    console.log(req);
    req.end();
});
