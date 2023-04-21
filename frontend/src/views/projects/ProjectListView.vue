<script setup>
import { ref } from "vue";
import ProjectList from "@/components/ProjectList.vue";
import ButtonNewProject from "@/components/ButtonNewProject.vue";
import { space } from "@/store/services/globals";

const refArchived = ref(null);
</script>

<template>
  <v-app id="app">
    <the-header></the-header>

    <v-main>
      <v-container>
        <v-row>
          <v-spacer></v-spacer>
          <v-col cols="12" sm="6">
            <v-sheet rounded="lg">
              <v-container>
                <v-container>
                  <v-row>
                    <button-new-project></button-new-project>

                    <v-spacer></v-spacer>

                    <v-btn-toggle v-model="refArchived" active-color="primary">
                      <v-btn icon="mdi-progress-check" :value="false"></v-btn>
                      <v-btn icon="mdi-archive-outline" :value="true"></v-btn>
                    </v-btn-toggle>
                  </v-row>
                </v-container>
                <!-- TODO show all tasks view with predefined filter by project -->
                <project-list
                  :archived="refArchived"
                  :space="space"
                  :show-description="true"
                ></project-list>
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
