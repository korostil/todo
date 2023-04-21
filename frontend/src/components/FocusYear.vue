<script setup>
const focus = [
  { title: "Max focus on 1", description: "lorem", is_completed: false },
  { title: "Max focus on 2", description: "ipsum", is_completed: true },
  { title: "Max focus on 3", description: "dios mio", is_completed: false },
];
</script>

<template>
  <v-list>
    <v-list-subheader>YEAR FOCUS</v-list-subheader>
    <v-list-item
      v-for="item in focus"
      :key="item.id"
      :title="item.title"
      :subtitle="item.description"
      :prepend-icon="item.is_completed ? 'mdi-check' : 'mdi-circle-outline'"
      active-color="primary"
      rounded="lg"
      @click="true"
    >
    </v-list-item>
  </v-list>
</template>

<style scoped></style>
