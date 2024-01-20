<template>
  <div class="container mt-5">
    <h2>Add Show to {{ theatre.name }}</h2>
    <form @submit.prevent="addShow">
      <div class="form-group">
        <label for="name">Show Name:</label>
        <input
          type="text"
          id="name"
          v-model="show.name"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="tags">Tags:</label>
        <input type="text" id="tags" v-model="show.tags" class="form-control" />
      </div>
      <div class="form-group">
        <label for="date">Date:</label>
        <input
          type="date"
          id="date"
          v-model="show.date"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="start_time">Start Time:</label>
        <input
          type="time"
          id="start_time"
          v-model="show.start_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="end_time">End Time:</label>
        <input
          type="time"
          id="end_time"
          v-model="show.end_time"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="price">Price:</label>
        <input
          type="number"
          id="price"
          v-model="show.price"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Add Show</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theatre: {},
      show: {
        name: "",
        tags: "",
        date: "",
        start_time: "",
        end_time: "",
        price: "",
      },
    };
  },
  async created() {
    const theatreId = this.$route.params.theatreId;
    await this.fetchTheatreData(theatreId);
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
    async addShow() {
      try {
        const accessToken = localStorage.getItem("access_token");
        const theatreId = this.theatre.id;

        const response = await fetch(
          `http://localhost:5000/theatres/${theatreId}/shows`,
          {
            method: "POST",
            headers: {
              Authorization: `Bearer ${accessToken}`,
              "Content-Type": "application/json",
            },
            body: JSON.stringify(this.show),
          }
        );

        if (!response.ok) {
          throw new Error("Error adding show");
        }

        const data = await response.json();
        console.log("Show added successfully:", data);
        alert("Show added successfully:");
        this.$router.push(`/view-theatre/${theatreId}/shows`);
      } catch (error) {
        console.error("Error adding show:", error);
      }
    },
  },
};
</script>

<style scoped>
/* Your component styles go here */
</style>
