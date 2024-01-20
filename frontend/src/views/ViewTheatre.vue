<template>
  <div class="container mt-4">
    <h2>Theatre {{ this.theatre.name }} Shows</h2>
    <router-link
      v-if="this.isadmin"
      :to="`/addshow/${this.theatreId}`"
      class="btn btn-primary"
      >Add Show</router-link
    >
    <table class="table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Date</th>
          <th>Start Time</th>
          <th>End Time</th>
          <th>Price</th>
          <th v-if="this.isadmin">Sold Tickets</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="show in shows" :key="show.id">
          <td>{{ show.id }}</td>
          <td>{{ show.name }}</td>
          <td>{{ show.date }}</td>
          <td>{{ show.start_time }}</td>
          <td>{{ show.end_time }}</td>
          <td>{{ show.price }}</td>
          <td v-if="this.isadmin">{{ show.sold_ticket_count }}</td>
          <td v-if="this.isadmin">
            <button class="btn btn-primary" @click="editShow(show.id)">
              Edit
            </button>
            <button class="btn btn-danger" @click="deleteShow(show.id)">
              Delete
            </button>
          </td>
          <td v-else>
            <button class="btn btn-primary" @click="bookShow(show.id)">
              BookShow
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import UserMixin from "../mixins/userMixin";

export default {
  mixins: [UserMixin],
  data: function () {
    return {
      theatre: {},
      theatreId: null,
      shows: [],
    };
  },
  async created() {
    this.theatreId = this.$route.params.theatreId;
    await this.fetchTheatreData(this.theatreId);
    await this.fetchShows(this.theatreId);
  },
  methods: {
    async fetchTheatreData(theatreId) {
      try {
        const response = await fetch(
          `http://localhost:5000/theatres/${theatreId}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
          }
        );
        if (!response.ok) {
          throw new Error("Error fetching theatre");
        }
        const data = await response.json();
        this.theatre = data;
      } catch (error) {
        console.error("Error fetching theatre:", error);
      }
    },
    async fetchShows(theatreId) {
      const accessToken = localStorage.getItem("access_token");
      fetch(`http://localhost:5000/theatres/${theatreId}/shows`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.shows = data;
          console.log(this.shows);
        })
        .catch((error) => {
          console.error("Error fetching shows:", error);
        });
    },
    editShow(showId) {
      // Implement the logic for editing a show
      console.log("Edit show with ID:", showId);
    },
    deleteShow(showId) {
      const confirmed = window.confirm(`Are you sure to delete this Show?`);
      if (!confirmed) {
        return;
      }
      fetch(`http://localhost:5000/shows/${showId}`, {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (!response.ok) {
          throw new Error("Error Deleting Show");
        }
      });
    },
    async bookShow(showId) {
      console.log(`Booked Tickets for ${showId}`);
    },
  },
};
</script>

<style></style>
