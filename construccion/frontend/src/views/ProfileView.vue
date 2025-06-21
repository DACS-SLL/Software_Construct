<template>
  <v-container fluid class="profile-container">
    <!-- Header del perfil -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card class="profile-header" elevation="4">
          <div class="profile-banner">
            <v-img
              :src="profileData.bannerImage || '/api/placeholder/1200/300'"
              height="200"
              cover
              class="banner-image"
            >
              <div class="banner-overlay"></div>
            </v-img>
            
            <!-- Botón para cambiar banner -->
            <v-btn
              v-if="isOwnProfile"
              icon
              class="change-banner-btn"
              @click="changeBanner"
            >
              <v-icon>mdi-camera</v-icon>
            </v-btn>
          </div>
          
          <v-card-text class="profile-info pa-6">
            <v-row align="center">
              <v-col cols="auto">
                <div class="profile-avatar-container">
                  <v-avatar
                    size="120"
                    class="profile-avatar elevation-4"
                  >
                    <v-img
                      :src="profileData.avatar || '/api/placeholder/120/120'"
                      :alt="profileData.name"
                    ></v-img>
                  </v-avatar>
                  
                  <!-- Badge de verificación -->
                  <v-chip
                    v-if="profileData.verified"
                    color="success"
                    size="small"
                    class="verification-badge"
                  >
                    <v-icon left size="16">mdi-check-decagram</v-icon>
                    Verificado
                  </v-chip>
                  
                  <!-- Botón para cambiar avatar -->
                  <v-btn
                    v-if="isOwnProfile"
                    icon
                    size="small"
                    class="change-avatar-btn"
                    @click="changeAvatar"
                  >
                    <v-icon size="16">mdi-camera</v-icon>
                  </v-btn>
                </div>
              </v-col>
              
              <v-col>
                <div class="d-flex align-center mb-2">
                  <h1 class="text-h3 font-weight-bold mr-4">
                    {{ profileData.name }}
                  </h1>
                  
                  <!-- Estado de disponibilidad -->
                  <v-chip
                    :color="getAvailabilityColor(profileData.availability)"
                    variant="elevated"
                    class="mr-2"
                  >
                    <v-icon left>{{ getAvailabilityIcon(profileData.availability) }}</v-icon>
                    {{ profileData.availability }}
                  </v-chip>
                  
                  <!-- Rating -->
                  <div class="d-flex align-center">
                    <v-rating
                      :model-value="profileData.rating"
                      readonly
                      density="compact"
                      color="warning"
                      size="small"
                    ></v-rating>
                    <span class="text-body-2 ml-2">({{ profileData.reviews }} reseñas)</span>
                  </div>
                </div>
                
                <h2 class="text-h6 text-primary mb-2">{{ profileData.title }}</h2>
                
                <div class="d-flex flex-wrap align-center mb-3">
                  <div class="d-flex align-center mr-6 mb-2">
                    <v-icon class="mr-2">mdi-map-marker</v-icon>
                    <span>{{ profileData.location }}</span>
                  </div>
                  
                  <div class="d-flex align-center mr-6 mb-2">
                    <v-icon class="mr-2">mdi-email</v-icon>
                    <span>{{ profileData.email }}</span>
                  </div>
                  
                  <div class="d-flex align-center mr-6 mb-2">
                    <v-icon class="mr-2">mdi-phone</v-icon>
                    <span>{{ profileData.phone }}</span>
                  </div>
                  
                  <div class="d-flex align-center mb-2">
                    <v-icon class="mr-2">mdi-calendar</v-icon>
                    <span>{{ calculateAge(profileData.birthDate) }} años</span>
                  </div>
                </div>
                
                <p class="text-body-1 mb-4">{{ profileData.summary }}</p>
                
                <!-- Redes sociales -->
                <div class="d-flex flex-wrap">
                  <v-btn
                    v-for="social in profileData.socialLinks"
                    :key="social.platform"
                    :href="social.url"
                    target="_blank"
                    variant="outlined"
                    size="small"
                    class="mr-2 mb-2"
                  >
                    <v-icon left>{{ getSocialIcon(social.platform) }}</v-icon>
                    {{ social.platform }}
                  </v-btn>
                </div>
              </v-col>
              
              <v-col cols="auto" v-if="!isOwnProfile">
                <div class="d-flex flex-column">
                  <v-btn
                    color="primary"
                    size="large"
                    @click="contactCandidate"
                    class="mb-2"
                  >
                    <v-icon left>mdi-message</v-icon>
                    Contactar
                  </v-btn>
                  
                  <v-btn
                    color="success"
                    variant="outlined"
                    @click="scheduleInterview"
                    class="mb-2"
                  >
                    <v-icon left>mdi-calendar-plus</v-icon>
                    Agendar Entrevista
                  </v-btn>
                  
                  <v-btn
                    :color="profileData.bookmarked ? 'error' : 'grey'"
                    variant="outlined"
                    @click="toggleBookmark"
                  >
                    <v-icon left>
                      {{ profileData.bookmarked ? 'mdi-heart' : 'mdi-heart-outline' }}
                    </v-icon>
                    {{ profileData.bookmarked ? 'Guardado' : 'Guardar' }}
                  </v-btn>
                </div>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Navegación de secciones -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card elevation="2">
          <v-tabs
            v-model="activeTab"
            bg-color="transparent"
            color="primary"
            grow
          >
            <v-tab
              v-for="section in sections"
              :key="section.value"
              :value="section.value"
            >
              <v-icon left>{{ section.icon }}</v-icon>
              {{ section.title }}
            </v-tab>
          </v-tabs>
        </v-card>
      </v-col>
    </v-row>

    <!-- Contenido de las pestañas -->
    <v-row>
      <v-col cols="12" md="8">
        <!-- Resumen -->
        <v-card v-if="activeTab === 'overview'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-account</v-icon>
            Resumen Profesional
          </v-card-title>
          
          <v-card-text>
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Acerca de mí</h3>
              <p class="text-body-1">{{ profileData.about }}</p>
            </div>
            
            <!-- Habilidades destacadas -->
            <div class="mb-6">
              <h3 class="text-h6 mb-3">Habilidades Principales</h3>
              <div class="d-flex flex-wrap">
                <v-chip
                  v-for="skill in profileData.topSkills"
                  :key="skill.name"
                  :color="getSkillColor(skill.level)"
                  class="ma-1"
                  variant="elevated"
                >
                  {{ skill.name }}
                  <v-tooltip activator="parent" location="top">
                    Nivel: {{ skill.level }}/5
                  </v-tooltip>
                </v-chip>
              </div>
            </div>
            
            <!-- Logros destacados -->
            <div>
              <h3 class="text-h6 mb-3">Logros Destacados</h3>
              <v-list>
                <v-list-item
                  v-for="achievement in profileData.achievements"
                  :key="achievement.id"
                >
                  <template v-slot:prepend>
                    <v-icon color="warning">mdi-trophy</v-icon>
                  </template>
                  
                  <v-list-item-title>{{ achievement.title }}</v-list-item-title>
                  <v-list-item-subtitle>{{ achievement.description }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
        </v-card>
        
        <!-- Experiencia -->
        <v-card v-if="activeTab === 'experience'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-briefcase</v-icon>
            Experiencia Laboral
            <v-spacer></v-spacer>
            <v-btn
              v-if="isOwnProfile"
              color="primary"
              @click="addExperience"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-timeline side="end" align="start">
              <v-timeline-item
                v-for="(exp, index) in profileData.experience"
                :key="index"
                dot-color="primary"
                size="small"
              >
                <template v-slot:opposite>
                  <div class="text-caption text-grey">
                    {{ formatDate(exp.startDate) }} - 
                    {{ exp.current ? 'Actual' : formatDate(exp.endDate) }}
                  </div>
                </template>
                
                <v-card variant="outlined" class="mb-4">
                  <v-card-text>
                    <div class="d-flex align-center mb-2">
                      <v-avatar
                        size="32"
                        :color="exp.companyColor || 'primary'"
                        class="mr-3"
                      >
                        <v-icon color="white">{{ exp.companyIcon || 'mdi-domain' }}</v-icon>
                      </v-avatar>
                      
                      <div>
                        <h4 class="text-h6">{{ exp.position }}</h4>
                        <p class="text-subtitle-1 text-primary">{{ exp.company }}</p>
                      </div>
                      
                      <v-spacer></v-spacer>
                      
                      <v-btn
                        v-if="isOwnProfile"
                        icon
                        size="small"
                        @click="editExperience(exp, index)"
                      >
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                    </div>
                    
                    <p class="text-body-2 mb-3">{{ exp.description }}</p>
                    
                    <!-- Tecnologías usadas -->
                    <div v-if="exp.technologies" class="d-flex flex-wrap">
                      <v-chip
                        v-for="tech in exp.technologies"
                        :key="tech"
                        size="small"
                        color="secondary"
                        variant="outlined"
                        class="mr-1 mb-1"
                      >
                        {{ tech }}
                      </v-chip>
                    </div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
        
        <!-- Educación -->
        <v-card v-if="activeTab === 'education'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-school</v-icon>
            Educación
            <v-spacer></v-spacer>
            <v-btn
              v-if="isOwnProfile"
              color="primary"
              @click="addEducation"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-timeline side="end" align="start">
              <v-timeline-item
                v-for="(edu, index) in profileData.education"
                :key="index"
                dot-color="info"
                size="small"
              >
                <template v-slot:opposite>
                  <div class="text-caption text-grey">
                    {{ formatDate(edu.startDate) }} - 
                    {{ edu.current ? 'En curso' : formatDate(edu.endDate) }}
                  </div>
                </template>
                
                <v-card variant="outlined" class="mb-4">
                  <v-card-text>
                    <div class="d-flex align-center mb-2">
                      <v-avatar
                        size="32"
                        color="info"
                        class="mr-3"
                      >
                        <v-icon color="white">mdi-school</v-icon>
                      </v-avatar>
                      
                      <div>
                        <h4 class="text-h6">{{ edu.degree }}</h4>
                        <p class="text-subtitle-1 text-info">{{ edu.institution }}</p>
                      </div>
                      
                      <v-spacer></v-spacer>
                      
                      <v-btn
                        v-if="isOwnProfile"
                        icon
                        size="small"
                        @click="editEducation(edu, index)"
                      >
                        <v-icon>mdi-pencil</v-icon>
                      </v-btn>
                    </div>
                    
                    <p v-if="edu.description" class="text-body-2 mb-3">
                      {{ edu.description }}
                    </p>
                    
                    <div v-if="edu.grade" class="text-body-2">
                      <strong>Promedio:</strong> {{ edu.grade }}
                    </div>
                  </v-card-text>
                </v-card>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
        
        <!-- Habilidades -->
        <v-card v-if="activeTab === 'skills'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-star</v-icon>
            Habilidades y Competencias
            <v-spacer></v-spacer>
            <v-btn
              v-if="isOwnProfile"
              color="primary"
              @click="addSkill"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <!-- Habilidades técnicas -->
            <div class="mb-6">
              <h3 class="text-h6 mb-4">Habilidades Técnicas</h3>
              <v-row>
                <v-col
                  v-for="skill in profileData.technicalSkills"
                  :key="skill.name"
                  cols="12"
                  md="6"
                >
                  <div class="skill-item">
                    <div class="d-flex justify-space-between mb-2">
                      <span class="font-weight-medium">{{ skill.name }}</span>
                      <span class="text-caption">{{ skill.level }}/5</span>
                    </div>
                    <v-progress-linear
                      :model-value="(skill.level / 5) * 100"
                      :color="getSkillColor(skill.level)"
                      height="8"
                      rounded
                    ></v-progress-linear>
                  </div>
                </v-col>
              </v-row>
            </div>
            
            <!-- Habilidades blandas -->
            <div class="mb-6">
              <h3 class="text-h6 mb-4">Habilidades Blandas</h3>
              <div class="d-flex flex-wrap">
                <v-chip
                  v-for="skill in profileData.softSkills"
                  :key="skill"
                  color="secondary"
                  variant="elevated"
                  class="ma-1"
                >
                  {{ skill }}
                </v-chip>
              </div>
            </div>
            
            <!-- Idiomas -->
            <div>
              <h3 class="text-h6 mb-4">Idiomas</h3>
              <v-row>
                <v-col
                  v-for="language in profileData.languages"
                  :key="language.name"
                  cols="12"
                  md="4"
                >
                  <v-card variant="outlined" class="pa-3 text-center">
                    <v-icon size="32" color="primary" class="mb-2">mdi-translate</v-icon>
                    <h4 class="text-subtitle-1">{{ language.name }}</h4>
                    <p class="text-body-2 text-grey">{{ language.level }}</p>
                  </v-card>
                </v-col>
              </v-row>
            </div>
          </v-card-text>
        </v-card>
        
        <!-- Proyectos -->
        <v-card v-if="activeTab === 'projects'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-folder</v-icon>
            Proyectos
            <v-spacer></v-spacer>
            <v-btn
              v-if="isOwnProfile"
              color="primary"
              @click="addProject"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col
                v-for="project in profileData.projects"
                :key="project.id"
                cols="12"
                md="6"
              >
                <v-card variant="outlined" class="project-card" hover>
                  <v-img
                    :src="project.image || '/api/placeholder/400/200'"
                    height="200"
                    cover
                  >
                    <div class="project-overlay">
                      <v-btn
                        icon
                        color="white"
                        @click="viewProject(project)"
                      >
                        <v-icon>mdi-eye</v-icon>
                      </v-btn>
                      
                      <v-btn
                        v-if="project.liveUrl"
                        icon
                        color="white"
                        @click="openProject(project.liveUrl)"
                      >
                        <v-icon>mdi-open-in-new</v-icon>
                      </v-btn>
                      
                      <v-btn
                        v-if="project.githubUrl"
                        icon
                        color="white"
                        @click="openProject(project.githubUrl)"
                      >
                        <v-icon>mdi-github</v-icon>
                      </v-btn>
                    </div>
                  </v-img>
                  
                  <v-card-text>
                    <h4 class="text-h6 mb-2">{{ project.title }}</h4>
                    <p class="text-body-2 mb-3">{{ project.description }}</p>
                    
                    <div class="d-flex flex-wrap">
                      <v-chip
                        v-for="tech in project.technologies"
                        :key="tech"
                        size="small"
                        color="primary"
                        variant="outlined"
                        class="mr-1 mb-1"
                      >
                        {{ tech }}
                      </v-chip>
                    </div>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <!-- Certificaciones -->
        <v-card v-if="activeTab === 'certifications'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-certificate</v-icon>
            Certificaciones y Cursos
            <v-spacer></v-spacer>
            <v-btn
              v-if="isOwnProfile"
              color="primary"
              @click="addCertification"
              prepend-icon="mdi-plus"
            >
              Agregar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <v-row>
              <v-col
                v-for="cert in profileData.certifications"
                :key="cert.id"
                cols="12"
                md="6"
              >
                <v-card variant="outlined" class="certification-card">
                  <v-card-text>
                    <div class="d-flex align-center mb-3">
                      <v-avatar
                        size="48"
                        :color="cert.providerColor || 'primary'"
                        class="mr-3"
                      >
                        <v-icon color="white">{{ cert.icon || 'mdi-certificate' }}</v-icon>
                      </v-avatar>
                      
                      <div>
                        <h4 class="text-subtitle-1">{{ cert.name }}</h4>
                        <p class="text-body-2 text-primary">{{ cert.provider }}</p>
                      </div>
                    </div>
                    
                    <div class="d-flex justify-space-between align-center mb-2">
                      <span class="text-body-2">
                        <v-icon size="16" class="mr-1">mdi-calendar</v-icon>
                        {{ formatDate(cert.date) }}
                      </span>
                      
                      <v-chip
                        v-if="cert.verified"
                        color="success"
                        size="small"
                      >
                        <v-icon left size="16">mdi-check</v-icon>
                        Verificado
                      </v-chip>
                    </div>
                    
                    <p v-if="cert.description" class="text-body-2 mb-3">
                      {{ cert.description }}
                    </p>
                    
                    <v-btn
                      v-if="cert.credentialUrl"
                      size="small"
                      color="primary"
                      variant="outlined"
                      @click="openProject(cert.credentialUrl)"
                    >
                      Ver Credencial
                    </v-btn>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
        
        <!-- Recomendaciones -->
        <v-card v-if="activeTab === 'recommendations'" class="mb-6" elevation="2">
          <v-card-title class="d-flex align-center">
            <v-icon class="mr-3">mdi-comment-quote</v-icon>
            Recomendaciones
            <v-spacer></v-spacer>
            <v-btn
              v-if="!isOwnProfile"
              color="primary"
              @click="addRecommendation"
              prepend-icon="mdi-plus"
            >
              Recomendar
            </v-btn>
          </v-card-title>
          
          <v-card-text>
            <div
              v-for="recommendation in profileData.recommendations"
              :key="recommendation.id"
              class="mb-4"
            >
              <v-card variant="outlined" class="recommendation-card">
                <v-card-text>
                  <div class="d-flex align-start mb-3">
                    <v-avatar
                      size="48"
                      class="mr-3"
                    >
                      <v-img :src="recommendation.avatar || '/api/placeholder/48/48'"></v-img>
                    </v-avatar>
                    
                    <div class="flex-grow-1">
                      <h4 class="text-subtitle-1">{{ recommendation.name }}</h4>
                      <p class="text-body-2 text-primary">{{ recommendation.position }}</p>
                      <p class="text-caption text-grey">{{ recommendation.company }}</p>
                    </div>
                    
                    <v-rating
                      :model-value="recommendation.rating"
                      readonly
                      density="compact"
                      color="warning"
                      size="small"
                    ></v-rating>
                  </div>
                  
                  <blockquote class="text-body-1 font-italic mb-3">
                    "{{ recommendation.text }}"
                  </blockquote>
                  
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption text-grey">
                      {{ formatDate(recommendation.date) }}
                    </span>
                    
                    <div class="d-flex align-center">
                      <v-icon size="16" color="primary" class="mr-1">mdi-handshake</v-icon>
                      <span class="text-caption">{{ recommendation.relationship }}</span>
                    </div>
                  </div>
                </v-card-text>
              </v-card>
            </div>
            
            <div v-if="profileData.recommendations.length === 0" class="text-center py-8">
              <v-icon size="64" color="grey">mdi-comment-quote-outline</v-icon>
              <p class="text-h6 mt-4">No hay recomendaciones aún</p>
              <p class="text-body-2 text-grey">
                Las recomendaciones aparecerán aquí cuando las recibas
              </p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <!-- Sidebar derecho -->
      <v-col cols="12" md="4">
        <!-- Estadísticas del perfil -->
        <v-card class="mb-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-chart-line</v-icon>
            Estadísticas del Perfil
          </v-card-title>
          
          <v-card-text>
            <div class="stats-grid">
              <div class="stat-item">
                <div class="stat-number text-h4 text-primary">{{ profileData.stats.views }}</div>
                <div class="stat-label text-body-2">Visualizaciones</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-number text-h4 text-success">{{ profileData.stats.applications }}</div>
                <div class="stat-label text-body-2">Postulaciones</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-number text-h4 text-warning">{{ profileData.stats.interviews }}</div>
                <div class="stat-label text-body-2">Entrevistas</div>
              </div>
              
              <div class="stat-item">
                <div class="stat-number text-h4 text-info">{{ profileData.stats.connections }}</div>
                <div class="stat-label text-body-2">Conexiones</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
        
        <!-- Compatibilidad con ofertas -->
        <v-card class="mb-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-target</v-icon>
            Ofertas Recomendadas
          </v-card-title>
          
          <v-card-text>
            <div
              v-for="job in recommendedJobs"
              :key="job.id"
              class="mb-3"
            >
              <v-card variant="outlined" class="job-match-card" hover>
                <v-card-text class="pa-3">
                  <div class="d-flex align-center mb-2">
                    <div class="flex-grow-1">
                      <h4 class="text-subtitle-2">{{ job.title }}</h4>
                      <p class="text-caption text-primary">{{ job.company }}</p>
                    </div>
                    
                    <v-chip
                      :color="getMatchColor(job.match)"
                      size="small"
                    >
                      {{ job.match }}% match
                    </v-chip>
                  </div>
                  
                  <div class="d-flex justify-space-between align-center">
                    <span class="text-caption">{{ job.location }}</span>
                    <v-btn
                      size="small"
                      color="primary"
                      variant="text"
                      @click="viewJob(job)"
                    >
                      Ver
                    </v-btn>
                  </div>
                </v-card-text>
              </v-card>
            </div>
          </v-card-text>
        </v-card>
        
        <!-- Actividad reciente -->
        <v-card class="mb-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-clock</v-icon>
            Actividad Reciente
          </v-card-title>
          
          <v-card-text>
            <v-timeline density="compact" side="end">
              <v-timeline-item
                v-for="activity in profileData.recentActivity"
                :key="activity.id"
                dot-color="primary"
                size="small"
              >
                <div class="d-flex align-center">
                  <v-icon size="16" class="mr-2">{{ getActivityIcon(activity.type) }}</v-icon>
                  <div class="flex-grow-1">
                    <div class="text-body-2">{{ activity.description }}</div>
                    <div class="text-caption text-grey">{{ formatDateTime(activity.date) }}</div>
                  </div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-card-text>
        </v-card>
        
        <!-- Skills trending -->
        <v-card class="mb-4" elevation="2">
          <v-card-title>
            <v-icon class="mr-2">mdi-trending-up</v-icon>
            Habilidades en Demanda
          </v-card-title>
          
          <v-card-text>
            <div
              v-for="skill in trendingSkills"
              :key="skill.name"
              class="d-flex justify-space-between align-center mb-2"
            >
              <span class="text-body-2">{{ skill.name }}</span>
              <v-chip
                :color="skill.hasSkill ? 'success' : 'grey'"
                size="small"
                variant="outlined"
              >
                <v-icon left size="16">
                  {{ skill.hasSkill ? 'mdi-check' : 'mdi-plus' }}
                </v-icon>
                {{ skill.hasSkill ? 'Tienes' : 'Aprender' }}
              </v-chip>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    
    <!-- Dialog para agregar/editar experiencia -->
    <v-dialog v-model="experienceDialog" max-width="600">
      <v-card>
        <v-card-title>
          {{ editingExperience ? 'Editar' : 'Agregar' }} Experiencia
        </v-card-title>
        
        <v-card-text>
          <v-form ref="experienceForm">
            <v-text-field
              v-model="experienceForm.position"
              label="Cargo"
              variant="outlined"
              class="mb-3"
            ></v-text-field>
            
            <v-text-field
              v-model="experienceForm.company"
              label="Empresa"
              variant="outlined"
              class="mb-3"
            ></v-text-field>
            
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model="experienceForm.startDate"
                  label="Fecha de inicio"
                  type="date"
                  variant="outlined"
                ></v-text-field>
              </v-col>
              
              <v-col cols="6">
                <v-text-field
                  v-model="experienceForm.endDate"
                  label="Fecha de fin"
                  type="date"
                  variant="outlined"
                  :disabled="experienceForm.current"
                ></v-text-field>
              </v-col>
            </v-row>
            
            <v-checkbox
              v-model="experienceForm.current"
              label="Trabajo actual"
            ></v-checkbox>
            
            <v-textarea
              v-model="experienceForm.description"
              label="Descripción"
              variant="outlined"
              rows="3"
              class="mb-3"
            ></v-textarea>
            
            <v-combobox
              v-model="experienceForm.technologies"
              label="Tecnologías utilizadas"
              variant="outlined"
              multiple
              chips
            ></v-combobox>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn @click="experienceDialog = false">Cancelar</v-btn>
          <v-btn color="primary" @click="saveExperience">Guardar</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// Estados reactivos
const activeTab = ref('overview')
const experienceDialog = ref(false)
const editingExperience = ref(false)
const editingIndex = ref(-1)

// Formularios
const experienceForm = ref({
  position: '',
  company: '',
  startDate: '',
  endDate: '',
  current: false,
  description: '',
  technologies: []
})

// Secciones del perfil
const sections = ref([
  { title: 'Resumen', value: 'overview', icon: 'mdi-account' },
  { title: 'Experiencia', value: 'experience', icon: 'mdi-briefcase' },
  { title: 'Educación', value: 'education', icon: 'mdi-school' },
  { title: 'Habilidades', value: 'skills', icon: 'mdi-star' },
  { title: 'Proyectos', value: 'projects', icon: 'mdi-folder' },
  { title: 'Certificaciones', value: 'certifications', icon: 'mdi-certificate' },
  { title: 'Recomendaciones', value: 'recommendations', icon: 'mdi-comment-quote' }
])

// Datos del perfil (simulados)
const profileData = ref({
  name: 'Juan Carlos Mendoza',
  title: 'Desarrollador Full Stack Senior',
  location: 'Arequipa, Perú',
  email: 'juan.mendoza@email.com',
  phone: '+51 987 654 321',
  birthDate: '1995-08-15',
  availability: 'Disponible',
  rating: 4.8,
  reviews: 23,
  verified: true,
  bookmarked: false,
  avatar: '/api/placeholder/120/120',
  bannerImage: '/api/placeholder/1200/300',
  summary: 'Desarrollador apasionado con 5+ años de experiencia en tecnologías web modernas.',
  about: 'Soy un desarrollador full stack con una sólida experiencia en el desarrollo de aplicaciones web escalables y sistemas distribuidos. Me especializo en JavaScript, Python y tecnologías cloud. Tengo un enfoque orientado a resultados y disfruto trabajando en equipos colaborativos donde puedo contribuir al crecimiento tanto técnico como del negocio.',
  
  socialLinks: [
    { platform: 'LinkedIn', url: 'https://linkedin.com/in/juanmendoza', icon: 'mdi-linkedin' },
    { platform: 'GitHub', url: 'https://github.com/juanmendoza', icon: 'mdi-github' },
    { platform: 'Portfolio', url: 'https://juanmendoza.dev', icon: 'mdi-web' }
  ],
  
  topSkills: [
    { name: 'JavaScript', level: 5 },
    { name: 'React', level: 5 },
    { name: 'Node.js', level: 4 },
    { name: 'Python', level: 4 },
    { name: 'AWS', level: 3 }
  ],
  
  achievements: [
    {
      id: 1,
      title: 'Mejor Desarrollador del Año 2023',
      description: 'Reconocimiento por excelencia técnica y liderazgo'
    },
    {
      id: 2,
      title: 'Certificación AWS Solutions Architect',
      description: 'Certificación profesional en arquitectura de soluciones cloud'
    }
  ],
  
  experience: [
    {
      position: 'Senior Full Stack Developer',
      company: 'TechCorp Solutions',
      startDate: '2022-01-15',
      endDate: null,
      current: true,
      description: 'Desarrollo y mantenimiento de aplicaciones web empresariales utilizando React, Node.js y AWS. Liderazgo de equipo de 4 desarrolladores junior.',
      technologies: ['React', 'Node.js', 'PostgreSQL', 'AWS', 'Docker'],
      companyColor: 'primary',
      companyIcon: 'mdi-rocket'
    },
    {
      position: 'Full Stack Developer',
      company: 'StartupTech',
      startDate: '2020-06-01',
      endDate: '2021-12-31',
      current: false,
      description: 'Desarrollo de MVP y características principales de la plataforma SaaS. Implementación de arquitectura de microservicios.',
      technologies: ['Vue.js', 'Express.js', 'MongoDB', 'Redis'],
      companyColor: 'green',
      companyIcon: 'mdi-leaf'
    }
  ],
  
  education: [
    {
      degree: 'Ingeniería de Sistemas',
      institution: 'Universidad Nacional de San Agustín',
      startDate: '2018-03-01',
      endDate: '2022-12-15',
      current: false,
      description: 'Especialización en desarrollo de software y sistemas distribuidos',
      grade: '16.8/20'
    }
  ],
  
  technicalSkills: [
    { name: 'JavaScript', level: 5 },
    { name: 'TypeScript', level: 4 },
    { name: 'React', level: 5 },
    { name: 'Vue.js', level: 4 },
    { name: 'Node.js', level: 4 },
    { name: 'Python', level: 4 },
    { name: 'SQL', level: 4 },
    { name: 'MongoDB', level: 3 },
    { name: 'AWS', level: 3 },
    { name: 'Docker', level: 3 }
  ],
  
  softSkills: [
    'Liderazgo', 'Comunicación', 'Trabajo en equipo', 'Resolución de problemas',
    'Adaptabilidad', 'Pensamiento crítico', 'Gestión del tiempo'
  ],
  
  languages: [
    { name: 'Español', level: 'Nativo' },
    { name: 'Inglés', level: 'Avanzado' },
    { name: 'Portugués', level: 'Básico' }
  ],
  
  projects: [
    {
      id: 1,
      title: 'E-commerce Platform',
      description: 'Plataforma de comercio electrónico completa con panel de administración',
      image: '/api/placeholder/400/200',
      technologies: ['React', 'Node.js', 'Stripe', 'PostgreSQL'],
      liveUrl: 'https://demo-ecommerce.com',
      githubUrl: 'https://github.com/juan/ecommerce'
    },
    {
      id: 2,
      title: 'Task Management App',
      description: 'Aplicación de gestión de tareas con colaboración en tiempo real',
      image: '/api/placeholder/400/200',
      technologies: ['Vue.js', 'Socket.io', 'Express', 'MongoDB'],
      liveUrl: 'https://taskapp.com',
      githubUrl: 'https://github.com/juan/taskapp'
    }
  ],
  
  certifications: [
    {
      id: 1,
      name: 'AWS Solutions Architect',
      provider: 'Amazon Web Services',
      date: '2023-05-15',
      verified: true,
      description: 'Certificación en diseño de arquitecturas escalables en AWS',
      credentialUrl: 'https://aws.amazon.com/certification',
      providerColor: 'orange',
      icon: 'mdi-aws'
    },
    {
      id: 2,
      name: 'React Professional',
      provider: 'Meta',
      date: '2022-11-20',
      verified: true,
      description: 'Certificación avanzada en desarrollo con React',
      credentialUrl: 'https://developers.facebook.com/certification',
      providerColor: 'blue',
      icon: 'mdi-react'
    }
  ],
  
  recommendations: [
    {
      id: 1,
      name: 'María García',
      position: 'Tech Lead',
      company: 'TechCorp Solutions',
      avatar: '/api/placeholder/48/48',
      rating: 5,
      text: 'Juan es un desarrollador excepcional con una capacidad técnica sobresaliente. Su liderazgo y mentoria han sido fundamentales para el crecimiento del equipo.',
      date: '2023-10-15',
      relationship: 'Supervisora directa'
    },
    {
      id: 2,
      name: 'Carlos Rodriguez',
      position: 'Product Manager',
      company: 'StartupTech',
      avatar: '/api/placeholder/48/48',
      rating: 5,
      text: 'Trabajé con Juan durante 2 años y siempre entregó proyectos de alta calidad en tiempo y forma. Su comunicación es excelente.',
      date: '2022-01-10',
      relationship: 'Colega'
    }
  ],
  
  stats: {
    views: 1247,
    applications: 23,
    interviews: 8,
    connections: 156
  },
  
  recentActivity: [
    {
      id: 1,
      type: 'application',
      description: 'Aplicó a Senior Developer en InnovaTech',
      date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000)
    },
    {
      id: 2,
      type: 'skill',
      description: 'Agregó nueva habilidad: GraphQL',
      date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000)
    },
    {
      id: 3,
      type: 'project',
      description: 'Publicó nuevo proyecto: Chat App',
      date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)
    }
  ]
})

