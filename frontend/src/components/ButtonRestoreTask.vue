<script setup>
import { ref } from "vue";
import { restoreTask } from "@/store/api/tasks";

const props = defineProps({
  task: Object,
});
const dialog = ref(false);

function onRestoreClick() {
  restoreTask(props.task.id);
  dialog.value = false;
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="30%" class="text-center">
    <template v-slot:activator="{ props }">
      <v-btn variant="plain" prepend-icon="mdi-restore" v-bind="props">
        Restore
      </v-btn>
    </template>

    <v-card>
      <v-card-text>
        Are you sure you want to restore task "{{ props.task.title }}"?
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" variant="text" @click="dialog.value = false">
          Cancel
        </v-btn>
        <v-btn color="red-darken-1" @click="onRestoreClick"> Restore </v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
