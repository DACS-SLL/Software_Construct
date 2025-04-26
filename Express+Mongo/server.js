require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const passport = require('passport');
const session = require('express-session');
//const authRoutes = require('./src/routes/authRoutes');
const bookRoutes = require('./src/routes/book.routes');
//const authorRoutes = require('./src/routes/authorRoutes');
//const errorHandler = require('./src/middlewares/errorHandler');
//const connectDB = require('./src/config/db');
//const oauthConfig = require('./src/config/oauth');
const dotenv = require('dotenv');

const app = express();
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Servidor corriendo en el puerto ${PORT}`));

dotenv.config();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static('public'));
app.set('view engine', 'ejs');


// Rutas
app.use('/api/libros', require('./src/routes/book.routes'));


// Session configuration
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: { secure: process.env.NODE_ENV === 'production' }
}));

// Passport initialization
app.use(passport.initialize());
app.use(passport.session());
//oauthConfig(passport);

// Conexión a MongoDB
mongoose.connect(process.env.MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log('Conectado a MongoDB'))
  .catch(err => console.error('Error al conectar a MongoDB:', err));

// Database connection
//connectDB();

// Routes
//app.use('/auth', authRoutes);
app.use('/api/books', bookRoutes);
//app.use('/api/authors', authorRoutes);

// Frontend route
app.get('/', (req, res) => {
  res.render('dashboard', { user: req.user });
});

// Error handler
//app.use(errorHandler);


// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});