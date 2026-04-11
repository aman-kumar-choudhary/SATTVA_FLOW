const fs = require('fs');
const path = require('path');

function replaceInFile(filePath) {
    let content = fs.readFileSync(filePath, 'utf8');
    if (content.includes('localStorage')) {
        content = content.replace(/localStorage/g, 'sessionStorage');
        fs.writeFileSync(filePath, content);
        console.log('Updated: ' + filePath);
    }
}

function walkSync(dir) {
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        if (fs.statSync(fullPath).isDirectory()) {
            walkSync(fullPath);
        } else if (fullPath.endsWith('.js') || fullPath.endsWith('.vue')) {
            replaceInFile(fullPath);
        }
    }
}

walkSync('./frontend/src');