// Ofertas recomendadas
const recommendedJobs = ref([
  {
    id: 1,
    title: 'Senior React Developer',
    company: 'InnovaTech',
    location: 'Lima, Perú',
    match: 95
  },
  {
    id: 2,
    title: 'Full Stack Engineer',
    company: 'StartupPro',
    location: 'Remoto',
    match: 88
  },
  {
    id: 3,
    title: 'Tech Lead',
    company: 'MegaCorp',
    location: 'Arequipa, Perú',
    match: 82
  }
])

// Habilidades en tendencia
const trendingSkills = ref([
  { name: 'TypeScript', hasSkill: true },
  { name: 'GraphQL', hasSkill: false },
  { name: 'Kubernetes', hasSkill: false },
  { name: 'Terraform', hasSkill: false }
])

// Computadas
const isOwnProfile = computed(() => {
  // En una aplicación real, esto verificaría si el usuario actual es el dueño del perfil
  return true
})

// Métodos
const calculateAge = (birthDate) => {
  const today = new Date()
  const birth = new Date(birthDate)
  let age = today.getFullYear() - birth.getFullYear()
  const monthDiff = today.getMonth() - birth.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
    age--
  }
  
  return age
}

const getAvailabilityColor = (availability) => {
  switch (availability) {
    case 'Disponible': return 'success'
    case 'Ocupado': return 'error'
    case 'Disponible en breve': return 'warning'
    default: return 'grey'
  }
}

