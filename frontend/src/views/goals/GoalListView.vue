<script setup>
import ButtonNewGoal from "@/components/ButtonNewGoal.vue";
import { monthShortNames } from "@/store/services/utils/dates";

const goals_feb = [
  {
    status: 0,
    title: "Something great in February",
    month: monthShortNames[1],
    year: 2023,
  },
  {
    status: 1,
    title: "Something great in February",
    month: monthShortNames[1],
    year: 2023,
  },
];
const goals_sep = [
  {
    status: 0,
    title: "Something great in September",
    month: monthShortNames[8],
    year: 2023,
  },
  {
    status: 1,
    title: "Something great in September",
    month: monthShortNames[8],
    year: 2023,
  },
];
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
                    <button-new-goal></button-new-goal>
                  </v-row>
                </v-container>
                <v-list
                  v-for="(month, idx) in [
                    { goals: goals_feb, name: 'FEBRUARY' },
                    { goals: goals_sep, name: 'SEPTEMBER' },
                  ]"
                  :key="idx"
                >
                  <v-list-subheader>{{ month.name }}</v-list-subheader>
                  <v-list-item
                    v-for="goal in month.goals"
                    :key="goal.id"
                    :title="goal.title"
                    :subtitle="goal.month + ' ' + goal.year"
                    :prepend-icon="
                      goal.status === 1 ? 'mdi-check' : 'mdi-circle-outline'
                    "
                    active-color="primary"
                    rounded="lg"
                    @click="true"
                  >
                  </v-list-item>
                </v-list>
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
