<v-card-text class="pa-6">
            <v-form ref="personalForm">
              <v-row>
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="personalInfo.nombre_completo"
                    label="Nombre completo"
                    variant="outlined"
                    prepend-inner-icon="mdi-account"
                    :rules="[v => !!v || 'Campo requerido']"
                    color="primary"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="personalInfo.email"
                    label="Correo electrónico"
                    type="email"
                    variant="outlined"
                    prepend-inner-icon="mdi-email"
                    :rules="emailRules"
                    color="primary"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="personalInfo.telefono"
                    label="Teléfono"
                    variant="outlined"
                    prepend-inner-icon="mdi-phone"
                    color="primary"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12" md="6">
                  <v-text-field
                    v-model="personalInfo.fecha_nacimiento"
                    label="Fecha de nacimiento"
                    type="date"
                    variant="outlined"
                    prepend-inner-icon="mdi-calendar"
                    color="primary"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-text-field
                    v-model="personalInfo.direccion"
                    label="Dirección"
                    variant="outlined"
                    prepend-inner-icon="mdi-map-marker"
                    color="primary"
                  ></v-text-field>
                </v-col>
                
                <v-col cols="12">
                  <v-textarea
                    v-model="personalInfo.resumen_profesional"
                    label="Resumen profesional"
                    variant="outlined"
                    rows="4"
                    prepend-inner-icon="mdi-text"
                    hint="Describe brevemente tu experiencia y objetivos profesionales"
                    color="primary"
                  ></v-textarea>
                </v-col>
              </v-row>
              
              <v-btn
                color="primary"
                @click="savePersonalInfo"
                :loading="saving.personal"
                class="mt-4"
              >
                <v-icon left>mdi-content-save</v-icon>
                Guardar Información
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <!-- Experiencia Laboral -->
        <v-card v-if="activeSection === 'experience'" class="mb-6" rounded="lg" elevation="2">
          <v-card-title class="text-h5 pa-6 bg-success-lighten-5">
            <v-icon color="success" class="mr-3">mdi-briefcase</v-icon>
            Experiencia Laboral
            <v-spacer></v-spacer>
            <v-btn
              color="success"
              @click="openExperienceDialog()"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text class="pa-6">
            <div v-if="experiences.length === 0" class="text-center py-8">
              <v-icon size="64" color="grey-lighten-2">mdi-briefcase-outline</v-icon>
              <p class="text-h6 text-grey mt-4">No hay experiencia laboral registrada</p>
              <p class="text-body-2 text-grey">Agrega tu primera experiencia laboral</p>
            </div>
            
            <v-timeline v-else side="end" align="start">
              <v-timeline-item
                v-for="(exp, index) in experiences"
                :key="index"
                dot-color="success"
                size="small"
              >
                <template v-slot:opposite>
                  <div class="text-caption text-grey">
                    {{ formatDate(exp.fecha_inicio) }} - 
                    {{ exp.fecha_fin ? formatDate(exp.fecha_fin) : 'Actual' }}
                  </div>
                </template>
                
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-h6">{{ exp.cargo }}</v-card-title>
                  <v-card-subtitle>{{ exp.empresa }}</v-card-subtitle>
                  <v-card-text>{{ exp.descripcion }}</v-card-text>
                  <v-card-actions>
                    <v-btn
                      color="primary"
                      variant="text"
                      @click="openExperienceDialog(exp, index)"
                      prepend-icon="mdi-pencil"
                    >
                      Editar
                    </v-btn>
                    <v-btn
                      color="error"
                      variant="text"
                      @click="deleteExperience(index)"
                      prepend-icon="mdi-delete"
                    >
                      Eliminar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>

        <!-- Educación -->
        <v-card v-if="activeSection === 'education'" class="mb-6" rounded="lg" elevation="2">
          <v-card-title class="text-h5 pa-6 bg-info-lighten-5">
            <v-icon color="info" class="mr-3">mdi-school</v-icon>
            Educación
            <v-spacer></v-spacer>
            <v-btn
              color="info"
              @click="openEducationDialog()"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text class="pa-6">
            <div v-if="education.length === 0" class="text-center py-8">
              <v-icon size="64" color="grey-lighten-2">mdi-school-outline</v-icon>
              <p class="text-h6 text-grey mt-4">No hay educación registrada</p>
              <p class="text-body-2 text-grey">Agrega tu formación académica</p>
            </div>
            
            <v-timeline v-else side="end" align="start">
              <v-timeline-item
                v-for="(edu, index) in education"
                :key="index"
                dot-color="info"
                size="small"
              >
                <template v-slot:opposite>
                  <div class="text-caption text-grey">
                    {{ formatDate(edu.fecha_inicio) }} - 
                    {{ edu.fecha_fin ? formatDate(edu.fecha_fin) : 'En curso' }}
                  </div>
                </template>
                
                <v-card variant="outlined" class="mb-4">
                  <v-card-title class="text-h6">{{ edu.titulo }}</v-card-title>
                  <v-card-subtitle>{{ edu.institucion }}</v-card-subtitle>
                  <v-card-actions>
                    <v-btn
                      color="primary"
                      variant="text"
                      @click="openEducationDialog(edu, index)"
                      prepend-icon="mdi-pencil"
                    >
                      Editar
                    </v-btn>
                    <v-btn
                      color="error"
                      variant="text"
                      @click="deleteEducation(index)"
                      prepend-icon="mdi-delete"
                    >
                      Eliminar
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>

        <!-- Habilidades -->
        <v-card v-if="activeSection === 'skills'" class="mb-6" rounded="lg" elevation="2">
          <v-card-title class="text-h5 pa-6 bg-warning-lighten-5">
            <v-icon color="warning" class="mr-3">mdi-star</v-icon>
            Habilidades
          </v-card-title>
          
          <v-card-text class="pa-6">
            <v-form ref="skillsForm">
              <v-combobox
                v-model="skills"
                label="Habilidades"
                variant="outlined"
                multiple
                chips
                clearable
                prepend-inner-icon="mdi-lightbulb"
                hint="Presiona Enter para agregar una habilidad"
                color="warning"
                class="mb-4"
              >
                <template v-slot:chip="{ props, item }">
                  <v-chip
                    v-bind="props"
                    :text="item"
                    color="warning"
                    variant="elevated"
                  ></v-chip>
                </template>
              </v-combobox>
              
              <v-btn
                color="warning"
                @click="saveSkills"
                :loading="saving.skills"
                class="mt-4"
              >
                <v-icon left>mdi-content-save</v-icon>
                Guardar Habilidades
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <!-- Documentos -->
        <v-card v-if="activeSection === 'documents'" class="mb-6" rounded="lg" elevation="2">
          <v-card-title class="text-h5 pa-6 bg-secondary-lighten-5">
            <v-icon color="secondary" class="mr-3">mdi-file-document</v-icon>
            Documentos
          </v-card-title>
          
          <v-card-text class="pa-6">
            <!-- Upload de CV -->
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Currículum Vitae (PDF)</h3>
              <v-file-input
                v-model="cvFile"
                label="Seleccionar archivo CV"
                variant="outlined"
                accept=".pdf"
                prepend-inner-icon="mdi-file-pdf-box"
                @change="uploadCV"
                color="secondary"
              ></v-file-input>
              
              <v-card v-if="currentCV" variant="outlined" class="mt-4">
                <v-card-text class="d-flex align-center">
                  <v-icon color="red" class="mr-3">mdi-file-pdf-box</v-icon>
                  <div class="flex-grow-1">
                    <div class="font-weight-bold">{{ currentCV.nombre }}</div>
                    <div class="text-caption text-grey">
                      Subido el {{ formatDate(currentCV.fecha_subida) }}
                    </div>
                  </div>
                  <v-btn
                    color="primary"
                    variant="text"
                    @click="downloadCV"
                    prepend-icon="mdi-download"
                  >
                    Descargar
                  </v-btn>
                </v-card-text>
              </v-card>
            </div>
            
            <!-- Otros documentos -->
            <div>
              <h3 class="text-h6 mb-3">Otros Documentos</h3>
              <v-file-input
                v-model="otherFiles"
                label="Certificados, diplomas, etc."
                variant="outlined"
                multiple
                accept=".pdf,.jpg,.png,.jpeg"
                prepend-inner-icon="mdi-file-multiple"
                @change="uploadOtherFiles"
                color="secondary"
              ></v-file-input>
              
              <v-list v-if="otherDocuments.length > 0" class="mt-4">
                <v-list-item
                  v-for="(doc, index) in otherDocuments"
                  :key="index"
                >
                  <template v-slot:prepend>
                    <v-icon>{{ getFileIcon(doc.tipo) }}</v-icon>
                  </template>
                  
                  <v-list-item-title>{{ doc.nombre }}</v-list-item-title>
                  <v-list-item-subtitle>{{ formatDate(doc.fecha_subida) }}</v-list-item-subtitle>
                  
                  <template v-slot:append>
                    <v-btn
                      icon
                      variant="text"
                      @click="downloadDocument(doc)"
                    >
                      <v-icon>mdi-download</v-icon>
                    </v-btn>
                    <v-btn
                      icon
                      variant="text"
                      color="error"
                      @click="deleteDocument(index)"
                    >
                      <v-icon>mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Dialog para Experiencia -->
    <v-dialog v-model="experienceDialog" max-width="600px">
      <v-card rounded="lg">
        <v-card-title class="text-h5">
          {{ editingExperience ? 'Editar' : 'Agregar' }} Experiencia
        </v-card-title>
        
        <v-card-text>
          <v-form ref="experienceForm">
            <v-text-field
              v-model="experienceForm.cargo"
              label="Cargo/Puesto"
              variant="outlined"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="experienceForm.empresa"
              label="Empresa"
              variant="outlined"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-4"
            ></v-text-field>
            
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="experienceForm.fecha_inicio"
                  label="Fecha de inicio"
                  type="date"
                  variant="outlined"
                  :rules="[v => !!v || 'Campo requerido']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="6">
                <v-text-field
                  v-model="experienceForm.fecha_fin"
                  label="Fecha de fin"
                  type="date"
                  variant="outlined"
                  :disabled="experienceForm.actual"
                ></v-text-field>
              </v-col>
            </v-row>
            
            <v-checkbox
              v-model="experienceForm.actual"
              label="Trabajo actual"
              @change="if(experienceForm.actual) experienceForm.fecha_fin = ''"
            ></v-checkbox>
            
            <v-textarea
              v-model="experienceForm.descripcion"
              label="Descripción de funciones"
              variant="outlined"
              rows="4"
              hint="Describe tus principales responsabilidades y logros"
            ></v-textarea>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="closeExperienceDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveExperience">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Dialog para Educación -->
    <v-dialog v-model="educationDialog" max-width="600px">
      <v-card rounded="lg">
        <v-card-title class="text-h5">
          {{ editingEducation ? 'Editar' : 'Agregar' }} Educación
        </v-card-title>
        
        <v-card-text>
          <v-form ref="educationFormRef">
            <v-text-field
              v-model="educationForm.titulo"
              label="Título/Grado"
              variant="outlined"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model="educationForm.institucion"
              label="Institución"
              variant="outlined"
              :rules="[v => !!v || 'Campo requerido']"
              class="mb-4"
            ></v-text-field>
            
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="educationForm.fecha_inicio"
                  label="Fecha de inicio"
                  type="date"
                  variant="outlined"
                  :rules="[v => !!v || 'Campo requerido']"
                ></v-text-field>
              </v-col>
              
              <v-col cols="6">
                <v-text-field
                  v-model="educationForm.fecha_fin"
                  label="Fecha de fin"
                  type="date"
                  variant="outlined"
                  :disabled="educationForm.en_curso"
                ></v-text-field>
              </v-col>
            </v-row>
            
            <v-checkbox
              v-model="educationForm.en_curso"
              label="Estudios en curso"
              @change="if(educationForm.en_curso) educationForm.fecha_fin = ''"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="closeEducationDialog">Cancelar</v-btn>
          <v-btn color="primary" @click="saveEducation">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Snackbar -->
    <v-snackbar
      v-model="snackbar.show"
      :color="snackbar.color"
      :timeout="4000"
      location="top right"
    >
      {{ snackbar.message }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar.show = false">
          Cerrar
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '/src/api/api'

const router = useRouter()

// Estado reactivo
const activeSection = ref('personal')
const saving = ref({
  personal: false,
  skills: false
})

// Datos del currículum
const personalInfo = ref({
  nombre_completo: '',
  email: '',
  telefono: '',
  fecha_nacimiento: '',
  direccion: '',
  resumen_profesional: ''
})

const experiences = ref([])
const education = ref([])
const skills = ref([])
const currentCV = ref(null)
const otherDocuments = ref([])

// Formularios y dialogs
const experienceDialog = ref(false)
const educationDialog = ref(false)
const editingExperience = ref(false)
const editingEducation = ref(false)
const editingIndex = ref(-1)

const experienceForm = ref({
  cargo: '',
  empresa: '',
  fecha_inicio: '',
  fecha_fin: '',
  descripcion: '',
  actual: false
})

const educationForm = ref({
  titulo: '',
  institucion: '',
  fecha_inicio: '',
  fecha_fin: '',
  en_curso: false
})

// Archivos
const cvFile = ref(null)
const otherFiles = ref([])

// Snackbar
const snackbar = ref({
  show: false,
  message: '',
  color: 'success'
})

// Secciones de navegación
const sections = ref([
  { id: 'personal', title: 'Información Personal', icon: 'mdi-account', completed: false },
  { id: 'experience', title: 'Experiencia Laboral', icon: 'mdi-briefcase', completed: false },
  { id: 'education', title: 'Educación', icon: 'mdi-school', completed: false },
  { id: 'skills', title: 'Habilidades', icon: 'mdi-star', completed: false },
  { id: 'documents', title: 'Documentos', icon: 'mdi-file-document', completed: false }
])

// Reglas de validación
const emailRules = [
  v => !!v || 'El email es requerido',
  v => /.+@.+\..+/.test(v) || 'El email debe ser válido'
]

// Computed
const profileCompleteness = computed(() => {
  let total = 0
  let completed = 0
  
  // Información personal (30%)
  total += 30
  if (personalInfo.value.nombre_completo && personalInfo.value.email && personalInfo.value.resumen_profesional) {
    completed += 30
  }
  
  // Experiencia (25%)
  total += 25
  if (experiences.value.length > 0) {
    completed += 25
  }
  
  // Educación (20%)
  total += 20
  if (education.value.length > 0) {
    completed += 20
  }
  
  // Habilidades (15%)
  total += 15
  if (skills.value.length > 0) {
    completed += 15
  }
  
  // Documentos (10%)
  total += 10
  if (currentCV.value) {
    completed += 10
  }
  
  return Math.round((completed / total) * 100)
})

// Métodos
const getProfileStatus = () => {
  const completeness = profileCompleteness.value
  if (completeness >= 90) return 'Excelente'
  if (completeness >= 70) return 'Muy Bueno'
  if (completeness >= 50) return 'Bueno'
  if (completeness >= 30) return 'Regular'
  return 'Incompleto'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'short' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const savePersonalInfo = async () => {
  saving.value.personal = true
  try {
    // Aquí iría la llamada a la API
    await new Promise(resolve => setTimeout(resolve, 1000))
    showSnackbar('Información personal guardada correctamente', 'success')
    updateSectionStatus('personal', true)
  } catch (error) {
    showSnackbar('Error al guardar la información', 'error')
  } finally {
    saving.value.personal = false
  }
}

const saveSkills = async () => {
  saving.value.skills = true
  try {
    // Aquí iría la llamada a la API
    await new Promise(resolve => setTimeout(resolve, 1000))
    showSnackbar('Habilidades guardadas correctamente', 'success')
    updateSectionStatus('skills', skills.value.length > 0)
  } catch (error) {
    showSnackbar('Error al guardar las habilidades', 'error')
  } finally {
    saving.value.skills = false
  }
}

const openExperienceDialog = (experience = null, index = -1) => {
  if (experience) {
    experienceForm.value = { ...experience }
    editingExperience.value = true
    editingIndex.value = index
  } else {
    experienceForm.value = {
      cargo: '',
      empresa: '',
      fecha_inicio: '',
      fecha_fin: '',
      descripcion: '',
      actual: false
    }
    editingExperience.value = false
    editingIndex.value = -1
  }
  experienceDialog.value = true
}

const closeExperienceDialog = () => {
  experienceDialog.value = false
  editingExperience.value = false
  editingIndex.value = -1
}

const saveExperience = () => {
  if (editingExperience.value) {
    experiences.value[editingIndex.value] = { ...experienceForm.value }
  } else {
    experiences.value.push({ ...experienceForm.value })
  }
  
  updateSectionStatus('experience', experiences.value.length > 0)
  showSnackbar('Experiencia guardada correctamente', 'success')
  closeExperienceDialog()
}

const deleteExperience = (index) => {
  experiences.value.splice(index, 1)
  updateSectionStatus('experience', experiences.value.length > 0)
  showSnackbar('Experiencia eliminada', 'info')
}

const openEducationDialog = (educationItem = null, index = -1) => {
  if (educationItem) {
    educationForm.value = { ...educationItem }
    editingEducation.value = true
    editingIndex.value = index
  } else {
    educationForm.value = {
      titulo: '',
      institucion: '',
      fecha_inicio: '',
      fecha_fin: '',
      en_curso: false
    }
    editingEducation.value = false
    editingIndex.value = -1
  }
  educationDialog.value = true
}

const closeEducationDialog = () => {
  educationDialog.value = false
  editingEducation.value = false
  editingIndex.value = -1
}

const saveEducation = () => {
  if (editingEducation.value) {
    education.value[editingIndex.value] = { ...educationForm.value }
  } else {
    education.value.push({ ...educationForm.value })
  }
  
  updateSectionStatus('education', education.value.length > 0)
  showSnackbar('Educación guardada correctamente', 'success')
  closeEducationDialog()
}

const deleteEducation = (index) => {
  education.value.splice(index, 1)
  updateSectionStatus('education', education.value.length > 0)
  showSnackbar('Educación eliminada', 'info')
}

const uploadCV = async () => {
  if (cvFile.value) {
    try {
      // Simular upload
      await new Promise(resolve => setTimeout(resolve, 1500))
      currentCV.value = {
        nombre: cvFile.value.name,
        fecha_subida: new Date().toISOString(),
        url: '#'
      }
      updateSectionStatus('documents', true)
      showSnackbar('CV subido correctamente', 'success')
    } catch (error) {
      showSnackbar('Error al subir el CV', 'error')
    }
  }
}

const uploadOtherFiles = async () => {
  if (otherFiles.value && otherFiles.value.length > 0) {
    try {
      // Simular upload
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      otherFiles.value.forEach(file => {
        otherDocuments.value.push({
          nombre: file.name,
          tipo: file.type,
          fecha_subida: new Date().toISOString(),
          url: '#'
        })
      })
      
      showSnackbar(`${otherFiles.value.length} documento(s) subido(s) correctamente`, 'success')
      otherFiles.value = []
    } catch (error) {
      showSnackbar('Error al subir los documentos', 'error')
    }
  }
}

const downloadCV = () => {
  showSnackbar('Descargando CV...', 'info')
}

const downloadDocument = (doc) => {
  showSnackbar(`Descargando ${doc.nombre}...`, 'info')
}

const deleteDocument = (index) => {
  otherDocuments.value.splice(index, 1)
  showSnackbar('Documento eliminado', 'info')
}

const getFileIcon = (fileType) => {
  if (fileType.includes('pdf')) return 'mdi-file-pdf-box'
  if (fileType.includes('image')) return 'mdi-file-image'
  return 'mdi-file-document'
}

const updateSectionStatus = (sectionId, completed) => {
  const section = sections.value.find(s => s.id === sectionId)
  if (section) {
    section.completed = completed
  }
}

const previewCV = () => {
  showSnackbar('Abriendo vista previa del CV...', 'info')
  // Aquí se abriría un modal con la vista previa del CV
}

const showSnackbar = (message, color = 'success') => {
  snackbar.value = {
    show: true,
    message,
    color
  }
}

// Lifecycle
onMounted(() => {
  // Cargar datos del currículum
  loadCurriculumData()
})

const loadCurriculumData = async () => {
  try {
    // Aquí cargarías los datos reales del usuario desde la API
    // const userData = await api.getUserProfile()
    
    // Datos de ejemplo
    personalInfo.value = {
      nombre_completo: 'Juan Pérez García',
      email: 'juan.perez@email.com',
      telefono: '+51 987 654 321',
      fecha_nacimiento: '1995-05-15',
      direccion: 'Av. Ejercito 123, Arequipa',
      resumen_profesional: 'Desarrollador Full Stack con 3 años de experiencia en tecnologías web modernas. Apasionado por crear soluciones innovadoras y eficientes.'
    }
    
    experiences.value = [
      {
        cargo: 'Desarrollador Frontend',
        empresa: 'Tech Solutions S.A.',
        fecha_inicio: '2021-06-01',
        fecha_fin: '2023-12-31',
        descripcion: 'Desarrollo de aplicaciones web usando React, Vue.js y TypeScript. Implementación de interfaces responsive y optimización de performance.',
        actual: false
      },
      {
        cargo: 'Desarrollador Full Stack',
        empresa: 'Innovatech',
        fecha_inicio: '2024-01-15',
        fecha_fin: '',
        descripcion: 'Desarrollo completo de aplicaciones web con Vue.js, Node.js y PostgreSQL. Liderazgo de proyectos y mentoring a desarrolladores junior.',
        actual: true
      }
    ]
    
    education.value = [
      {
        titulo: 'Ingeniería de Sistemas',
        institucion: 'Universidad Nacional de San Agustín',
        fecha_inicio: '2018-03-01',
        fecha_fin: '2022-12-15',
        en_curso: false
      },
      {
        titulo: 'Certificación en React',
        institucion: 'Platzi',
        fecha_inicio: '2021-05-01',
        fecha_fin: '2021-08-15',
        en_curso: false
      }
    ]
    
    skills.value = [
      'JavaScript', 'Vue.js', 'React', 'Node.js', 'Python', 
      'PostgreSQL', 'MongoDB', 'Git', 'Docker', 'AWS'
    ]
    
    // Actualizar estado de las secciones
    updateSectionStatus('personal', true)
    updateSectionStatus('experience', experiences.value.length > 0)
    updateSectionStatus('education', education.value.length > 0)
    updateSectionStatus('skills', skills.value.length > 0)
    
  } catch (error) {
    console.error('Error cargando datos del currículum:', error)
    showSnackbar('Error al cargar los datos del currículum', 'error')
  }
}
</script>

<style scoped>
.curriculum-container {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.sticky-sidebar {
  position: sticky;
  top: 24px;
  height: fit-content;
}

.bg-primary-lighten-5 {
  background-color: rgba(var(--v-theme-primary), 0.1) !important;
}

.bg-success-lighten-5 {
  background-color: rgba(var(--v-theme-success), 0.1) !important;
}

.bg-info-lighten-5 {
  background-color: rgba(var(--v-theme-info), 0.1) !important;
}

.bg-warning-lighten-5 {
  background-color: rgba(var(--v-theme-warning), 0.1) !important;
}

.bg-secondary-lighten-5 {
  background-color: rgba(var(--v-theme-secondary), 0.1) !important;
}

/* Animaciones */
.v-card {
  transition: all 0.3s ease;
}

.v-card:hover {
  transform: translateY(-2px);
}

.v-timeline-item {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive */
@media (max-width: 960px) {
  .sticky-sidebar {
    position: relative;
    top: 0;
  }
  
  .curriculum-container {
    padding: 16px;
  }
}

/* Timeline custom styles */
.v-timeline {
  padding-left: 0;
}

.v-timeline-item {
  padding-bottom: 24px;
}

/* Custom chip styles */
.v-chip {
  margin: 2px;
  transition: transform 0.2s ease;
}

.v-chip:hover {
  transform: scale(1.05);
}

/* Progress bar animation */
.v-progress-linear {
  transition: all 0.8s ease;
}

/* File input custom styles */
.v-file-input {
  margin-bottom: 16px;
}

/* Dialog responsive */
@media (max-width: 600px) {
  .v-dialog {
    margin: 16px;
  }
  
  .v-dialog .v-card {
    margin: 0;
  }
}

/* Section navigation active state */
.v-list-item.bg-primary-lighten-5 {
  border-left: 4px solid rgb(var(--v-theme-primary));
  font-weight: 600;
}

/* Beautiful hover effects */
.v-btn {
  transition: all 0.3s ease;
}

.v-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

/* Timeline dot animation */
.v-timeline-item .v-timeline-item__body {
  animation: slideInRight 0.6s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Card hover effect */
.v-card {
  overflow: hidden;
  position: relative;
}

.v-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.v-card:hover::before {
  left: 100%;
}

/* Smooth scrolling for section navigation */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar for timeline */
.v-timeline::-webkit-scrollbar {
  width: 4px;
}

.v-timeline::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.v-timeline::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.3);
  border-radius: 4px;
}

.v-timeline::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.5);
}
</style><template>
  <v-container class="curriculum-container">
    <!-- Header -->
    <v-row class="mb-6">
      <v-col cols="12">
        <div class="d-flex align-center justify-space-between">
          <div>
            <h1 class="text-h3 font-weight-bold text-primary mb-2">
              Mi Currículum
            </h1>
            <p class="text-h6 text-grey-darken-1">
              Gestiona tu información profesional y mantén tu perfil actualizado
            </p>
          </div>
          
          <v-btn
            color="primary"
            size="large"
            @click="previewCV"
            prepend-icon="mdi-eye"
            class="ml-4"
          >
            Vista Previa
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <!-- Progreso del perfil -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="pa-4" rounded="lg" elevation="2">
          <v-card-title class="text-h6 mb-3">
            <v-icon color="success" class="mr-2">mdi-chart-line</v-icon>
            Completitud del Perfil
          </v-card-title>
          
          <v-progress-linear
            :model-value="profileCompleteness"
            color="success"
            height="12"
            rounded
            class="mb-2"
          ></v-progress-linear>
          
          <div class="d-flex justify-space-between">
            <span class="text-body-2">{{ profileCompleteness }}% completo</span>
            <span class="text-body-2 font-weight-bold">
              {{ getProfileStatus() }}
            </span>
          </div>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <!-- Sidebar con navegación -->
      <v-col cols="12" md="3">
        <v-card rounded="lg" elevation="2" class="sticky-sidebar">
          <v-card-title class="text-h6 pa-4">
            <v-icon color="primary" class="mr-2">mdi-format-list-bulleted</v-icon>
            Secciones
          </v-card-title>
          
          <v-list>
            <v-list-item
              v-for="section in sections"
              :key="section.id"
              @click="activeSection = section.id"
              :class="{ 'bg-primary-lighten-5': activeSection === section.id }"
              rounded="lg"
              class="ma-2"
            >
              <template v-slot:prepend>
                <v-icon :color="section.completed ? 'success' : 'grey'">
                  {{ section.icon }}
                </v-icon>
              </template>
              
              <v-list-item-title>{{ section.title }}</v-list-item-title>
              
              <template v-slot:append>
                <v-icon v-if="section.completed" color="success" size="small">
                  mdi-check-circle
                </v-icon>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <!-- Contenido principal -->
      <v-col cols="12" md="9">
        <!-- Información Personal -->
        <v-card v-if="activeSection === 'personal'" class="mb-6" rounded="lg" elevation="2">
          <v-card-title class="text-h5 pa-6 bg-primary-lighten-5">
            <v-icon color="primary" class="mr-3">mdi-account</v-icon>
            Información Personal
          </v-card-title>
          
          <v-card-text class="pa-6">
            <v-form ref="personalForm">
              <v-row>