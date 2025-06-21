<template>
  <v-container fluid class="job-search-container">
    <!-- Hero Section -->
    <v-row class="hero-section mb-8">
      <v-col cols="12">
        <div class="text-center py-12">
          <h1 class="text-h2 font-weight-bold text-white mb-4">
            Encuentra tu trabajo ideal
          </h1>
          <p class="text-h6 text-white mb-8 opacity-90">
            Más de {{ totalJobs.toLocaleString() }} oportunidades te esperan
          </p>
          
          <!-- Buscador principal -->
          <v-card
            class="mx-auto search-card"
            max-width="800"
            elevation="8"
          >
            <v-card-text class="pa-6">
              <v-form @submit.prevent="performSearch">
                <v-row align="center">
                  <v-col cols="12" md="4">
                    <v-text-field
                      v-model="searchQuery.keywords"
                      placeholder="¿Qué trabajo buscas?"
                      variant="outlined"
                      prepend-inner-icon="mdi-magnify"
                      hide-details
                      class="search-input"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="3">
                    <v-text-field
                      v-model="searchQuery.location"
                      placeholder="Ubicación"
                      variant="outlined"
                      prepend-inner-icon="mdi-map-marker"
                      hide-details
                      class="search-input"
                    ></v-text-field>
                  </v-col>
                  
                  <v-col cols="12" md="3">
                    <v-select
                      v-model="searchQuery.category"
                      :items="categories"
                      placeholder="Categoría"
                      variant="outlined"
                      prepend-inner-icon="mdi-tag"
                      hide-details
                      clearable
                      class="search-input"
                    ></v-select>
                  </v-col>
                  
                  <v-col cols="12" md="2">
                    <v-btn
                      type="submit"
                      color="primary"
                      size="large"
                      block
                      :loading="searching"
                      class="search-btn"
                    >
                      <v-icon left>mdi-magnify</v-icon>
                      Buscar
                    </v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-card-text>
          </v-card>
          
          <!-- Filtros rápidos -->
          <div class="quick-filters mt-6">
            <v-chip-group
              v-model="selectedQuickFilter"
              column
              @update:modelValue="applyQuickFilter"
            >
              <v-chip
                v-for="filter in quickFilters"
                :key="filter.value"
                :value="filter.value"
                color="white"
                variant="outlined"
                class="ma-1"
              >
                <v-icon left>{{ filter.icon }}</v-icon>
                {{ filter.label }}
              </v-chip>
            </v-chip-group>
          </div>
        </div>
      </v-col>
    </v-row>

    <!-- Filtros avanzados -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-expansion-panels v-model="filtersExpanded">
          <v-expansion-panel>
            <v-expansion-panel-title>
              <div class="d-flex align-center">
                <v-icon class="mr-3">mdi-filter-variant</v-icon>
                Filtros Avanzados
                <v-chip
                  v-if="activeFiltersCount > 0"
                  color="primary"
                  size="small"
                  class="ml-3"
                >
                  {{ activeFiltersCount }}
                </v-chip>
              </div>
            </v-expansion-panel-title>
            
            <v-expansion-panel-text>
              <v-card flat>
                <v-card-text>
                  <v-row>
                    <!-- Salario -->
                    <v-col cols="12" md="3">
                      <h4 class="text-subtitle-1 mb-3">Rango Salarial</h4>
                      <v-range-slider
                        v-model="filters.salaryRange"
                        :min="500"
                        :max="10000"
                        :step="100"
                        thumb-label="always"
                        color="primary"
                        class="mb-4"
                      >
                        <template v-slot:thumb-label="{ modelValue }">
                          S/{{ modelValue.toLocaleString() }}
                        </template>
                      </v-range-slider>
                      <div class="d-flex justify-space-between text-caption">
                        <span>S/{{ filters.salaryRange[0].toLocaleString() }}</span>
                        <span>S/{{ filters.salaryRange[1].toLocaleString() }}</span>
                      </div>
                    </v-col>
                    
                    <!-- Tipo de contrato -->
                    <v-col cols="12" md="3">
                      <h4 class="text-subtitle-1 mb-3">Tipo de Contrato</h4>
                      <v-checkbox-group v-model="filters.contractTypes">
                        <v-checkbox
                          v-for="type in contractTypes"
                          :key="type.value"
                          :value="type.value"
                          :label="type.label"
                          density="compact"
                        ></v-checkbox>
                      </v-checkbox-group>
                    </v-col>
                    
                    <!-- Modalidad de trabajo -->
                    <v-col cols="12" md="3">
                      <h4 class="text-subtitle-1 mb-3">Modalidad</h4>
                      <v-checkbox-group v-model="filters.workModes">
                        <v-checkbox
                          v-for="mode in workModes"
                          :key="mode.value"
                          :value="mode.value"
                          :label="mode.label"
                          density="compact"
                        ></v-checkbox>
                      </v-checkbox-group>
                    </v-col>
                    
                    <!-- Experiencia -->
                    <v-col cols="12" md="3">
                      <h4 class="text-subtitle-1 mb-3">Experiencia</h4>
                      <v-select
                        v-model="filters.experience"
                        :items="experienceLevels"
                        variant="outlined"
                        multiple
                        chips
                        closable-chips
                        density="compact"
                      ></v-select>
                    </v-col>
                  </v-row>
                  
                  <v-row class="mt-4">
                    <!-- Fecha de publicación -->
                    <v-col cols="12" md="4">
                      <h4 class="text-subtitle-1 mb-3">Fecha de Publicación</h4>
                      <v-select
                        v-model="filters.datePosted"
                        :items="dateOptions"
                        variant="outlined"
                        density="compact"
                      ></v-select>
                    </v-col>
                    
                    <!-- Tamaño de empresa -->
                    <v-col cols="12" md="4">
                      <h4 class="text-subtitle-1 mb-3">Tamaño de Empresa</h4>
                      <v-select
                        v-model="filters.companySize"
                        :items="companySizes"
                        variant="outlined"
                        multiple
                        chips
                        closable-chips
                        density="compact"
                      ></v-select>
                    </v-col>
                    
                    <!-- Ordenar por -->
                    <v-col cols="12" md="4">
                      <h4 class="text-subtitle-1 mb-3">Ordenar por</h4>
                      <v-select
                        v-model="filters.sortBy"
                        :items="sortOptions"
                        variant="outlined"
                        density="compact"
                      ></v-select>
                    </v-col>
                  </v-row>
                  
                  <!-- Botones de acción -->
                  <v-row class="mt-4">
                    <v-col cols="12" class="d-flex justify-end">
                      <v-btn
                        variant="text"
                        @click="clearFilters"
                        class="mr-3"
                      >
                        Limpiar Filtros
                      </v-btn>
                      <v-btn
                        color="primary"
                        @click="applyFilters"
                        :loading="searching"
                      >
                        Aplicar Filtros
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-card-text>
              </v-card>
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-col>
    </v-row>

    <!-- Resultados -->
    <v-row>
      <!-- Sidebar con filtros rápidos -->
      <v-col cols="12" md="3" class="d-none d-md-block">
        <v-card class="sticky-sidebar" elevation="2">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-filter</v-icon>
            Filtros Rápidos
          </v-card-title>
          
          <v-card-text>
            <!-- Guardar búsqueda -->
            <div class="mb-6">
              <v-btn
                color="primary"
                variant="outlined"
                block
                @click="saveSearch"
                prepend-icon="mdi-heart"
              >
                Guardar Búsqueda
              </v-btn>
            </div>
            
            <!-- Categorías populares -->
            <div class="mb-6">
              <h4 class="text-subtitle-1 mb-3">Categorías Populares</h4>
              <v-list density="compact">
                <v-list-item
                  v-for="category in popularCategories"
                  :key="category.name"
                  @click="selectCategory(category)"
                  class="px-0"
                >
                  <v-list-item-title class="text-body-2">
                    {{ category.name }}
                  </v-list-item-title>
                  <template v-slot:append>
                    <v-chip size="small" color="grey">
                      {{ category.count }}
                    </v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </div>
            
            <!-- Empresas destacadas -->
            <div class="mb-6">
              <h4 class="text-subtitle-1 mb-3">Empresas Destacadas</h4>
              <div class="d-flex flex-wrap">
                <v-chip
                  v-for="company in featuredCompanies"
                  :key="company"
                  size="small"
                  class="ma-1"
                  variant="outlined"
                  @click="searchByCompany(company)"
                >
                  {{ company }}
                </v-chip>
              </div>
            </div>
            
            <!-- Alertas de trabajo -->
            <div>
              <h4 class="text-subtitle-1 mb-3">Alertas de Trabajo</h4>
              <p class="text-body-2 text-grey mb-3">
                Recibe notificaciones de nuevas ofertas
              </p>
              <v-btn
                color="secondary"
                variant="outlined"
                block
                @click="createJobAlert"
                prepend-icon="mdi-bell"
              >
                Crear Alerta
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Lista de resultados -->
      <v-col cols="12" md="9">
        <!-- Header de resultados -->
        <div class="d-flex align-center justify-space-between mb-4">
          <div>
            <h2 class="text-h5">
              {{ filteredJobs.length }} ofertas encontradas
            </h2>
            <p class="text-body-2 text-grey" v-if="searchQuery.keywords">
              Resultados para "{{ searchQuery.keywords }}"
            </p>
          </div>
          
          <div class="d-flex align-center">
            <!-- Vista -->
            <v-btn-toggle v-model="viewMode" mandatory class="mr-3">
              <v-btn value="list" icon>
                <v-icon>mdi-view-list</v-icon>
              </v-btn>
              <v-btn value="grid" icon>
                <v-icon>mdi-view-grid</v-icon>
              </v-btn>
            </v-btn-toggle>
            
            <!-- Ordenamiento rápido -->
            <v-select
              v-model="quickSort"
              :items="quickSortOptions"
              variant="outlined"
              density="compact"
              hide-details
              style="width: 180px;"
              @update:modelValue="sortJobs"
            ></v-select>
          </div>
        </div>
        
        <!-- Loading state -->
        <div v-if="searching" class="text-center py-8">
          <v-progress-circular
            indeterminate
            color="primary"
            size="64"
          ></v-progress-circular>
          <p class="text-h6 mt-4">Buscando ofertas...</p>
        </div>
        
        <!-- Lista de ofertas -->
        <div v-else>
          <!-- Vista de lista -->
          <template v-if="viewMode === 'list'">
            <v-card
              v-for="job in paginatedJobs"
              :key="job.id"
              class="mb-4 job-card"
              elevation="2"
              hover
              @click="viewJobDetails(job)"
            >
              <v-card-text class="pa-6">
                <v-row>
                  <v-col cols="12" md="8">
                    <div class="d-flex align-start">
                      <v-avatar
                        size="48"
                        class="mr-4"
                        :color="job.company.color"
                      >
                        <v-icon color="white">{{ job.company.icon }}</v-icon>
                      </v-avatar>
                      
                      <div class="flex-grow-1">
                        <h3 class="text-h6 mb-1">{{ job.title }}</h3>
                        <p class="text-subtitle-1 text-primary mb-2">
                          {{ job.company.name }}
                        </p>
                        
                        <div class="d-flex align-center mb-3">
                          <v-icon size="16" class="mr-1">mdi-map-marker</v-icon>
                          <span class="text-body-2 mr-4">{{ job.location }}</span>
                          
                          <v-icon size="16" class="mr-1">mdi-briefcase</v-icon>
                          <span class="text-body-2 mr-4">{{ job.type }}</span>
                          
                          <v-icon size="16" class="mr-1">mdi-clock</v-icon>
                          <span class="text-body-2">{{ formatDate(job.postedDate) }}</span>
                        </div>
                        
                        <p class="text-body-2 text-grey job-description">
                          {{ job.description }}
                        </p>
                        
                        <div class="d-flex flex-wrap mt-3">
                          <v-chip
                            v-for="skill in job.skills.slice(0, 3)"
                            :key="skill"
                            size="small"
                            color="primary"
                            variant="outlined"
                            class="mr-2 mb-1"
                          >
                            {{ skill }}
                          </v-chip>
                          <v-chip
                            v-if="job.skills.length > 3"
                            size="small"
                            color="grey"
                            variant="outlined"
                            class="mr-2 mb-1"
                          >
                            +{{ job.skills.length - 3 }} más
                          </v-chip>
                        </div>
                      </div>
                    </div>
                  </v-col>
                  
                  <v-col cols="12" md="4" class="d-flex flex-column justify-space-between">
                    <div class="text-right">
                      <div class="text-h6 text-success mb-2">
                        {{ job.salary }}
                      </div>
                      <v-chip
                        :color="getStatusColor(job.urgency)"
                        size="small"
                        class="mb-3"
                      >
                        {{ job.urgency }}
                      </v-chip>
                    </div>
                    
                    <div class="d-flex flex-column">
                      <v-btn
                        color="primary"
                        @click.stop="applyToJob(job)"
                        :loading="job.applying"
                        class="mb-2"
                      >
                        <v-icon left>mdi-send</v-icon>
                        Postular
                      </v-btn>
                      
                      <div class="d-flex">
                        <v-btn
                          icon
                          variant="text"
                          @click.stop="saveJob(job)"
                          :color="job.saved ? 'error' : 'grey'"
                        >
                          <v-icon>{{ job.saved ? 'mdi-heart' : 'mdi-heart-outline' }}</v-icon>
                        </v-btn>
                        
                        <v-btn
                          icon
                          variant="text"
                          @click.stop="shareJob(job)"
                        >
                          <v-icon>mdi-share-variant</v-icon>
                        </v-btn>
                      </div>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </template>
          
          <!-- Vista de grilla -->
          <template v-else>
            <v-row>
              <v-col
                v-for="job in paginatedJobs"
                :key="job.id"
                cols="12"
                md="6"
                lg="4"
              >
                <v-card
                  class="job-card-grid"
                  elevation="2"
                  hover
                  @click="viewJobDetails(job)"
                >
                  <v-card-text class="pa-4">
                    <div class="d-flex align-center mb-3">
                      <v-avatar
                        size="32"
                        :color="job.company.color"
                        class="mr-3"
                      >
                        <v-icon size="16" color="white">{{ job.company.icon }}</v-icon>
                      </v-avatar>
                      <div>
                        <h4 class="text-subtitle-1">{{ job.title }}</h4>
                        <p class="text-body-2 text-primary">{{ job.company.name }}</p>
                      </div>
                    </div>
                    
                    <div class="mb-3">
                      <div class="d-flex align-center mb-1">
                        <v-icon size="14" class="mr-1">mdi-map-marker</v-icon>
                        <span class="text-caption">{{ job.location }}</span>
                      </div>
                      <div class="d-flex align-center">
                        <v-icon size="14" class="mr-1">mdi-briefcase</v-icon>
                        <span class="text-caption">{{ job.type }}</span>
                      </div>
                    </div>
                    
                    <p class="text-body-2 text-grey job-description-grid">
                      {{ job.description }}
                    </p>
                    
                    <div class="text-h6 text-success mb-3">
                      {{ job.salary }}
                    </div>
                    
                    <v-btn
                      color="primary"
                      size="small"
                      block
                      @click.stop="applyToJob(job)"
                      :loading="job.applying"
                    >
                      Postular
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </template>
          
          <!-- Paginación -->
          <div v-if="totalPages > 1" class="d-flex justify-center mt-6">
            <v-pagination
              v-model="currentPage"
              :length="totalPages"
              :total-visible="7"
              @update:modelValue="scrollToTop"
            ></v-pagination>
          </div>
          
          <!-- Estado vacío -->
          <div v-if="filteredJobs.length === 0" class="text-center py-12">
            <v-icon size="72" color="grey">mdi-briefcase-search</v-icon>
            <h3 class="text-h5 mt-4 mb-2">No se encontraron ofertas</h3>
            <p class="text-body-1 text-grey mb-4">
              Intenta ajustar tus filtros de búsqueda
            </p>
            <v-btn color="primary" @click="clearFilters">
              Limpiar Filtros
            </v-btn>
          </div>
        </div>
      </v-col>
    </v-row>
    
    <!-- Dialog de detalles del trabajo -->
    <v-dialog
      v-model="jobDetailDialog"
      max-width="800"
      scrollable
    >
      <v-card v-if="selectedJob">
        <v-card-title class="d-flex align-center">
          <div class="flex-grow-1">
            <h2 class="text-h5">{{ selectedJob.title }}</h2>
            <p class="text-subtitle-1 text-primary">{{ selectedJob.company.name }}</p>
          </div>
          <v-btn
            icon
            @click="jobDetailDialog = false"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>
        
        <v-card-text>
          <div class="mb-4">
            <div class="d-flex align-center mb-2">
              <v-icon class="mr-2">mdi-map-marker</v-icon>
              {{ selectedJob.location }}
            </div>
            <div class="d-flex align-center mb-2">
              <v-icon class="mr-2">mdi-briefcase</v-icon>
              {{ selectedJob.type }}
            </div>
            <div class="d-flex align-center mb-2">
              <v-icon class="mr-2">mdi-currency-usd</v-icon>
              {{ selectedJob.salary }}
            </div>
          </div>
          
          <v-divider class="my-4"></v-divider>
          
          <h3 class="text-h6 mb-3">Descripción del puesto</h3>
          <p class="text-body-1 mb-4">{{ selectedJob.fullDescription }}</p>
          
          <h3 class="text-h6 mb-3">Habilidades requeridas</h3>
          <div class="d-flex flex-wrap mb-4">
            <v-chip
              v-for="skill in selectedJob.skills"
              :key="skill"
              color="primary"
              variant="outlined"
              class="mr-2 mb-2"
            >
              {{ skill }}
            </v-chip>
          </div>
          
          <h3 class="text-h6 mb-3">Beneficios</h3>
          <v-list density="compact">
            <v-list-item
              v-for="benefit in selectedJob.benefits"
              :key="benefit"
            >
              <template v-slot:prepend>
                <v-icon color="success">mdi-check</v-icon>
              </template>
              <v-list-item-title>{{ benefit }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-card-text>
        
        <v-card-actions class="pa-4">
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            size="large"
            @click="applyToJob(selectedJob)"
            :loading="selectedJob.applying"
          >
            <v-icon left>mdi-send</v-icon>
            Postular a este trabajo
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Estados reactivos
const searching = ref(false)
const filtersExpanded = ref(null)
const viewMode = ref('list')
const currentPage = ref(1)
const itemsPerPage = ref(10)
const jobDetailDialog = ref(false)
const selectedJob = ref(null)
const selectedQuickFilter = ref(null)

// Datos de búsqueda
const searchQuery = ref({
  keywords: '',
  location: '',
  category: null
})

// Filtros
const filters = ref({
  salaryRange: [1000, 5000],
  contractTypes: [],
  workModes: [],
  experience: [],
  datePosted: 'Cualquier momento',
  companySize: [],
  sortBy: 'Relevancia'
})

// Opciones
const categories = [
  'Desarrollo de Software',
  'Marketing Digital', 
  'Diseño Gráfico',
  'Ventas',
  'Recursos Humanos',
  'Finanzas',
  'Ingeniería',
  'Educación'
]

const contractTypes = [
  { label: 'Tiempo Completo', value: 'full-time' },
  { label: 'Medio Tiempo', value: 'part-time' },
  { label: 'Por Contrato', value: 'contract' },
  { label: 'Freelance', value: 'freelance' },
  { label: 'Pasantía', value: 'internship' }
]

const workModes = [
  { label: 'Presencial', value: 'on-site' },
  { label: 'Remoto', value: 'remote' },
  { label: 'Híbrido', value: 'hybrid' }
]

const experienceLevels = [
  'Sin experiencia',
  '1-2 años',
  '3-5 años',
  '5-10 años',
  'Más de 10 años'
]

const dateOptions = [
  'Cualquier momento',
  'Última semana',
  'Último mes',
  'Últimos 3 meses'
]

const companySizes = [
  'Startup (1-10)',
  'Pequeña (11-50)', 
  'Mediana (51-200)',
  'Grande (201-1000)',
  'Corporación (1000+)'
]

const sortOptions = [
  'Relevancia',
  'Más recientes',
  'Salario (mayor a menor)',
  'Salario (menor a mayor)',
  'Alfabético'
]

const quickSortOptions = [
  { title: 'Relevancia', value: 'relevance' },
  { title: 'Más recientes', value: 'newest' },
  { title: 'Salario ↓', value: 'salary-desc' },
  { title: 'Salario ↑', value: 'salary-asc' }
]

const quickSort = ref('relevance')

// Filtros rápidos
const quickFilters = [
  { label: 'Remoto', value: 'remote', icon: 'mdi-home' },
  { label: 'Tiempo Completo', value: 'full-time', icon: 'mdi-clock' },
  { label: 'Sin Experiencia', value: 'entry-level', icon: 'mdi-school' },
  { label: 'Startups', value: 'startup', icon: 'mdi-rocket' }
]

// Datos mock
const totalJobs = ref(15247)

const jobs = ref([
  {
    id: 1,
    title: 'Desarrollador Frontend React',
    company: {
      name: 'TechCorp Solutions',
      color: 'primary',
      icon: 'mdi-react'
    },
    location: 'Arequipa, Perú',
    type: 'Tiempo Completo',
    salary: 'S/ 3,500 - 5,000',
    urgency: 'Urgente',
    description: 'Buscamos desarrollador Frontend con experiencia en React, TypeScript y metodologías ágiles...',
    fullDescription: 'Estamos buscando un Desarrollador Frontend especializado en React para unirse a nuestro equipo dinámico. El candidato ideal tendrá experiencia sólida en el desarrollo de aplicaciones web modernas utilizando React, TypeScript, y las mejores prácticas de desarrollo.',
    skills: ['React', 'TypeScript', 'JavaScript', 'CSS3', 'HTML5', 'Git'],
    benefits: ['Seguro médico', 'Trabajo remoto', 'Capacitaciones', 'Bonos por rendimiento'],
    postedDate: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    saved: false,
    applying: false
  },
  {
    id: 2,
    title: 'Diseñador UX/UI Senior',
    company: {
      name: 'Design Studio',
      color: 'purple',
      icon: 'mdi-palette'
    },
    location: 'Lima, Perú',
    type: 'Tiempo Completo',
    salary: 'S/ 4,000 - 6,500',
    urgency: 'Normal',
    description: 'Posición para diseñador UX/UI con portfolio sólido y experiencia en productos digitales...',
    fullDescription: 'Buscamos un Diseñador UX/UI Senior para liderar el diseño de experiencias digitales excepcionales. Trabajarás en proyectos innovadores con clientes de primer nivel.',
    skills: ['Figma', 'Sketch', 'Adobe XD', 'Prototyping', 'User Research', 'Design Systems'],
    benefits: ['Horario flexible', 'Equipo de última generación', 'Días libres adicionales'],
    postedDate: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    saved: true,
    applying: false
  },
  {
    id: 3,
    title: 'Backend Developer Node.js',
    company: {
      name: 'StartupTech',
      color: 'green',
      icon: 'mdi-server'
    },
    location: 'Cusco, Perú',
    type: 'Tiempo Completo',
    salary: 'S/ 3,000 - 4,500',
    urgency: 'Normal',
    description: 'Desarrollador Backend para APIs REST, microservicios y bases de datos...',
    fullDescription: 'Únete a nuestro equipo como Desarrollador Backend especializado en Node.js. Trabajarás en la construcción de APIs robustas y escalables.',
    skills: ['Node.js', 'Express', 'MongoDB', 'PostgreSQL', 'Docker', 'AWS'],
    benefits: ['Stock options', 'Ambiente startup', 'Crecimiento acelerado'],
    postedDate: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    saved: false,
    applying: false
  },
  {
    id: 4,
    title: 'Marketing Digital Specialist',
    company: {
      name: 'AgencyPro',
      color: 'orange',
      icon: 'mdi-bullhorn'
    },
    location: 'Arequipa, Perú',
    type: 'Medio Tiempo',
    salary: 'S/ 2,000 - 3,000',
    urgency: 'Normal',
    description: 'Especialista en marketing digital para campañas SEM, SEO y social media...',
    fullDescription: 'Buscamos un especialista en marketing digital para gestionar campañas integrales y estrategias de crecimiento digital.',
    skills: ['Google Ads', 'Facebook Ads', 'SEO', 'Analytics', 'Content Marketing'],
    benefits: ['Comisiones por resultados', 'Capacitación constante', 'Trabajo híbrido'],
    postedDate: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
    saved: false,
    applying: false
  }
])

const popularCategories = ref([
  { name: 'Desarrollo de Software', count: 234 },
  { name: 'Marketing Digital', count: 156 },
  { name: 'Diseño Gráfico', count: 89 },
  { name: 'Ventas', count: 167 },
  { name: 'Recursos Humanos', count: 45 }
])

const featuredCompanies = ref([
  'Google', 'Microsoft', 'Amazon', 'TechCorp', 'InnovaTech', 'StartupPro'
])

// Computadas
const activeFiltersCount = computed(() => {
  let count = 0
  if (filters.value.salaryRange[0] !== 1000 || filters.value.salaryRange[1] !== 5000) count++
  if (filters.value.contractTypes.length > 0) count++
  if (filters.value.workModes.length > 0) count++
  if (filters.value.experience.length > 0) count++
  if (filters.value.datePosted !== 'Cualquier momento') count++
  if (filters.value.companySize.length > 0) count++
  if (filters.value.sortBy !== 'Relevancia') count++
  return count
})

const filteredJobs = computed(() => {
  let filtered = [...jobs.value]
  
  // Filtrar por palabras clave
  if (searchQuery.value.keywords) {
    const keywords = searchQuery.value.keywords.toLowerCase()
    filtered = filtered.filter(job => 
      job.title.toLowerCase().includes(keywords) ||
      job.description.toLowerCase().includes(keywords) ||
      job.skills.some(skill => skill.toLowerCase().includes(keywords))
    )
  }
  
  // Filtrar por ubicación
  if (searchQuery.value.location) {
    const location = searchQuery.value.location.toLowerCase()
    filtered = filtered.filter(job => 
      job.location.toLowerCase().includes(location)
    )
  }
  
  // Filtrar por categoría
  if (searchQuery.value.category) {
    // Lógica de filtrado por categoría
    filtered = filtered.filter(job => 
      job.category === searchQuery.value.category
    )
  }
  
  // Aplicar filtros avanzados
  if (filters.value.contractTypes.length > 0) {
    filtered = filtered.filter(job => 
      filters.value.contractTypes.some(type => 
        job.type.toLowerCase().includes(type.replace('-', ' '))
      )
    )
  }
  
  if (filters.value.workModes.length > 0) {
    filtered = filtered.filter(job => 
      filters.value.workModes.some(mode => 
        job.workMode === mode
      )
    )
  }
  
  return filtered
})

const paginatedJobs = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredJobs.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredJobs.value.length / itemsPerPage.value)
})

