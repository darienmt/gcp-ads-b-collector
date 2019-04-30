const functions = require('firebase-functions');
const express = require('express');

const API_PREFIX = 'data';
const app = express();

// Rewrite Firebase hosting requests: /data/:path => /:path
app.use((req, res, next) => {
    if (req.url.indexOf(`/${API_PREFIX}/`) === 0) {
        req.url = req.url.substring(API_PREFIX.length + 1);
    }
    next();
});

app.get('/status.json', (req, res) => {
    res.send({
      type : 'flightfeeder'
    })
});

exports[API_PREFIX] = functions.https.onRequest(app);