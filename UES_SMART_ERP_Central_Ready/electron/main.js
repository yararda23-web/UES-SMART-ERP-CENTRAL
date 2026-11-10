'use strict';
const {app, BrowserWindow, Menu, dialog, ipcMain, session} = require('electron');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');
const {pathToFileURL}=require('url');

app.setName('UES SMART ERP');
let mainWindow=null;
const FILE_CONFIG=()=>path.join(app.getPath('userData'),'server.json');
const SETUP_HTML=path.join(__dirname,'setup.html');

function allowedUrl(raw) {
  try {
    const url=new URL(String(raw).trim());
    const localhost=['127.0.0.1','localhost'].includes(url.hostname);
    if(url.protocol!=='https:' && !(localhost && url.protocol==='http:')) return null;
    if(url.username||url.password||url.search||url.hash||url.pathname!=='/') return null;
    return url.origin;
  } catch(e) {return null;}
}
function loadConfig() {
  try{return allowedUrl(JSON.parse(fs.readFileSync(FILE_CONFIG(),'utf8')).serverUrl);}catch(_){return null;}
}
function ping(url) {
  return new Promise((resolve,reject)=>{
    const mod=url.startsWith('https:')?https:http;
    const req=mod.get(url+'/api/health',{timeout:10000},res=>{
      let body='';res.setEncoding('utf8');res.on('data',x=>{body+=x;if(body.length>10240)req.destroy()});
      res.on('end',()=>{
        try {const x=JSON.parse(body);
          if(res.statusCode===200 && x.service==='UES-SMART-ERP-CENTRAL' && x.ok) resolve(x);
          else reject(new Error('العنوان لا يستضيف خادم المتحدة المركزي'));
        } catch(e) {reject(e);}
      });
    });
    req.on('error',reject);req.on('timeout',()=>req.destroy(new Error('انتهت مهلة الاتصال')));
  });
}
async function showSetup(message='') {
  if(!mainWindow || mainWindow.isDestroyed()) return;
  mainWindow.webContents.removeAllListeners('will-navigate');
  await mainWindow.loadFile(SETUP_HTML);
  mainWindow.webContents.once('did-finish-load',()=>mainWindow.webContents.send('setup:status',message));
}
async function openRemote(url) {
  if(!mainWindow || mainWindow.isDestroyed())return;
  // No arbitrary popups, navigation to other origins or native privileges.
  mainWindow.webContents.removeAllListeners('will-navigate');
  mainWindow.webContents.on('will-navigate',(event,target)=>{
    try {if(new URL(target).origin!==url)event.preventDefault();}
    catch(_){event.preventDefault();}
  });
  await mainWindow.loadURL(url);
}
function makeMenu() {
  return Menu.buildFromTemplate([
    {label:'المتحدة',submenu:[{label:'إعداد عنوان السيرفر',click:()=>showSetup('أدخل رابط السيرفر الجديد للتبديل.')},{role:'quit',label:'خروج'}]},
    {label:'عرض',submenu:[{role:'reload',label:'تحديث'},{role:'zoomIn',label:'تكبير'},{role:'zoomOut',label:'تصغير'},{role:'togglefullscreen',label:'ملء الشاشة'}]}
  ]);
}
app.whenReady().then(async ()=>{
  session.defaultSession.setPermissionRequestHandler((webContents,permission,callback)=>callback(false));
  session.defaultSession.setPermissionCheckHandler(()=>false);
  mainWindow=new BrowserWindow({width:1460,height:920,minWidth:880,minHeight:600,
    title:'UES SMART ERP — المتحدة للخدمات التعليمية',backgroundColor:'#0B1F33',
    webPreferences:{preload:path.join(__dirname,'preload.js'),nodeIntegration:false,contextIsolation:true,sandbox:true,webSecurity:true,webviewTag:false}
  });
  mainWindow.webContents.setWindowOpenHandler(()=>({action:'deny'}));
  Menu.setApplicationMenu(makeMenu());
  const configured=loadConfig();
  if(configured) {
    try{await ping(configured);await openRemote(configured);}
    catch(e){await showSetup('تعذر الاتصال بالسيرفر المحفوظ: '+e.message);}
  } else await showSetup('أدخل رابط سيرفر المتحدة HTTPS للمرة الأولى.');
}).catch(err=>dialog.showErrorBox('UES Startup Error',err.message));

// Only the LOCAL setup page may call these privileged IPC handlers.
function setupSender(event) {
  try{return new URL(event.sender.getURL()).protocol==='file:' &&
    event.sender.getURL()===pathToFileURL(SETUP_HTML).href;}
  catch(_){return false;}
}
ipcMain.handle('ues:connect',async(event,raw)=>{
  if(!setupSender(event)) throw new Error('Not authorized');
  const url=allowedUrl(raw);
  if(!url)throw new Error('استخدم رابط HTTPS صحيحًا دون مسار أو كلمة مرور');
  await ping(url);
  fs.mkdirSync(path.dirname(FILE_CONFIG()),{recursive:true});
  fs.writeFileSync(FILE_CONFIG(),JSON.stringify({serverUrl:url},null,2),{mode:0o600});
  await openRemote(url);
  return {ok:true};
});
app.on('window-all-closed',()=>{if(process.platform!=='darwin')app.quit();});
