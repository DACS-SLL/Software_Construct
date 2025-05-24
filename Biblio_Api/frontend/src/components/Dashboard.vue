<template>
  <div class="dashboard">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h2>Biblioteca API</h2>
      </div>
      <div class="sidebar-menu">
        <router-link to="/dashboard/autores" class="menu-item" active-class="active">
          <i class="fas fa-user"></i>
          Autores
        </router-link>
        <router-link to="/dashboard/libros" class="menu-item" active-class="active">
          <i class="fas fa-book"></i>
          Libros
        </router-link>
        <router-link to="/dashboard/generos" class="menu-item" active-class="active">
          <i class="fas fa-tag"></i>
          Géneros
        </router-link>
        <button class="menu-item logout-button" @click="handleLogout">
          <i class="fas fa-sign-out-alt"></i>
          Cerrar Sesión
        </button>
      </div>
    </nav>

    <main class="main-content">
      <div class="content-header">
        <h2>{{ currentSection }}</h2>
        <div class="user-info">
          <span>Bienvenido, {{ currentUser?.username || 'Adobo' }}</span>
        </div>
      </div>

      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'Dashboard',
  setup() {
    const router = useRouter()
    const savedUser = localStorage.getItem('user')
const currentUser = ref(savedUser ? JSON.parse(savedUser) : null)

    const currentSection = computed(() => {
      const path = router.currentRoute.value.path
      if (path.includes('autores')) return 'Autores'
      if (path.includes('libros')) return 'Libros'
      if (path.includes('generos')) return 'Géneros'
      return 'Dashboard'
    })

    const handleLogout = () => {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      router.push('/login')
    }

    return {
      currentUser,
      currentSection,
      handleLogout
    }
  }
}
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background-color: var(--primary-color);
  color: white;
  padding: 1rem;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-radius: var(--border-radius);
  text-decoration: none;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.menu-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.menu-item i {
  width: 20px;
}

.menu-item.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: bold;
}

.main-content {
  flex: 1;
  padding: 2rem;
  background-color: var(--background-color);
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.content-header h2 {
  color: var(--primary-color);
}

.user-info {
  font-size: 0.9rem;
  color: var(--text-color);
}

.logout-button {
  background: none;
  border: none;
  color: white;
  text-align: left;
}
.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

</style>