// Métodos
const performSearch = async () => {
  searching.value = true
  // Simular búsqueda
  await new Promise(resolve => setTimeout(resolve, 1500))
  searching.value = false
  currentPage.value = 1
}

const applyQuickFilter = (filterValue) => {
  if (!filterValue) return
  
  switch (filterValue) {
    case 'remote':
      filters.value.workModes = ['remote']
      break
    case 'full-time':
      filters.value.contractTypes = ['full-time']
      break
    case 'entry-level':
      filters.value.experience = ['Sin experiencia']
      break
    case 'startup':
      filters.value.companySize = ['Startup (1-10)']
      break
  }
  
  applyFilters()
}

const applyFilters = async () => {
  searching.value = true
  await new Promise(resolve => setTimeout(resolve, 1000))
  searching.value = false
  currentPage.value = 1
}

const clearFilters = () => {
  searchQuery.value = {
    keywords: '',
    location: '',
    category: null
  }
  
  filters.value = {
    salaryRange: [1000, 5000],
    contractTypes: [],
    workModes: [],
    experience: [],
    datePosted: 'Cualquier momento',
    companySize: [],
    sortBy: 'Relevancia'
  }
  
  selectedQuickFilter.value = null
  currentPage.value = 1
}

const sortJobs = (sortValue) => {
  // Implementar lógica de ordenamiento
  console.log(`Ordenando por: ${sortValue}`)
}

