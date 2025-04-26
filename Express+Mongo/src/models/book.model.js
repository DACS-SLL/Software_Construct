const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  titulo: { type: String, required: true },
  autor: { type: String, required: true },
  genero: { type: String, required: true },
  anioPublicacion: { type: Number },
  disponible: { type: Boolean, default: true }
}, { timestamps: true });

module.exports = mongoose.model('Libro', bookSchema);
