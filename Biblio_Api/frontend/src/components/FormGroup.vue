<template>
  <div class="form-group">
    <label class="block font-semibold mb-1">
      {{ label }}
      <span v-if="required" class="text-red-500">*</span>
    </label>
    <slot></slot>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  required: Boolean
})
</script>
