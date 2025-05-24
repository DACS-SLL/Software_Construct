import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import Dashboard from '../components/Dashboard.vue'
import Autores from '../components/Autores.vue'
import Libros from '../components/Libros.vue'
import Generos from '../components/Generos.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    redirect: '/dashboard/autores',
    children: [
      {
        path: 'autores',
        name: 'autores',
        component: Autores
      },
      {
        path: 'libros',
        name: 'libros',
        component: Libros
      },
      {
        path: 'generos',
        name: 'generos',
        component: Generos
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard de autenticación
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const token = localStorage.getItem('token')

  if (requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
