const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const root = path.join(__dirname, '..');
let result;
const choices = process.platform === 'win32' ? [['py',['-3']],['python',[]]] : [['python3',[]],['python',[]]];
let success = false;
for (const [command, args] of choices) {
  result=spawnSync(command,[...args,path.join(root,'frontend','src','assemble_app.py')],{cwd:root,stdio:'inherit',shell:false});
  if(result.status === 0) { success=true; break; }
}
if(!success) { console.error('Python 3 is required to rebuild UES frontend'); process.exit(1); }
fs.mkdirSync(path.join(root,'frontend','dist','assets'),{recursive:true});
const tailwindBin=require.resolve('tailwindcss/lib/cli.js');
result=spawnSync(process.execPath,[tailwindBin,'-c','tailwind.config.cjs','-i','./frontend/src/style.css','-o','./frontend/dist/assets/ues.css','--minify'],{cwd:root,stdio:'inherit',shell:false});
if(result.status !== 0) process.exit(result.status || 1);
console.log('UES local front-end built successfully.');