const getAvailabilityIcon = (availability) => {
  switch (availability) {
    case 'Disponible': return 'mdi-check-circle'
    case 'Ocupado': return 'mdi-close-circle'
    case 'Disponible en breve': return 'mdi-clock'
    default: return 'mdi-help-circle'
  }
}

const getSocialIcon = (platform) => {
  const icons = {
    'LinkedIn': 'mdi-linkedin',
    'GitHub': 'mdi-github',
    'Portfolio': 'mdi-web',
    'Twitter': 'mdi-twitter'
  }
  return icons[platform] || 'mdi-link'
}

const getSkillColor = (level) => {
  if (level >= 4) return 'success'
  if (level >= 3) return 'warning'
  if (level >= 2) return 'info'
  return 'error'
}

const getMatchColor = (match) => {
  if (match >= 90) return 'success'
  if (match >= 75) return 'warning'
  if (match >= 60) return 'info'
  return 'error'
}

const getActivityIcon = (type) => {
  const icons = {
    application: 'mdi-send',
    skill: 'mdi-star-plus',
    project: 'mdi-folder-plus',
    certification: 'mdi-certificate',
    recommendation: 'mdi-comment-plus'
  }
  return icons[type] || 'mdi-circle'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const options = { year: 'numeric', month: 'short' }
  return new Date(dateString).toLocaleDateString('es-ES', options)
}

