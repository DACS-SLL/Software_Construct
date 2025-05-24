import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'

// Importar Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUser, faBook, faTag, faSignOutAlt } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Agregar iconos a la biblioteca
library.add(faUser, faBook, faTag, faSignOutAlt)

const app = createApp(App)

// Registrar el componente global de FontAwesome
app.component('font-awesome-icon', FontAwesomeIcon)

// Usar el router
app.use(router)

app.mount('#app')
