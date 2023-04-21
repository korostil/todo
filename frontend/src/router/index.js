import { createRouter, createWebHistory } from "vue-router";
import { routes as tasks_routes } from "@/router/tasks";
import { routes as projects_routes } from "@/router/projects";
import { routes as goals_routes } from "@/router/goals";
import { routes as reviews_routes } from "@/router/reviews";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "main",
      component: () => import("../views/MainView.vue"),
    },
  ].concat(tasks_routes, projects_routes, goals_routes, reviews_routes),
});

export default router;
