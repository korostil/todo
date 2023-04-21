<script setup>
import { ref } from "vue";
import { archiveProject } from "@/store/api/projects";

const props = defineProps({
  project: Object,
});
const dialog = ref(false);

function onArchiveClick() {
  archiveProject(props.project.id);
  dialog.value = false;
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="30%" class="text-center">
    <template v-slot:activator="{ props }">
      <v-btn variant="plain" prepend-icon="mdi-archive-outline" v-bind="props"
        >Archive</v-btn
      >
    </template>

    <v-card>
      <v-card-text>
        Are you sure you want to archive project "{{ props.project.title }}"?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="text" @click="dialog.value = false">
          Cancel
        </v-btn>
        <v-btn color="red-darken-1" @click="onArchiveClick">Archive</v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
