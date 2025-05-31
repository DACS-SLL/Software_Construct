import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  }
})

export default {
  // Ofertas
  getOfertas(skip = 0, limit = 100) {
    return api.get(`/ofertas-laborales?skip=${skip}&limit=${limit}`)
  },
  createOferta(data) {
    return api.post('/ofertas-laborales', data)
  },
  updateOferta(id, data) {
    return api.put(`/ofertas-laborales/${id}`, data)
  },
  deleteOferta(id) {
    return api.delete(`/ofertas-laborales/${id}`)
  },

  // Empresas
  getEmpresas(skip = 0, limit = 100) {
    return api.get(`/empresas?skip=${skip}&limit=${limit}`)
  },
  createEmpresa(data) {
    return api.post('/empresas', data)
  },
  updateEmpresa(id, data) {
    return api.put(`/empresas/${id}`, data)
  },
  deleteEmpresa(id) {
    return api.delete(`/empresas/${id}`)
  },

  // Postulantes
  getPostulantes(skip = 0, limit = 100) {
    return api.get(`/postulantes?skip=${skip}&limit=${limit}`)
  },
  createPostulante(data) {
    return api.post('/postulantes', data)
  },
  updatePostulante(id, data) {
    return api.put(`/postulantes/${id}`, data)
  },
  deletePostulante(id) {
    return api.delete(`/postulantes/${id}`)
  },

  // Categorías
  getCategorias() {
    return api.get('/categorias')
  }
}