const formatDateTime = (date) => {
  const options = { 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }
  return new Intl.DateTimeFormat('es-ES', options).format(date)
}

// Métodos de interacción
const contactCandidate = () => {
  window.showSnackbar('Abriendo chat con el candidato...', 'info')
}

const scheduleInterview = () => {
  window.showSnackbar('Abriendo calendario para agendar entrevista...', 'info')
}

const toggleBookmark = () => {
  profileData.value.bookmarked = !profileData.value.bookmarked
  const message = profileData.value.bookmarked ? 'Candidato guardado' : 'Candidato removido'
  window.showSnackbar(message, 'success')
}

const changeBanner = () => {
  // Simular cambio de banner
  window.showSnackbar('Funcionalidad de cambio de banner en desarrollo', 'info')
}

const changeAvatar = () => {
  // Simular cambio de avatar
  window.showSnackbar('Funcionalidad de cambio de avatar en desarrollo', 'info')
}

// Métodos para proyectos
const viewProject = (project) => {
  window.showSnackbar(`Viendo detalles de: ${project.title}`, 'info')
}

const openProject = (url) => {
  window.open(url, '_blank')
}

// Métodos para ofertas
const viewJob = (job) => {
  router.push(`/ofertas/${job.id}`)
}

// Métodos de formularios
const addExperience = () => {
  experienceForm.value = {
    position: '',
    company: '',
    startDate: '',
    endDate: '',
    current: false,
    description: '',
    technologies: []
  }
  editingExperience.value = false
  editingIndex.value = -1
  experienceDialog.value = true
}

