const Libro = require('../models/book.model');

exports.obtenerLibros = async (req, res) => {
  try {
    const libros = await Libro.find();
    res.json(libros);
  } catch (error) {
    res.status(500).json({ mensaje: 'Error al obtener los libros', error });
  }
};

exports.obtenerLibroPorId = async (req, res) => {
  try {
    const libro = await Libro.findById(req.params.id);
    if (!libro) return res.status(404).json({ mensaje: 'Libro no encontrado' });
    res.json(libro);
  } catch (error) {
    res.status(500).json({ mensaje: 'Error al obtener el libro', error });
  }
};

exports.crearLibro = async (req, res) => {
  try {
    const nuevoLibro = new Libro(req.body);
    await nuevoLibro.save();
    res.status(201).json(nuevoLibro);
  } catch (error) {
    res.status(400).json({ mensaje: 'Error al crear el libro', error });
  }
};

exports.actualizarLibro = async (req, res) => {
  try {
    const libroActualizado = await Libro.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!libroActualizado) return res.status(404).json({ mensaje: 'Libro no encontrado' });
    res.json(libroActualizado);
  } catch (error) {
    res.status(400).json({ mensaje: 'Error al actualizar el libro', error });
  }
};

exports.eliminarLibro = async (req, res) => {
  try {
    const libroEliminado = await Libro.findByIdAndDelete(req.params.id);
    if (!libroEliminado) return res.status(404).json({ mensaje: 'Libro no encontrado' });
    res.json({ mensaje: 'Libro eliminado correctamente' });
  } catch (error) {
    res.status(500).json({ mensaje: 'Error al eliminar el libro', error });
  }
};
