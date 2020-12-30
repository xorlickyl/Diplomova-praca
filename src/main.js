const { app, BrowserWindow } = require('electron')


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
    var python = require('child_process').spawn('pyhton', ['./text_from_url.py',arg]);
    python.stdout.on('data',(data)=>{
        console.log("data: ",data);
    });
   // event.sender.send('finish',arg);
    // send message to index.html
   // event.sender.send('asynchronous-reply', arg);
});
