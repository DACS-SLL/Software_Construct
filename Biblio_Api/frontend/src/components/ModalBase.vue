<template>
  <div v-if="show" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <h2>{{ title }}</h2>
        <button class="btn btn-danger btn-small" @click="$emit('close')">
          &times;
        </button>
      </div>
      
      <div class="modal-body">
        <slot name="body"></slot>
      </div>
      
      <div class="modal-footer">
        <slot name="footer">
          <button class="btn btn-secondary" @click="$emit('close')">
            Cancelar
          </button>
          <button class="btn btn-primary" @click="$emit('submit')">
            {{ submitText }}
          </button>
        </slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ModalBase',
  props: {
    show: Boolean,
    title: String,
    submitText: {
      type: String,
      default: 'Guardar'
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background-color: white;
  border-radius: var(--border-radius);
  padding: 1.5rem;
  width: 90%;
  max-width: 600px;
  box-shadow: var(--box-shadow);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  margin: 0;
}

.modal-header button {
  padding: 0.5rem;
  font-size: 1.5rem;
  line-height: 1;
}

.modal-body {
  margin-bottom: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.btn-small {
  padding: 0.25rem 0.5rem;
}
</style>
