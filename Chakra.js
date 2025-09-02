//For RT. 

const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const path = require('path');
const { exec } = require('child_process');

const sessionFolder = path.resolve(__dirname, 'custom-session-folder');

const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: sessionFolder
  }),
  puppeteer: {
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  }
});

client.on('qr', (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('Client is ready!');
    exec('python3 /wwebjs-bot/core.py', (error, stdout, stderr) => {
        client.sendMessage('91953XXXXX9@c.us', stdout.trim());
        client.sendMessage('919999999999@c.us', stdout.trim());
    });
});

client.on('message_create', async message => {
  if (message.body.startsWith('/self')) {
    client.sendMessage('91953XXXXX99@c.us', "Jai Shree Ram, Test");
  }

  if (message.body.startsWith('/vedic')) {
    exec('python3 core.py', (error, stdout, stderr) => {
      if (error) {
        console.error(`exec error: ${error}`);
        client.sendMessage(message.from, 'Error executing script.');
        client.sendMessage(message.from, `exec error: ${error}`)
        return;
      }

      if (stderr && !stderr.includes('RequestsDependencyWarning')) {
        console.error(`stderr: ${stderr}`);
        client.sendMessage(message.from, 'Error in script execution.');
        return;
      }

      if (stdout.trim()) {
        client.sendMessage(message.from, stdout.trim());
      } else {
        client.sendMessage(message.from, 'No output from the script.');
      }
    });
  }
});

client.initialize();
//Without You, i dont need even heavens. I accept this hell. For you!
