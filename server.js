const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');
const bcrypt = require('bcrypt');
const passport = require('passport');
const flash = require('express-flash');
const session = require('express-session');
const methodOverride = require('method-override');
const initializePassport = require('./passport-config');
const UserModel = require('./models/UserModel');
const cors = require('cors');
app.use(cors());

initializePassport(
  passport,
  email => UserModel.findOne({ email: email }),
  id => UserModel.findById(id)
);

const users = [];

app.set('view-engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(flash());
app.use(session({
  secret: process.env.SESSION_SECRET || 'defaultSecret',
  resave: false,
  saveUninitialized: false
}));
initializePassport(passport);
app.use(passport.initialize());
app.use(passport.session());
app.use(methodOverride('_method'));
app.use(express.static('public'));
app.use(express.static('images'));
app.use('/public/styles', express.static(path.join(__dirname, 'public/styles'), {
  setHeaders: (res, path) => {
    if (path.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    }
  },
}));

// Assuming you have an Express route like this
app.get('/', (req, res) => {
  const name = 'John Doe'; // Replace this with the actual name you want to display
  res.render('index', { name: name }); // Pass the 'name' variable to the template
});


app.get('/login', checkNotAuthenticated, (req, res) => {
  res.render('login.ejs');
});

app.post('/login', checkNotAuthenticated, passport.authenticate('local', {
  successRedirect: '/index',
  failureRedirect: '/login',
  failureFlash: true
}));

app.get('/register', checkNotAuthenticated, (req, res) => {
  res.render('register.ejs');
});

app.post('/register', checkNotAuthenticated, async (req, res) => {
  try {
    await mongoose.connect('mongodb://localhost:27017/demo2');
    
    const userSchema = new mongoose.Schema({
      name: String,
      email: String,
      password: String
    });

    const UserModel = mongoose.model('UserModel', userSchema);

    const hashedPassword = await bcrypt.hash(req.body.password, 10);
    const entry = new UserModel({
      name: req.body.name,
      email: req.body.email,
      password: hashedPassword
    });

    await entry.save();
    const newUsers = await UserModel.find();
    console.log(newUsers);

    res.redirect('/login');
  } catch (error) {
    console.error(error);
    res.redirect('/register');
  }
});

initializePassport(
  passport,
  email => users.find(user => user.email === email),
  id => users.find(user => user.id === id)
);

/*app.delete('/logout', (req, res) => {
  req.logout(function(err) {
    if (err) {
      return res.status(500).json({ error: 'Logout failed' });
    }
    res.redirect('/register');
  });
});*/

function checkAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return next();
  }
  res.redirect('/login');
}
app.use(express.static(path.join(__dirname, 'views')));

function checkNotAuthenticated(req, res, next) {
  if (req.isAuthenticated()) {
    return res.redirect('/');
  }
  next();
}

app.listen(1400, () => {
  console.log('Server is running on port 1400');
});

