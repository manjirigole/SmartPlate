const LocalStrategy = require('passport-local').Strategy;
const bcrypt = require('bcrypt');
const UserModel = require('./models/UserModel');


async function initialize(passport, getUserByEmail, getUserById) {
  const authenticateUser = async (email, password, done) => {
    const user = getUserByEmail(email);
    if (user == null) {
      return done(null, false, { message: 'No user with that email' });
    }

    try {
      if (await bcrypt.compare(password, user.password)) {
        return done(null, user);
      } else {
        return done(null, false, { message: 'Password incorrect' });
      }
    } catch (e) {
      return done(e);
    }
  };

  passport.use(new LocalStrategy({ usernameField: 'email' }, authenticateUser));
  passport.serializeUser((user, done) => done(null, user.id));
  passport.deserializeUser(async (id, done) => {
    const user = getUserById(id);
    return done(null, user);
  });
}

module.exports = initialize;
// passport-config.js
/*const LocalStrategy = require('passport-local').Strategy;
const UserModel = require('./models/UserModel'); // Adjust the path accordingly


function initialize(passport) {
    passport.use(new LocalStrategy({ usernameField: 'email' }, async (email, password, done) => {
        const user = await UserModel.findOne({ email: email });
        if (user == null) {
            return done(null, false, { message: 'No user with that email' });
        }

        try {
            if (await bcrypt.compare(password, user.password)) {
                return done(null, user);
            } else {
                return done(null, false, { message: 'Password incorrect' });
            }
        } catch (err) {
            return done(err);
        }
    }));

    passport.serializeUser((user, done) => {
        done(null, user.id);
    });

    passport.deserializeUser((id, done) => {
        UserModel.findById(id, (err, user) => {
            done(err, user);
        });
    });
}

module.exports = initialize;*/