const editExperience = (exp, index) => {
  experienceForm.value = { ...exp }
  editingExperience.value = true
  editingIndex.value = index
  experienceDialog.value = true
}

const saveExperience = () => {
  if (editingExperience.value) {
    profileData.value.experience[editingIndex.value] = { ...experienceForm.value }
  } else {
    profileData.value.experience.unshift({ ...experienceForm.value })
  }
  
  experienceDialog.value = false
  window.showSnackbar('Experiencia guardada correctamente', 'success')
}

const addEducation = () => {
  window.showSnackbar('Funcionalidad de agregar educación en desarrollo', 'info')
}

const editEducation = (edu, index) => {
  window.showSnackbar('Funcionalidad de editar educación en desarrollo', 'info')
}

const addSkill = () => {
  window.showSnackbar('Funcionalidad de agregar habilidad en desarrollo', 'info')
}

const addProject = () => {
  window.showSnackbar('Funcionalidad de agregar proyecto en desarrollo', 'info')
}

const addCertification = () => {
  window.showSnackbar('Funcionalidad de agregar certificación en desarrollo', 'info')
}

const addRecommendation = () => {
  window.showSnackbar('Funcionalidad de agregar recomendación en desarrollo', 'info')
}

// Lifecycle
onMounted(() => {
  // Simular carga de datos del perfil
  console.log('Perfil cargado:', profileData.value.name)
})
</script>

