<template>
  <div class="container my-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center">Edit Theatre</h2>
            <form @submit.prevent="updateTheatre">
              <div class="mb-3">
                <label for="name" class="form-label">Name</label>
                <input
                  type="text"
                  id="name"
                  class="form-control"
                  v-model="name"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="place" class="form-label">Place</label>
                <input
                  type="text"
                  id="place"
                  class="form-control"
                  v-model="place"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="location" class="form-label">Location</label>
                <input
                  type="text"
                  id="location"
                  class="form-control"
                  v-model="location"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="capacity" class="form-label">Capacity</label>
                <input
                  type="number"
                  id="capacity"
                  class="form-control"
                  v-model="capacity"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary btn-block">
                Update Theatre
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      theatreId: null,
      name: "",
      place: "",
      location: "",
      capacity: "",
    };
  },
  created() {
    this.theatreId = this.$route.params.theatreId;
    this.fetchTheatreData();
  },
  methods: {
    fetchTheatreData() {
      const accessToken = localStorage.getItem("access_token");
      fetch(`http://localhost:5000/theatres/${this.theatreId}`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data);
          this.name = data.name;
          this.place = data.place;
          this.location = data.location;
          this.capacity = data.capacity;
        })
        .catch((error) => {
          console.error("Fetch theatre data error:", error);
          this.errorMessage =
            "Error fetching theatre data. Please try again later.";
        });
    },
    updateTheatre() {
      const accessToken = localStorage.getItem("access_token");
      fetch(`http://localhost:5000/theatres/${this.theatreId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          name: this.name,
          place: this.place,
          location: this.location,
          capacity: this.capacity,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error updating theatre");
          }
          return response.json();
        })
        .then((data) => {
          console.log(data);
          this.$router.push("/all-theatres");
        })
        .catch((error) => {
          console.error("Update theatre error:", error);
          this.errorMessage = "Error updating theatre. Please try again later.";
        });
    },
  },
};
</script>

<style></style>
