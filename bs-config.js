// bs-config.js
module.exports = {
  "port": 3000,
  "files": [
    "./public/**/*.{html,htm,css,js,py}"
  ],
  "server": {
    "baseDir": "./public",
    "middleware": [
      function (req, res, next) {
        res.setHeader('Access-Control-Allow-Origin', '*');
        res.setHeader('Cross-Origin-Opener-Policy', 'same-origin');
        res.setHeader('Cross-Origin-Embedder-Policy', 'require-corp');
        res.setHeader('Cross-Origin-Resource-Policy', 'cross-origin');
        next();
      }
    ]
  },
  "browser": "default",
  "reloadDelay": 1000,
  "logLevel": "info"
};

