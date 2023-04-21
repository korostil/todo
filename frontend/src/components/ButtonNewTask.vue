<script setup>
import { ref } from "vue";
import { createTask } from "@/store/api/tasks";
import { useRouter } from "vue-router";
import { activeProjects } from "@/store/api/projects";
import { taskDueDateRules, titleRules } from "@/store/services/rules";
import { PERSONAL_SPACE, WORK_SPACE } from "@/store/services/constants";
import { findEntityIndexById } from "@/store/services/utils/entities";

const dialog = ref(false),
  valid = ref(false);
const router = useRouter();
const task = ref({
  space: PERSONAL_SPACE,
});

function doCreate() {
  const projectIdx = findEntityIndexById(activeProjects, task.value.project_id),
    project = activeProjects.value[projectIdx];
  if (project) task.value.space = project.space;

  return createTask(task.value)
    .then((json) => {
      dialog.value = false;
      router.push({ name: "task", params: { task_id: json.data.id } });
    })
    .catch(() => {
      console.log("error");
    });
}
</script>

<template>
  <v-dialog v-model="dialog" max-width="30%" rounded="lg">
    <template v-slot:activator="{ props }">
      <v-btn variant="plain" prepend-icon="mdi-plus" v-bind="props">
        new task
      </v-btn>
    </template>

    <v-card>
      <v-container>
        <v-card-title>
          <span class="text-h4">New task</span>
        </v-card-title>

        <v-form v-model="valid" @submit.prevent="doCreate">
          <v-container>
            <v-text-field
              color="grey-darken-2"
              label="Title"
              v-model="task.title"
              variant="outlined"
              :rules="titleRules"
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
            <v-btn color="primary" type="submit"> Create </v-btn>
          </v-card-actions>
        </v-form>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
