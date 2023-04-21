<script setup>
import { onMounted, ref } from "vue";
import ButtonNewTask from "@/components/ButtonNewTask.vue";
import TaskList from "@/components/TaskList.vue";
import { activeProjects, readProjectList } from "@/store/api/projects";

const refCompleted = ref(null);
const refProjectId = ref(null);

onMounted(() => {
  readProjectList({});
});
</script>

<template>
  <v-app id="app">
    <the-header></the-header>

    <v-main>
      <v-container>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="12" sm="6">
            <v-sheet rounded="lg" min-height="268">
              <v-container>
                <v-container>
                  <v-row>
                    <button-new-task></button-new-task>

                    <v-spacer></v-spacer>

                    <v-select
                      label="Project"
                      v-model="refProjectId"
                      :items="activeProjects"
                      item-title="title"
                      item-value="id"
                      variant="outlined"
                      density="comfortable"
                      clearable
                    ></v-select>

                    <v-btn-toggle v-model="refCompleted" active-color="primary">
                      <v-btn icon="mdi-progress-check" :value="false"></v-btn>
                      <v-btn icon="mdi-check-all" :value="true"></v-btn>
                    </v-btn-toggle>
                  </v-row>
                </v-container>
                <task-list
                  :completed="refCompleted"
                  :project-id="refProjectId"
                ></task-list>
              </v-container>
            </v-sheet>
          </v-col>
          <v-spacer></v-spacer>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped></style>
