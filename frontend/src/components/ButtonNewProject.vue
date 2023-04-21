<script setup>
import { ref } from "vue";
import { createProject } from "@/store/api/projects";
import { descriptionRules, titleRules } from "@/store/services/rules";
import { PERSONAL_SPACE, WORK_SPACE } from "@/store/services/constants";

const dialog = ref(false),
  valid = ref(false);
const project = ref({ space: PERSONAL_SPACE });

function doCreate() {
  return createProject(project.value)
    .then(() => {
      dialog.value = false;
      project.value = { space: PERSONAL_SPACE };
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
        new project
      </v-btn>
    </template>

    <v-card>
      <v-container>
        <v-card-title>
          <span class="text-h4">New project</span>
        </v-card-title>

        <v-form v-model="valid" @submit.prevent="doCreate">
          <v-container>
            <v-text-field
              color="grey-darken-2"
              label="Title"
              v-model="project.title"
              variant="outlined"
              :rules="titleRules"
              autofocus
            ></v-text-field>
            <v-text-field
              color="grey-darken-2"
              label="Description"
              v-model="project.description"
              variant="outlined"
              :rules="descriptionRules"
            ></v-text-field>
            <v-color-picker
              label="Color"
              v-model="project.color"
            ></v-color-picker>
            <v-text-field
              color="grey-darken-2"
              label="Goal"
              v-model="project.goal_id"
              variant="outlined"
            ></v-text-field>
            <v-btn-toggle
              v-model="project.space"
              active-color="primary"
              mandatory
            >
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
