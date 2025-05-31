import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '/src/views/HomeView.vue'
import OfertasView from '/src/views/OfertasView.vue'
import EmpresasView from '/src/views/EmpresasView.vue'
import PostulantesView from '/src/views/PostulantesView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/ofertas',
    name: 'ofertas',
    component: OfertasView
  },
  {
    path: '/empresas',
    name: 'empresas',
    component: EmpresasView
  },
  {
    path: '/postulantes',
    name: 'postulantes',
    component: PostulantesView
  },

  {
    path: '/postulantes/:id',
    name: 'postulante-detail',
    component: () => import('/src/views/PostulanteDetailView.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router