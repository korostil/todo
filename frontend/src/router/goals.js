export const routes = [
  {
    path: "/goals/",
    name: "goal_list",
    component: () => import("../views/goals/GoalListView.vue"),
  },
];
