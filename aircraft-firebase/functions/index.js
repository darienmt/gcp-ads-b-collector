'use strict';

const functions = require('firebase-functions');
const admin = require('firebase-admin');
admin.initializeApp();
const config = functions.config();

const express = require('express');
const cookieParser = require('cookie-parser')();
const cors = require('cors')({origin: true});
const app = express();

// Express middleware that validates Firebase ID Tokens passed in the Authorization HTTP header.
// The Firebase ID token needs to be passed as a Bearer token in the Authorization HTTP header like this:
// `Authorization: Bearer <Firebase ID Token>`.
// when decoded successfully, the ID Token content will be added as `req.user`.
const validateFirebaseIdToken = async (req, res, next) => {
  console.log('Check if request is authorized with Firebase ID token');

  if ((!req.headers.authorization || !req.headers.authorization.startsWith('Bearer ')) &&
      !(req.cookies && req.cookies.__session)) {
    console.error('No Firebase ID token was passed as a Bearer token in the Authorization header.',
        'Make sure you authorize your request by providing the following HTTP header:',
        'Authorization: Bearer <Firebase ID Token>',
        'or by passing a "__session" cookie.');
    res.status(403).send('Unauthorized');
    return;
  }

  let idToken;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer ')) {
    console.log('Found "Authorization" header');
    // Read the ID Token from the Authorization header.
    idToken = req.headers.authorization.split('Bearer ')[1];
  } else if(req.cookies) {
    console.log('Found "__session" cookie');
    // Read the ID Token from cookie.
    idToken = req.cookies.__session;
  } else {
    // No cookie
    res.status(403).send('Unauthorized');
    return;
  }

  try {
    const decodedIdToken = await admin.auth().verifyIdToken(idToken);
    req.user = decodedIdToken;
    next();
    return;
  } catch (error) {
    console.error('Error while verifying Firebase ID token:', error);
    res.status(403).send('Unauthorized');
    return;
  }
};

app.use(cors);

app.use(cookieParser);
app.use(validateFirebaseIdToken);
app.get('/data/status.json', (req, res) => {
  res.send({ type : 'flightfeeder'})
});

app.get('/data/upintheair.json', (req, res) => {
  res.send({
    rings: []
  })
});

app.get('/data/receiver.json', (req, res) => {
  res.send(
    { 
      "version" : config.receiver.version, 
      "refresh" : parseInt(config.receiver.refresh), 
      "history" : parseInt(config.receiver.history), 
      "lat" : parseFloat(config.receiver.lat), 
      "lon" : parseFloat(config.receiver.lon) 
    }
  )
});


app.get('/data/history_:number.json', (req, res) => {
  res.send({
    now : new Date() / 1000,
    aircraft : []
  })
});


app.get('/data/aircraft.json', (req, res) => {
  let now = new Date() / 1000;
  console.log( 'Now : ' + now)
  res.send({
    now : now,
    aircraft : []
  })
});

// This HTTPS endpoint can only be accessed by your Firebase Users.
// Requests need to be authorized by providing an `Authorization` HTTP header
// with value `Bearer <Firebase ID Token>`.
exports.aircraftBasic = functions.https.onRequest(app);