const viewJobDetails = (job) => {
  selectedJob.value = job
  jobDetailDialog.value = true
}

const applyToJob = async (job) => {
  job.applying = true
  // Simular aplicación
  await new Promise(resolve => setTimeout(resolve, 2000))
  job.applying = false
  window.showSnackbar(`Postulación enviada para: ${job.title}`, 'success')
}

const saveJob = (job) => {
  job.saved = !job.saved
  const message = job.saved ? 'Trabajo guardado' : 'Trabajo removido de guardados'
  window.showSnackbar(message, job.saved ? 'success' : 'info')
}

const shareJob = (job) => {
  // Simular compartir
  if (navigator.share) {
    navigator.share({
      title: job.title,
      text: `Mira esta oferta: ${job.title} en ${job.company.name}`,
      url: window.location.href
    })
  } else {
    // Fallback para navegadores que no soportan Web Share API
    navigator.clipboard.writeText(window.location.href)
    window.showSnackbar('Enlace copiado al portapapeles', 'info')
  }
}

const selectCategory = (category) => {
  searchQuery.value.category = category.name
  performSearch()
}

const searchByCompany = (company) => {
  searchQuery.value.keywords = company
  performSearch()
}

const saveSearch = () => {
  // Implementar guardar búsqueda
  window.showSnackbar('Búsqueda guardada exitosamente', 'success')
}

