const bcrypt = require('bcrypt');
/*const UserModel = require('./models/UserModel.js'); // Import the Mongoose User Model*/

async function initialize(passport) {
  const authenticateUser = async (email, password, done) => {
    try {
      const user = await UserModel.findOne({ email: email });
      if (!user) {
        return done(null, false, { message: 'No user with that email' });
      }

      if (await bcrypt.compare(password, user.password)) {
        return done(null, user);
      } else {
        return done(null, false, { message: 'Password incorrect' });
      }
    } catch (error) {
      return done(error);
    }
  };

  passport.use(new LocalStrategy({ usernameField: 'email' }, authenticateUser));
  passport.serializeUser((user, done) => done(null, user.id));
  passport.deserializeUser(async (id, done) => {
    const user = await UserModel.findById(id);
    return done(null, user);
  });
}

module.exports = initialize;
/*module.exports = mongoose.model('UserModel', userSchema);*/

