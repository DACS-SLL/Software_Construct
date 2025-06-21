import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  }
})

// Interceptor para agregar token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default {
  // ==================== AUTENTICACIÓN ====================
  
  // Login real usando el endpoint del backend
  login(credentials) {
    return api.post('/auth/login', credentials)
  },

  // Registro real usando el endpoint del backend
  register(userData) {
    return api.post('/auth/register', userData)
  },

  // Logout
  logout() {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  },

  // Añadir token a blacklist
  addTokenToBlacklist(token) {
    return api.post('/token-blacklist/', { token })
  },

  // Obtener usuario actual
  getCurrentUser() {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  },

  // ==================== ROLES ====================
  
  getRoles() {
    return api.get('/roles')
  },

  createRol(data) {
    return api.post('/roles', data)
  },

  // ==================== USUARIOS ====================
  
  getUsuarios(skip = 0, limit = 100) {
    return api.get(`/usuarios?skip=${skip}&limit=${limit}`)
  },
  
  getUsuario(id) {
    return api.get(`/usuarios/${id}`)
  },
  
  createUsuario(userData) {
    return api.post('/usuarios', userData)
  },
  
  updateUsuario(id, data) {
    return api.put(`/usuarios/${id}`, data)
  },

  // ==================== OFERTAS ====================
  
  getOfertas(skip = 0, limit = 100) {
    return api.get(`/ofertas-laborales?skip=${skip}&limit=${limit}`)
  },
  
  getOferta(id) {
    return api.get(`/ofertas-laborales/${id}`)
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

  // ==================== EMPRESAS ====================
  
  getEmpresas(skip = 0, limit = 100) {
    return api.get(`/empresas?skip=${skip}&limit=${limit}`)
  },
  
  getEmpresa(id) {
    return api.get(`/empresas/${id}`)
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

  // ==================== POSTULANTES ====================
  
  getPostulantes(skip = 0, limit = 100) {
    return api.get(`/postulantes?skip=${skip}&limit=${limit}`)
  },
  
  getPostulante(id) {
    return api.get(`/postulantes/${id}`)
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

  // ==================== CATEGORÍAS ====================
  
  getCategorias() {
    return api.get('/categorias')
  },
  
  createCategoria(data) {
    return api.post('/categorias', data)
  },

  // ==================== POSTULACIONES ====================
  
  getPostulaciones(params = {}) {
    const queryParams = new URLSearchParams(params).toString()
    return api.get(`/postulaciones?${queryParams}`)
  },
  
  createPostulacion(data) {
    return api.post('/postulaciones', data)
  },
  
  updatePostulacion(id, data) {
    return api.put(`/postulaciones/${id}`, data)
  },
  
  deletePostulacion(id) {
    return api.delete(`/postulaciones/${id}`)
  },

  // ==================== CURRÍCULUM ====================
  
  getCurriculums(postulante_id = null) {
    const params = postulante_id ? `?postulante_id=${postulante_id}` : ''
    return api.get(`/curriculums${params}`)
  },
  
  getCurriculum(id) {
    return api.get(`/curriculums/${id}`)
  },
  
  createCurriculum(data) {
    return api.post('/curriculums', data)
  },
  
  updateCurriculum(id, data) {
    return api.put(`/curriculums/${id}`, data)
  },
  
  deleteCurriculum(id) {
    return api.delete(`/curriculums/${id}`)
  },

  // ==================== EDUCACIÓN ====================
  
  getEducaciones(curriculum_id = null) {
    const params = curriculum_id ? `?curriculum_id=${curriculum_id}` : ''
    return api.get(`/educaciones${params}`)
  },
  
  createEducacion(data) {
    return api.post('/educaciones', data)
  },
  
  updateEducacion(id, data) {
    return api.put(`/educaciones/${id}`, data)
  },
  
  deleteEducacion(id) {
    return api.delete(`/educaciones/${id}`)
  },

  // ==================== EXPERIENCIA LABORAL ====================
  
  getExperienciasLaborales(curriculum_id = null) {
    const params = curriculum_id ? `?curriculum_id=${curriculum_id}` : ''
    return api.get(`/experiencias-laborales${params}`)
  },
  
  createExperienciaLaboral(data) {
    return api.post('/experiencias-laborales', data)
  },
  
  updateExperienciaLaboral(id, data) {
    return api.put(`/experiencias-laborales/${id}`, data)
  },
  
  deleteExperienciaLaboral(id) {
    return api.delete(`/experiencias-laborales/${id}`)
  },

  // ==================== HABILIDADES ====================
  
  getHabilidades() {
    return api.get('/habilidades')
  },
  
  createHabilidad(data) {
    return api.post('/habilidades', data)
  },
  
  updateHabilidad(id, data) {
    return api.put(`/habilidades/${id}`, data)
  },
  
  deleteHabilidad(id) {
    return api.delete(`/habilidades/${id}`)
  },

  // ==================== ENTREVISTAS ====================
  
  getEntrevistas(postulacion_id = null) {
    const params = postulacion_id ? `?postulacion_id=${postulacion_id}` : ''
    return api.get(`/entrevistas${params}`)
  },
  
  createEntrevista(data) {
    return api.post('/entrevistas', data)
  },
  
  updateEntrevista(id, data) {
    return api.put(`/entrevistas/${id}`, data)
  },
  
  deleteEntrevista(id) {
    return api.delete(`/entrevistas/${id}`)
  },

  // ==================== NOTIFICACIONES ====================
  
  getNotificaciones(usuario_id = null, leida = null) {
    const params = new URLSearchParams()
    if (usuario_id) params.append('usuario_id', usuario_id)
    if (leida !== null) params.append('leida', leida)
    
    return api.get(`/notificaciones?${params.toString()}`)
  },
  
  createNotificacion(data) {
    return api.post('/notificaciones', data)
  },
  
  marcarNotificacionLeida(id) {
    return api.put(`/notificaciones/${id}/leer`)
  },
  
  marcarTodasNotificacionesLeidas(usuario_id) {
    return api.put(`/usuarios/${usuario_id}/notificaciones/leer-todas`)
  },

  // ==================== MENSAJES ====================
  
  getMensajes(emisor_id = null, receptor_id = null) {
    const params = new URLSearchParams()
    if (emisor_id) params.append('emisor_id', emisor_id)
    if (receptor_id) params.append('receptor_id', receptor_id)
    
    return api.get(`/mensajes?${params.toString()}`)
  },
  
  getMensajesEntreUsuarios(usuario1_id, usuario2_id) {
    return api.get(`/mensajes/entre-usuarios?usuario1_id=${usuario1_id}&usuario2_id=${usuario2_id}`)
  },
  
  createMensaje(data) {
    return api.post('/mensajes', data)
  },

  // ==================== EVALUACIONES ====================
  
  getEvaluaciones(postulacion_id = null, evaluador_id = null) {
    const params = new URLSearchParams()
    if (postulacion_id) params.append('postulacion_id', postulacion_id)
    if (evaluador_id) params.append('evaluador_id', evaluador_id)
    
    return api.get(`/evaluaciones?${params.toString()}`)
  },
  
  createEvaluacion(data) {
    return api.post('/evaluaciones', data)
  },
  
  updateEvaluacion(id, data) {
    return api.put(`/evaluaciones/${id}`, data)
  },

  // ==================== ENDPOINTS RELACIONALES ====================
  
  // Obtener ofertas de una empresa
  getOfertasByEmpresa(empresa_id, estado = null) {
    const params = estado ? `?estado=${estado}` : ''
    return api.get(`/empresas/${empresa_id}/ofertas-laborales${params}`)
  },
  
  // Obtener postulaciones de un postulante
  getPostulacionesByPostulante(postulante_id, estado = null) {
    const params = estado ? `?estado=${estado}` : ''
    return api.get(`/postulantes/${postulante_id}/postulaciones${params}`)
  },
  
  // Obtener postulantes de una oferta
  getPostulantesByOferta(oferta_id, estado = null) {
    const params = estado ? `?estado=${estado}` : ''
    return api.get(`/ofertas-laborales/${oferta_id}/postulantes${params}`)
  },
  
  // Obtener currículum de un postulante
  getCurriculumByPostulante(postulante_id) {
    return api.get(`/postulantes/${postulante_id}/curriculum`)
  },
  
  // Obtener educaciones de un currículum
  getEducacionesByCurriculum(curriculum_id) {
    return api.get(`/curriculums/${curriculum_id}/educaciones`)
  },
  
  // Obtener experiencias de un currículum
  getExperienciasByCurriculum(curriculum_id) {
    return api.get(`/curriculums/${curriculum_id}/experiencias-laborales`)
  },
  
  // Obtener entrevistas de una postulación
  getEntrevistasByPostulacion(postulacion_id) {
    return api.get(`/postulaciones/${postulacion_id}/entrevistas`)
  },
  
  // Obtener evaluaciones de una postulación
  getEvaluacionesByPostulacion(postulacion_id) {
    return api.get(`/postulaciones/${postulacion_id}/evaluaciones`)
  },
  
  // Obtener notificaciones de un usuario
  getNotificacionesByUsuario(usuario_id, leida = null) {
    const params = leida !== null ? `?leida=${leida}` : ''
    return api.get(`/usuarios/${usuario_id}/notificaciones${params}`)
  },

  // ==================== MÉTODOS DE UTILIDAD ====================
  
  // Actualizar estado de postulación
  actualizarEstadoPostulacion(postulacion_id, estado) {
    return api.put(`/postulaciones/${postulacion_id}/actualizar-estado`, { estado })
  },
  
  // Actualizar estado de oferta
  actualizarEstadoOferta(oferta_id, estado) {
    return api.put(`/ofertas-laborales/${oferta_id}/actualizar-estado`, { estado })
  },
  
  // Verificar si token está en blacklist
  checkTokenBlacklist(token) {
    return api.get(`/token-blacklist/check/${token}`)
  },

  // ==================== MÉTODOS PARA CURRÍCULUM COMPLETO ====================
  
  // Obtener currículum completo de un postulante (con todas las relaciones)
  async getCurriculumCompleto(postulante_id) {
    try {
      // Obtener currículum base
      const curriculumResponse = await this.getCurriculumByPostulante(postulante_id)
      const curriculum = curriculumResponse.data[0] // Asumiendo que hay un currículum por postulante
      
      if (!curriculum) {
        return {
          curriculum: null,
          educaciones: [],
          experiencias: [],
          postulante: null
        }
      }
      
      // Obtener datos relacionados en paralelo
      const [educacionesResponse, experienciasResponse, postulanteResponse] = await Promise.all([
        this.getEducacionesByCurriculum(curriculum.id),
        this.getExperienciasByCurriculum(curriculum.id),
        this.getPostulante(postulante_id)
      ])
      
      return {
        curriculum: curriculum,
        educaciones: educacionesResponse.data,
        experiencias: experienciasResponse.data,
        postulante: postulanteResponse.data
      }
    } catch (error) {
      console.error('Error obteniendo currículum completo:', error)
      throw error
    }
  },

  // Guardar currículum completo
  async saveCurriculumCompleto(postulante_id, curriculumData) {
    try {
      let curriculum_id
      
      // 1. Crear o actualizar currículum base
      if (curriculumData.curriculum_id) {
        await this.updateCurriculum(curriculumData.curriculum_id, {
          postulante_id: postulante_id,
          ruta_archivo: curriculumData.ruta_archivo || 'curriculum.pdf'
        })
        curriculum_id = curriculumData.curriculum_id
      } else {
        const curriculumResponse = await this.createCurriculum({
          postulante_id: postulante_id,
          ruta_archivo: curriculumData.ruta_archivo || 'curriculum.pdf'
        })
        curriculum_id = curriculumResponse.data.id
      }
      
      // 2. Guardar educaciones
      if (curriculumData.educaciones && curriculumData.educaciones.length > 0) {
        for (const educacion of curriculumData.educaciones) {
          if (educacion.id) {
            await this.updateEducacion(educacion.id, {
              ...educacion,
              curriculum_id: curriculum_id
            })
          } else {
            await this.createEducacion({
              ...educacion,
              curriculum_id: curriculum_id
            })
          }
        }
      }
      
      // 3. Guardar experiencias laborales
      if (curriculumData.experiencias && curriculumData.experiencias.length > 0) {
        for (const experiencia of curriculumData.experiencias) {
          if (experiencia.id) {
            await this.updateExperienciaLaboral(experiencia.id, {
              ...experiencia,
              curriculum_id: curriculum_id
            })
          } else {
            await this.createExperienciaLaboral({
              ...experiencia,
              curriculum_id: curriculum_id
            })
          }
        }
      }
      
      return { success: true, curriculum_id }
    } catch (error) {
      console.error('Error guardando currículum completo:', error)
      throw error
    }
  },

  // ==================== BÚSQUEDA Y FILTROS ====================
  
  // Búsqueda avanzada de ofertas
  buscarOfertas(filtros = {}) {
    const params = new URLSearchParams()
    
    Object.keys(filtros).forEach(key => {
      if (filtros[key] !== null && filtros[key] !== undefined && filtros[key] !== '') {
        params.append(key, filtros[key])
      }
    })
    
    return api.get(`/ofertas-laborales?${params.toString()}`)
  },
  
  // Búsqueda de postulantes
  buscarPostulantes(filtros = {}) {
    const params = new URLSearchParams()
    
    Object.keys(filtros).forEach(key => {
      if (filtros[key] !== null && filtros[key] !== undefined && filtros[key] !== '') {
        params.append(key, filtros[key])
      }
    })
    
    return api.get(`/postulantes?${params.toString()}`)
  },

  // ==================== ESTADÍSTICAS Y REPORTES ====================
  
  // Obtener estadísticas generales
  async getEstadisticas() {
    try {
      const [ofertas, empresas, postulantes, postulaciones] = await Promise.all([
        this.getOfertas(),
        this.getEmpresas(),
        this.getPostulantes(),
        this.getPostulaciones()
      ])
      
      return {
        total_ofertas: ofertas.data.length,
        total_empresas: empresas.data.length,
        total_postulantes: postulantes.data.length,
        total_postulaciones: postulaciones.data.length,
        ofertas_activas: ofertas.data.filter(o => o.estado === 'activa').length,
        postulaciones_pendientes: postulaciones.data.filter(p => p.estado === 'pendiente').length
      }
    } catch (error) {
      console.error('Error obteniendo estadísticas:', error)
      throw error
    }
  },

  // ==================== INICIALIZACIÓN ====================
  
  // Inicializar datos del sistema
  initializeData() {
    return api.post('/init-data/')
  }
}