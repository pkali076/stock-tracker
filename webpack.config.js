const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'static/js'),
        library: {
            name: 'MyLibrary',
            type: 'var',
        },
    },
    mode: 'development',
};
