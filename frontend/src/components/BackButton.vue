<script setup>
import { RouterLink } from 'vue-router';
import { defineProps } from 'vue';

const props = defineProps({
    to: {
        type: String,
        required: true
    },
    text: {
        type: String,
        required: true
    },
})
</script>

<template>
  <section>
    <div class="container mt-4">
      <RouterLink
        :to="to"
        class="d-flex align-items-center btn btn-outline-primary rounded-pill shadow-sm hover-scale"
        style="width: fit-content; transition: all 0.2s ease;"
      >
        <i class="pi pi-arrow-circle-left me-2"></i>
        {{ text }}
      </RouterLink>
    </div>
  </section>
</template>