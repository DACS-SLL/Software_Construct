<template>
  <div class="card">
    <h2>{{ title }}</h2>
    <div class="actions" v-if="showCreate">
      <button class="btn btn-primary" @click="handleCreate">{{ createLabel }}</button>
    </div>

    <div class="loading" v-if="loading">
      <div class="loading-spinner"></div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <table class="table" v-else-if="items.length > 0">
      <thead>
        <tr>
          <th v-for="(header, index) in headers" :key="index">
            {{ header }}
          </th>
          <th>Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(item, index) in items" :key="index">
          <td v-for="(header, headerIndex) in headers" :key="headerIndex">
            {{ item[header.toLowerCase()] }}
          </td>
          <td>
            <button class="btn btn-secondary" @click="handleEdit(item)">Editar</button>
            <button class="btn btn-danger" @click="handleDelete(item)">{{ actionLabel }}</button>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-else class="alert alert-info">
      No hay elementos disponibles
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseList',
  props: {
    title: String,
    headers: Array,
    items: Array,
    loading: Boolean,
    error: String,
    actionLabel: {
      type: String,
      default: 'Eliminar'
    },
    showCreate: {
      type: Boolean,
      default: true
    },
    createLabel: {
      type: String,
      default: 'Crear Nuevo'
    }
  },
  methods: {
    handleCreate() {
      this.$emit('create')
    },
    handleEdit(item) {
      this.$emit('edit', item)
    },
    handleDelete(item) {
      if (confirm('¿Estás seguro de que deseas eliminar este elemento?')) {
        this.$emit('delete', item)
      }
    }
  }
}
</script>
