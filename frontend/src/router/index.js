import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterPage from "../views/RegisterPage.vue";
import LoginPage from "../views/LoginPage.vue";
import CreateTheatre from "../views/CreateTheatre.vue";
import AllTheatres from "../views/AllTheatres.vue";
import EditTheatre from "../views/EditTheatre.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterPage,
  },
  {
    path: "/create-theatre",
    name: "create-theatre",
    component: CreateTheatre,
  },
  {
    path: "/all-theatres",
    name: "all-theatres",
    component: AllTheatres,
  },
  {
    path: "/edit-theatre/:theatreId",
    name: "edit-theatre",
    component: EditTheatre,
  },
  {
    path: "/about",
    name: "about",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/AboutView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
