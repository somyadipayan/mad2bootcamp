import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import RegisterPage from "../views/RegisterPage.vue";
import LoginPage from "../views/LoginPage.vue";
import CreateTheatre from "../views/CreateTheatre.vue";
import AllTheatres from "../views/AllTheatres.vue";
import EditTheatre from "../views/EditTheatre.vue";
import ViewTheatre from "../views/ViewTheatre.vue";
import AddShow from "../views/AddShow.vue";

function checkAuth(to, from, next) {
  const access_token = localStorage.getItem("access_token");
  if (!access_token) {
    next("/login");
  } else {
    fetch("http://localhost:5000/fetchuserinfo", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${access_token}`,
      },
    })
      .then((response) => response.json())
      .then((data) => {
        const isadmin = data.is_admin;
        if (!isadmin) {
          next("/");
        } else {
          next();
        }
      })
      .catch((error) => {
        console.error("Some Error Ocuured:", error);
        next("/");
      });
  }
}

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
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: "/all-theatres",
    name: "all-theatres",
    component: AllTheatres,
    meta: { requiresAuth: true },
    beforeEnter: checkAuth,
  },
  {
    path: "/edit-theatre/:theatreId",
    name: "edit-theatre",
    component: EditTheatre,
  },
  {
    path: "/view-theatre/:theatreId/shows",
    name: "view-theatre",
    component: ViewTheatre,
  },
  {
    path: "/addshow/:theatreId",
    name: "addshow",
    component: AddShow,
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
