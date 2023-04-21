export const routes = [
  {
    path: "/reviews/daily/",
    name: "daily_review",
    component: () => import("../views/reviews/DailyReviewView.vue"),
  },
  {
    path: "/reviews/weekly/",
    name: "weekly_review",
    component: () => import("../views/reviews/WeeklyReviewView.vue"),
  },
  {
    path: "/reviews/monthly/",
    name: "monthly_review",
    component: () => import("../views/reviews/MonthlyReviewView.vue"),
  },
  {
    path: "/reviews/yearly/",
    name: "yearly_review",
    component: () => import("../views/reviews/YearlyReviewView.vue"),
  },
];
