const mongoose = require('mongoose');

const BookSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Author',
    required: true
  },
  isbn: {
    type: String,
    required: true,
    unique: true
  },
  publishedDate: {
    type: Date,
    required: true
  },
  pageCount: {
    type: Number,
    min: 1
  },
  genre: {
    type: [String],
    required: true
  },
  publisher: String,
  language: {
    type: String,
    default: 'English'
  },
  description: String,
  coverImage: String,
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: {
    type: Date,
    default: Date.now
  },
  createdBy: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }
});

module.exports = mongoose.model('Book', BookSchema);