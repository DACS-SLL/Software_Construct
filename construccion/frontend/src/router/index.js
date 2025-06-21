import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import OfertasView from '../views/OfertasView.vue'
import EmpresasView from '../views/EmpresasView.vue'
import PostulantesView from '../views/PostulantesView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'

// Nuevos imports para los componentes avanzados
import DashboardView from '../views/DashboardView.vue'
import AdvancedJobSearchView from '../views/AdvancedJobSearchView.vue'
import ProfileView from '../views/ProfileView.vue'

const routes = [
  // ==================== RUTAS PÚBLICAS ====================
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      title: 'Inicio - Plataforma de Empleo',
      description: 'Encuentra tu trabajo ideal o el candidato perfecto'
    }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { 
      hideNavigation: true,
      title: 'Iniciar Sesión',
      guest: true // Solo para usuarios no autenticados
    }
  },
  {
    path: '/register',
    name: 'register', 
    component: RegisterView,
    meta: { 
      hideNavigation: true,
      title: 'Registro',
      guest: true // Solo para usuarios no autenticados
    }
  },

  // ==================== OFERTAS Y BÚSQUEDA ====================
  {
    path: '/ofertas',
    name: 'ofertas',
    component: OfertasView,
    meta: {
      title: 'Ofertas de Trabajo',
      description: 'Explora todas las ofertas laborales disponibles'
    }
  },
  {
    path: '/ofertas/:id',
    name: 'oferta-detail',
    component: () => import('../views/OfertaDetailView.vue'),
    meta: {
      title: 'Detalle de Oferta'
    }
  },
  {
    path: '/buscar-empleos',
    name: 'advanced-search',
    component: AdvancedJobSearchView,
    meta: {
      title: 'Búsqueda Avanzada de Empleos',
      description: 'Encuentra tu trabajo ideal con filtros avanzados'
    }
  },

  // ==================== EMPRESAS ====================
  {
    path: '/empresas',
    name: 'empresas',
    component: EmpresasView,
    meta: {
      title: 'Empresas',
      description: 'Descubre las empresas que están contratando'
    }
  },
  {
    path: '/empresas/:id',
    name: 'empresa-detail',
    component: () => import('../views/EmpresaDetailView.vue'),
    meta: {
      title: 'Perfil de Empresa'
    }
  },
  //{
    //path: '/empresas/:id/ofertas',
    //name: 'empresa-ofertas',
    //component: () => import('../views/EmpresaOfertasView.vue'),
    //meta: {
      //title: 'Ofertas de la Empresa'
    //}
  //},

  // ==================== POSTULANTES ====================
  {
    path: '/postulantes',
    name: 'postulantes',
    component: PostulantesView,
    meta: {
      title: 'Postulantes',
      description: 'Encuentra el talento perfecto para tu empresa',
      requiresAuth: true,
      roles: ['empresa', 'admin'] // Solo empresas y admins pueden ver postulantes
    }
  },
  {
    path: '/postulantes/:id',
    name: 'postulante-detail',
    component: () => import('../views/PostulanteDetailView.vue'),
    meta: {
      title: 'Perfil de Postulante',
      requiresAuth: true
    }
  },

  // ==================== PERFIL Y CV ====================
  {
    path: '/perfil/:id?',
    name: 'profile',
    component: ProfileView,
    meta: {
      title: 'Perfil Profesional',
      requiresAuth: true
    }
  },
  {
    path: '/mi-perfil',
    name: 'mi-perfil',
    component: () => import('../views/MiPerfilView.vue'),
    meta: {
      title: 'Mi Perfil',
      requiresAuth: true
    }
  },
  {
    path: '/curriculum',
    name: 'curriculum',
    component: () => import('../views/Curriculums.vue'),
    meta: {
      title: 'Mi Currículum',
      requiresAuth: true,
      roles: ['admin']
    }
  },

  // ==================== DASHBOARD Y GESTIÓN ====================
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      title: 'Dashboard',
      requiresAuth: true,
      roles: ['empresa', 'admin'] // Solo empresas y admins tienen dashboard
    }
  },
  {
    path: '/mis-ofertas',
    name: 'mis-ofertas',
    component: () => import('../views/MisOfertasView.vue'),
    meta: {
      title: 'Mis Ofertas',
      requiresAuth: true,
      roles: ['empresa', 'admin']
    }
  },
  {
    path: '/mis-postulaciones',
    name: 'mis-postulaciones',
    component: () => import('../views/MisPostulacionesView.vue'),
    meta: {
      title: 'Mis Postulaciones',
      requiresAuth: true,
      roles: ['postulante']
    }
  },

  // ==================== COMUNICACIÓN ====================
  {
    path: '/mensajes',
    name: 'mensajes',
    component: () => import('../views/MensajesView.vue'),
    meta: {
      title: 'Mensajes',
      requiresAuth: true
    }
  },
  {
    path: '/notificaciones',
    name: 'notificaciones',
    component: () => import('../views/NotificacionesView.vue'),
    meta: {
      title: 'Notificaciones',
      requiresAuth: true
    }
  },

  // ==================== CONFIGURACIÓN ====================
  {
    path: '/configuracion',
    name: 'configuracion',
    component: () => import('../views/ConfiguracionView.vue'),
    meta: {
      title: 'Configuración',
      requiresAuth: true
    }
  },

  // ==================== PÁGINAS INFORMATIVAS ====================
  {
    path: '/acerca-de',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: {
      title: 'Acerca de Nosotros'
    }
  },
  {
    path: '/contacto',
    name: 'contact',
    component: () => import('../views/ContactView.vue'),
    meta: {
      title: 'Contacto'
    }
  },
  {
    path: '/terminos',
    name: 'terms',
    component: () => import('../views/TermsView.vue'),
    meta: {
      title: 'Términos y Condiciones'
    }
  },
  {
    path: '/privacidad',
    name: 'privacy',
    component: () => import('../views/PrivacyView.vue'),
    meta: {
      title: 'Política de Privacidad'
    }
  },

  // ==================== RECUPERACIÓN DE CONTRASEÑA ====================
  {
    path: '/recuperar-password',
    name: 'forgot-password',
    component: () => import('../views/ForgotPasswordView.vue'),
    meta: {
      hideNavigation: true,
      title: 'Recuperar Contraseña',
      guest: true
    }
  },
  {
    path: '/restablecer-password',
    name: 'reset-password',
    component: () => import('../views/ResetPasswordView.vue'),
    meta: {
      hideNavigation: true,
      title: 'Restablecer Contraseña',
      guest: true
    }
  },

  // ==================== PÁGINAS DE ERROR ====================
  {
    path: '/403',
    name: 'forbidden',
    component: () => import('../views/ForbiddenView.vue'),
    meta: {
      title: 'Acceso Prohibido',
      hideNavigation: false
    }
  },
  {
    path: '/404',
    name: 'not-found',
    component: () => import('../views/NotFoundView.vue'),
    meta: {
      title: 'Página No Encontrada',
      hideNavigation: false
    }
  },

  // ==================== RUTA CATCH-ALL ====================
  {
    path: '/:pathMatch(.*)*',
    redirect: '/404'
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // Comportamiento de scroll personalizado
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  }
})

