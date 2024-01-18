<template>
  <nav
    class="navbar navbar-expand-lg navbar-light bg-light"
    style="position: sticky"
  >
    <div class="container">
      <router-link class="navbar-brand" to="/">TicketShow</router-link>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav ms-auto">
          <div class="navitems" v-if="loggedin">
            <router-link
              v-if="isadmin"
              class="nav-item nav-link"
              to="/adminactions"
              >Admin Actions</router-link
            >
            <router-link class="nav-item nav-link" to="/"
              >Book Tickets</router-link
            >
            <router-link class="nav-item nav-link" to="/bookinghistory"
              >Booking History</router-link
            >
            <a @click="logout"> logout </a>
          </div>
          <div class="navitems" v-else>
            <router-link class="nav-item nav-link" to="/login"
              >Login</router-link
            >
            <router-link class="nav-item nav-link" to="/register"
              >Register</router-link
            >
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import UserMixin from "../mixins/userMixin";

export default {
  mixins: [UserMixin],
};
</script>

<style>
.navitems {
  display: flex;
  align-items: center;
}

.navitems a {
  margin-left: 15px;
}
</style>