<style scoped>
.profile-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 24px;
}

.profile-header {
  border-radius: 16px;
  overflow: hidden;
  position: relative;
}

.profile-banner {
  position: relative;
}

.banner-image {
  border-radius: 16px 16px 0 0;
}

.banner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, transparent 0%, rgba(0,0,0,0.3) 100%);
}

.change-banner-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
}

.profile-info {
  margin-top: -60px;
  position: relative;
  z-index: 2;
}

.profile-avatar-container {
  position: relative;
}

.profile-avatar {
  border: 4px solid white;
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.verification-badge {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
}

.change-avatar-btn {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(255,255,255,0.9);
  backdrop-filter: blur(10px);
}

/* Estadísticas */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-item {
  text-align: center;
  padding: 16px;
  background: rgba(var(--v-theme-surface), 0.8);
  border-radius: 12px;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
}

.stat-number {
  font-weight: bold;
  line-height: 1.2;
}

.stat-label {
  opacity: 0.8;
}

/* Cards de proyectos */
.project-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.project-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.project-card:hover .project-overlay {
  opacity: 1;
}

/* Cards de certificaciones */
.certification-card {
  transition: all 0.3s ease;
  height: 100%;
}

.certification-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.1);
}

/* Cards de recomendaciones */
.recommendation-card {
  position: relative;
  overflow: hidden;
}