// ==================== GUARDS DE NAVEGACIÓN ====================

// Guard global para autenticación
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  const userRole = user.user_type || user.rol

  // Actualizar título de la página
  if (to.meta.title) {
    document.title = `${to.meta.title} - Plataforma de Empleo`
  }

  // Rutas que requieren autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({
      name: 'login',
      query: { redirect: to.fullPath }
    })
    return
  }

  // Rutas solo para invitados (no autenticados)
  if (to.meta.guest && isAuthenticated) {
    next({ name: 'dashboard' })
    return
  }

  // Verificar roles específicos
  if (to.meta.roles && isAuthenticated) {
    const allowedRoles = to.meta.roles
    const hasPermission = allowedRoles.some(role => {
      if (role === 'admin') return userRole === 'admin'
      if (role === 'empresa') return userRole === 'empresa' || userRole === 'admin'
      if (role === 'postulante') return userRole === 'postulante' || userRole === 'usuario'
      return false
    })

    if (!hasPermission) {
      next({ name: 'forbidden' })
      return
    }
  }

  // Redirección especial para /perfil sin ID
  if (to.name === 'profile' && !to.params.id && isAuthenticated) {
    // Redirigir al perfil del usuario actual
    next({ name: 'profile', params: { id: user.id || 'me' } })
    return
  }

  next()
})

// Guard después de la navegación para analytics (opcional)
router.afterEach((to, from) => {
  // Aquí puedes agregar tracking de analytics
  console.log(`Navegando de ${from.name} a ${to.name}`)
  
  // Ejemplo de Google Analytics
  // if (window.gtag) {
  //   window.gtag('config', 'GA_TRACKING_ID', {
  //     page_path: to.fullPath,
  //     page_title: to.meta.title
  //   })
  // }
})

export default router