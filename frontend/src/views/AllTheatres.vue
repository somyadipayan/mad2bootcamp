<template>
  <div>
    <h2>All Theatres</h2>
    <router-link to="/create-theatre" class="btn btn-primary"
      >Add a Theatre</router-link
    >
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Place</th>
          <th>Location</th>
          <th>Capacity</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="theatre in theatres" :key="theatre.id">
          <td>{{ theatre.name }}</td>
          <td>{{ theatre.place }}</td>
          <td>{{ theatre.location }}</td>
          <td>{{ theatre.capacity }}</td>
          <td>
            <router-link
              :to="`view-theatre/${theatre.id}/shows`"
              class="btn btn-primary mr-2"
              >View</router-link
            >
            <router-link
              :to="`edit-theatre/${theatre.id}`"
              class="btn btn-success mr-2"
              >Edit</router-link
            >
            <button
              @click="deleteTheatre(theatre.id, theatre.name)"
              class="btn btn-danger"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theatres: [],
    };
  },
  created() {
    this.fetchTheatres();
  },
  methods: {
    fetchTheatres() {
      fetch("http://localhost:5000/theatres", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.theatres = data.data;
          console.log(this.theatres);
        })
        .catch((error) => {
          console.error("Error fetching theatres:", error);
        });
    },
    deleteTheatre(theatreId, theatrename) {
      const confirmed = window.confirm(`Are you sure to delete ${theatrename}`);
      if (!confirmed) {
        return;
      }
      fetch(`http://localhost:5000/theatres/${theatreId}`, {
        method: "DELETE",
        headers: {
          Authorization: "Bearer " + localStorage.getItem("access_token"),
          "Content-Type": "application/json",
        },
      }).then((response) => {
        if (!response.ok) {
          throw new Error("Error Deleting theatre");
        }
      });
      console.log(`${theatreId} Deleted`);
      this.$router.go();
    },
  },
};
</script>

<style scoped></style>