.recommendation-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, var(--v-theme-primary), var(--v-theme-secondary));
}

/* Cards de trabajos recomendados */
.job-match-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.job-match-card:hover {
  transform: translateX(4px);
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

/* Habilidades */
.skill-item {
  padding: 12px;
  background: rgba(var(--v-theme-surface), 0.5);
  border-radius: 8px;
  border: 1px solid rgba(var(--v-theme-primary), 0.1);
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

.v-card {
  animation: fadeInUp 0.6s ease-out;
}

/* Efectos de hover mejorados */
.v-chip:hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

.v-btn:not(.v-btn--disabled):hover {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

/* Timeline personalizada */
.v-timeline-item {
  margin-bottom: 8px;
}

/* Responsive */
@media (max-width: 960px) {
  .profile-container {
    padding: 16px;
  }
  
  .profile-info {
    margin-top: -40px;
  }
  
  .profile-avatar {
    width: 80px !important;
    height: 80px !important;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }
  
  .stat-item {
    padding: 12px;
  }
  
  .stat-number {
    font-size: 1.5rem !important;
  }
}

@media (max-width: 600px) {
  .profile-avatar {
    width: 60px !important;
    height: 60px !important;
  }
  
  .verification-badge {
    display: none;
  }
  
  .change-avatar-btn {
    display: none;
  }
}

/* Dark mode support */
.v-theme--dark .profile-container {
  background: linear-gradient(135deg, #1a1a1a 0%, #2d3748 100%);
}

.v-theme--dark .profile-header {
  border: 1px solid rgba(255,255,255,0.1);
}

.v-theme--dark .stat-item {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
}

.v-theme--dark .skill-item {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
}

/* Scroll suave */
html {
  scroll-behavior: smooth;
}

/* Efectos adicionales */
.v-tabs {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.v-tab {
  transition: all 0.3s ease;
}

.v-tab:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
}

/* Mejoras para los avatares */
.v-avatar {
  transition: all 0.3s ease;
}

.v-avatar:hover {
  transform: scale(1.05);
}

/* Efectos para las progress bars */
.v-progress-linear {
  transition: all 0.8s ease;
  border-radius: 4px;
  overflow: hidden;
}

/* Mejoras para los ratings */
.v-rating {
  transition: all 0.3s ease;
}

/* Customización del scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0,0,0,0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(var(--v-theme-primary), 0.5);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(var(--v-theme-primary), 0.7);
}

/* Efectos de focus mejorados */
.v-text-field:focus-within,
.v-textarea:focus-within,
.v-select:focus-within {
  transform: translateY(-1px);
  transition: transform 0.2s ease;
}

/* Mejoras para los dialogs */
.v-dialog .v-card {
  border-radius: 16px;
  overflow: hidden;
}

/* Efectos para las listas */
.v-list-item:hover {
  background-color: rgba(var(--v-theme-primary), 0.05);
  transform: translateX(2px);
  transition: all 0.2s ease;
}

/* Animación de pulso para elementos importantes */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.02);
  }
}

.verification-badge {
  animation: pulse 2s ease-in-out infinite;
}

/* Mejoras para la tipografía */
.text-h3, .text-h4, .text-h5, .text-h6 {
  font-weight: 600;
  letter-spacing: -0.025em;
}

/* Efectos de transición globales */
* {
  transition: color 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
}
</style>