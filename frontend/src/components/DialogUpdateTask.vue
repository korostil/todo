<script setup>
import { ref } from "vue";
import { deleteTask, updateTask } from "@/store/api/tasks";
import { activeProjects } from "@/store/api/projects";
import ButtonRemoveTask from "@/components/ButtonRemoveTask.vue";
import { taskDueDateRules, titleRules } from "@/store/services/rules";
import { PERSONAL_SPACE, WORK_SPACE } from "@/store/services/constants";
import { findEntityIndexById } from "@/store/services/utils/entities";
import ButtonRestoreTask from "@/components/ButtonRestoreTask.vue";

const emit = defineEmits(["taskUpdated"]);
const props = defineProps({
  task: Object,
});
const dialog = ref(false),
  valid = ref(false);
const task = ref(Object.assign({}, props.task));

function doUpdate() {
  const projectIdx = findEntityIndexById(activeProjects, task.value.project_id),
    project = activeProjects.value[projectIdx];
  if (project) task.value.space = project.space;

  return updateTask(task.value.id, task.value)
    .then(() => {
      dialog.value = false;
      emit("taskUpdated", task);
    })
    .catch(() => {
      console.log("error");
    });
}

function doDelete(task_id) {
  deleteTask(task_id)
    .then(() => {
      dialog.value = false;
    })
    .catch(() => {
      console.log("error");
    });
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="30%" rounded="lg" activator="parent">
    <v-card>
      <v-container>
        <v-card-title>
          <span class="text-h4">Update task</span>
        </v-card-title>

        <v-form v-model="valid" @submit.prevent="doUpdate">
          <v-container>
            <v-text-field
              color="grey-darken-2"
              label="Title"
              v-model="task.title"
              variant="outlined"
              :rules="titleRules"
              required
              autofocus
            ></v-text-field>

            <v-text-field
              color="grey-darken-2"
              label="Description"
              v-model="task.description"
              variant="outlined"
            ></v-text-field>

            <v-switch
              label="Decisive"
              v-model="task.decisive"
              color="secondary"
              density="compact"
            ></v-switch>

            <v-text-field
              label="Due date"
              type="date"
              v-model="task.due_date"
              variant="outlined"
              :rules="taskDueDateRules"
            ></v-text-field>

            <v-text-field
              label="Due time"
              type="time"
              v-model="task.due_time"
              variant="outlined"
            ></v-text-field>

            <v-select
              label="Project"
              v-model="task.project_id"
              :items="activeProjects"
              item-title="title"
              item-value="id"
              variant="outlined"
              clearable
            ></v-select>

            <v-btn-toggle
              v-model="task.space"
              active-color="primary"
              mandatory
              v-if="!task.project_id"
            >
              <v-label> Space </v-label>
              <v-btn icon="mdi-account" :value="PERSONAL_SPACE"></v-btn>
              <v-btn icon="mdi-domain" :value="WORK_SPACE"></v-btn>
            </v-btn-toggle>
          </v-container>

          <v-card-actions>
            <v-spacer></v-spacer>
            <button-remove-task
              :task="task"
              @task-removed="doDelete"
            ></button-remove-task>
            <button-restore-task :task="task"></button-restore-task>
            <v-btn color="primary" type="submit"> Save </v-btn>
          </v-card-actions>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
