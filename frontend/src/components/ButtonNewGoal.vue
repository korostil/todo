<script setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { createGoal } from "@/store/api/goals";
import { monthMap } from "@/store/services/utils/dates";

const dialog = ref(false);
const router = useRouter();
const today = new Date();
const goal = ref({
  month: today.getMonth() + 1,
  year: today.getFullYear(),
});
const selectableYears = [today.getFullYear(), today.getFullYear() + 1];

function doCreate() {
  return createGoal(goal.value)
    .then((json) => {
      router.push({ name: "goal", params: { goal_id: json.data.id } });
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
        new goal
      </v-btn>
    </template>

    <v-card>
      <v-container>
        <v-card-title>
          <span class="text-h4">New goal</span>
        </v-card-title>

        <v-container>
          <v-text-field
            color="grey-darken-2"
            label="Title"
            v-model="goal.title"
            variant="outlined"
          ></v-text-field>
          <v-select
            label="Select"
            :items="monthMap"
            item-title="shortName"
            item-value="value"
            variant="solo"
            v-model="goal.month"
          ></v-select>
          <v-select
            label="Select"
            :items="selectableYears"
            variant="solo"
            v-model="goal.year"
          ></v-select>
        </v-container>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="doCreate"> Create </v-btn>
        </v-card-actions>
      </v-container>
    </v-card>
  </v-dialog>
</template>

<style scoped></style>
