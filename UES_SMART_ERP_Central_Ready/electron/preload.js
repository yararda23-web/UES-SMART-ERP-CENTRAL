'use strict';
const {contextBridge,ipcRenderer}=require('electron');
// No privileged API exposure to remote web content, including admin views.
const isSetup=window.location.protocol==='file:';
if(isSetup)contextBridge.exposeInMainWorld('UESConnection',Object.freeze({
  connect:(url)=>ipcRenderer.invoke('ues:connect',url),
  onStatus:(callback)=>ipcRenderer.on('setup:status',(_event,content)=>callback(content))
}));