const createJobAlert = () => {
  // Implementar crear alerta
  window.showSnackbar('Alerta de trabajo creada', 'success')
}

const getStatusColor = (urgency) => {
  switch (urgency) {
    case 'Urgente': return 'error'
    case 'Normal': return 'primary'
    default: return 'grey'
  }
}

const formatDate = (date) => {
  const now = new Date()
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return 'Hace 1 día'
  if (diffDays < 7) return `Hace ${diffDays} días`
  if (diffDays < 30) return `Hace ${Math.ceil(diffDays / 7)} semanas`
  return `Hace ${Math.ceil(diffDays / 30)} meses`
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Lifecycle
onMounted(() => {
  // Simular carga inicial
  searching.value = true
  setTimeout(() => {
    searching.value = false
  }, 1000)
})

// Watchers
watch(() => searchQuery.value.keywords, (newVal) => {
  if (newVal.length > 2) {
    // Auto-búsqueda después de 3 caracteres
    setTimeout(() => {
      if (searchQuery.value.keywords === newVal) {
        performSearch()
      }
    }, 500)
  }
})
</script>

<style scoped>
.job-search-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: -24px -24px 0 -24px;
  padding: 0 24px;
}

.search-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
}

.search-input {
  background: white;
  border-radius: 8px;
}

