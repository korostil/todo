<script setup>
import { getFormattedDueDateTime } from "@/store/services/utils/dates";
import { completeTask } from "@/store/api/tasks";
import DialogUpdateTask from "@/components/DialogUpdateTask.vue";
import { computed, ref } from "vue";
import { projects } from "@/store/api/projects";
import { findEntityIndexById } from "@/store/services/utils/entities";
import { PERSONAL_SPACE } from "@/store/services/constants";

const props = defineProps({ task: Object });
const emit = defineEmits(["taskCompleted"]);
const refTaskIsCompleted = ref(props.task.is_completed);
const projectIdx = findEntityIndexById(projects, props.task.project_id),
  project = projects.value[projectIdx];

function doComplete() {
  completeTask(props.task.id);
  refTaskIsCompleted.value = true;
  emit("taskCompleted", props.task.id);
}

const due_datetime = computed(() => {
  return getFormattedDueDateTime(props.task.due_date, props.task.due_time);
});
const spaceIcon = computed(() => {
  return props.task.space === PERSONAL_SPACE ? "mdi-account" : "mdi-domain";
});
</script>

<template>
  <v-row>
    <v-col cols="12" sm="1">
      <v-btn
        class="ma-2"
        size="small"
        variant="outlined"
        :icon="refTaskIsCompleted ? 'mdi-check' : ''"
        :color="props.task.decisive ? 'red' : 'grey'"
        @click="doComplete"
      ></v-btn>
    </v-col>
    <v-col cols="12" sm="11">
      <dialog-update-task :task="task"></dialog-update-task>
      <div class="mt-1">
        <span class="text-h5">{{ props.task.title }}</span>
      </div>
      <div>
        <span class="text-subtitle-1">{{ props.task.description }}</span>
      </div>
      <v-row>
        <v-col cols="12" sm="8">
          <v-chip
            class="ml-0 pl-0 task-due"
            size="small"
            variant="text"
            v-if="due_datetime"
          >
            {{ due_datetime }}
          </v-chip>
          <v-chip class="my-2 mx-1" color="#a6e22e" size="small" label>
            some
          </v-chip>
          <v-chip class="my-2 mx-1" color="#e6db74" size="small" label>
            different
          </v-chip>
          <v-chip class="my-2 mx-1" color="#51edbc" size="small" label>
            tags
          </v-chip>
        </v-col>
        <v-col cols="12" sm="4" class="d-flex justify-end">
          <v-chip
            class="ma-2"
            :color="project ? project.color : ''"
            size="small"
            variant="text"
          >
            {{ project ? project.title : "" }}
            <v-icon end :icon="spaceIcon"></v-icon>
          </v-chip>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>

<style scoped>
.task-due {
  color: #fd971f;
}
</style>
