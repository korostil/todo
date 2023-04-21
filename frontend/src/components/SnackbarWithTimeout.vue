<script setup>
import { ref } from "vue";

defineProps({
  text: String,
  timeout: { type: Number, required: false, default: 3000 },
});
const snackbar = ref(true);
</script>

<template>
  <v-snackbar v-model="snackbar" :timeout="timeout" color="grey-darken-2">
    {{ text }}
  </v-snackbar>
</template>

<style scoped></style>
