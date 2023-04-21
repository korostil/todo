<script setup>
import ProjectList from "@/components/ProjectList.vue";
import TaskList from "@/components/TaskList.vue";
import ButtonNewProject from "@/components/ButtonNewProject.vue";
import ButtonAllProjects from "@/components/ButtonAllProjects.vue";
import ButtonNewTask from "@/components/ButtonNewTask.vue";
import ButtonAllTasks from "@/components/ButtonAllTasks.vue";
import FocusWeek from "@/components/FocusWeek.vue";
import FocusMonth from "@/components/FocusMonth.vue";
import FocusYear from "@/components/FocusYear.vue";
import ButtonNewGoal from "@/components/ButtonNewGoal.vue";
import ButtonAllGoals from "@/components/ButtonAllGoals.vue";
import { ref } from "vue";
import { space } from "@/store/services/globals";

const projectId = ref(null);

function showProjectTasks(project_id) {
  projectId.value = projectId.value === project_id ? null : project_id;
}
</script>

<template>
  <v-app>
    <the-header></the-header>

    <v-main>
      <v-container>
        <v-row>
          <v-col cols="12" sm="3">
            <v-sheet rounded="lg">
              <v-container>
                <button-new-project></button-new-project>
                <button-all-projects></button-all-projects>
                <project-list
                  :archived="false"
                  :space="space"
                  @project-selected="showProjectTasks"
                ></project-list>
              </v-container>
            </v-sheet>
          </v-col>

          <v-col cols="12" sm="6">
            <v-sheet min-height="90vh" rounded="lg">
              <v-container>
                <button-new-task></button-new-task>
                <button-all-tasks></button-all-tasks>
                <task-list
                  :today="projectId === null"
                  :space="space"
                  :project-id="projectId"
                ></task-list>
              </v-container>
            </v-sheet>
          </v-col>

          <v-col cols="12" sm="3">
            <v-sheet rounded="lg" min-height="268">
              <v-container>
                <button-new-goal></button-new-goal>
                <button-all-goals></button-all-goals>
                <focus-week></focus-week>
                <focus-month></focus-month>
                <focus-year></focus-year>
              </v-container>
            </v-sheet>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<style scoped></style>