.search-btn {
  height: 56px;
  border-radius: 8px;
}

.quick-filters {
  max-width: 800px;
  margin: 0 auto;
}

.job-card {
  transition: all 0.3s ease;
  cursor: pointer;
  border-radius: 12px;
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.job-card-grid {
  transition: all 0.3s ease;
  cursor: pointer;
  border-radius: 12px;
  height: 100%;
}

.job-card-grid:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

.job-description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.job-description-grid {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  min-height: 60px;
}

.sticky-sidebar {
  position: sticky;
  top: 24px;
  height: fit-content;
}

/* Animaciones */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.job-card, .job-card-grid {
  animation: fadeInUp 0.6s ease-out;
}

/* Responsive */
@media (max-width: 960px) {
  .hero-section {
    padding: 0 16px;
  }
  
  .search-card {
    margin: 0 16px;
  }
  
  .job-search-container {
    padding: 16px;
  }
}

/* Dark mode support */
.v-theme--dark .search-card {
  background: rgba(30, 30, 30, 0.95);
}

.v-theme--dark .job-card,
.v-theme--dark .job-card-grid {
  border: 1px solid rgba(255,255,255,0.1);
}

/* Scrollbar personalizado */
.v-dialog .v-card-text::-webkit-scrollbar {
  width: 6px;
}

.v-dialog .v-card-text::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.1);
  border-radius: 3px;
}

.v-dialog .v-card-text::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.5);
  border-radius: 3px;
}

.v-dialog .v-card-text::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.7);
}

/* Efectos adicionales */
.v-chip:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

.v-btn:not(.v-btn--disabled):hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

/* Mejoras para la vista de grilla */
.job-card-grid .v-card-text {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.job-card-grid .v-btn {
  margin-top: auto;
}

/* Efectos para los filtros */
.v-expansion-panel-title:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

/* Estilos para el range slider */
.v-slider {
  margin: 8px 0;
}

/* Mejoras para la paginación */
.v-pagination {
  margin: 20px 0;
}

/* Efectos para las cards del sidebar */
.sticky-sidebar .v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  border-radius: 8px;
  transition: all 0.2s ease;
}

/* Estados de carga mejorados */
.v-progress-circular {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}
</style>