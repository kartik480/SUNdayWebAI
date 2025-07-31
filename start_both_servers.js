const { spawn } = require('child_process');
const path = require('path');

console.log('🚀 Starting SUNDAY-PAAI - Both Frontend and Backend...');
console.log('==================================================');

// Start Flask backend
console.log('🤖 Starting Flask Backend...');
const flaskProcess = spawn('python', ['improved_app.py'], {
    cwd: __dirname,
    stdio: 'pipe',
    shell: true
});

flaskProcess.stdout.on('data', (data) => {
    console.log(`[Flask] ${data.toString().trim()}`);
});

flaskProcess.stderr.on('data', (data) => {
    console.log(`[Flask Error] ${data.toString().trim()}`);
});

// Wait a bit for Flask to start, then start Next.js
setTimeout(() => {
    console.log('⚛️  Starting Next.js Frontend...');
    const nextProcess = spawn('npm', ['run', 'dev'], {
        cwd: __dirname,
        stdio: 'inherit',
        shell: true
    });

    nextProcess.on('close', (code) => {
        console.log(`Next.js process exited with code ${code}`);
        flaskProcess.kill();
        process.exit(code);
    });
}, 3000);

// Handle process termination
process.on('SIGINT', () => {
    console.log('\n🛑 Shutting down both servers...');
    flaskProcess.kill();
    process.exit(0);
});

process.on('SIGTERM', () => {
    console.log('\n🛑 Shutting down both servers...');
    flaskProcess.kill();
    process.exit(0);
}); 