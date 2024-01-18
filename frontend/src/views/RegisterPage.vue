<template>
  <div class="container my-5">
    <div class="col-md-6">
      <div class="card">
        <div class="card-body">
          <h2 class="card-title text-center">REGISTER</h2>
          <form @submit.prevent="signup">
            <div class="mb-2">
              <label for="name" class="form-label">Name</label>
              <input
                type="text"
                id="name"
                class="form-control"
                v-model="name"
                required
              />
            </div>
            <div class="mb-2">
              <label for="email" class="form-label">Email</label>
              <input
                type="email"
                id="email"
                class="form-control"
                v-model="email"
                required
              />
            </div>
            <div class="mb-2">
              <label for="city" class="form-label">city</label>
              <input
                type="text"
                id="city"
                class="form-control"
                v-model="city"
              />
            </div>
            <div class="mb-2">
              <label for="password" class="form-label">password</label>
              <input
                type="password"
                id="password"
                class="form-control"
                v-model="password"
                required
              />
            </div>
            <div class="mb-2">
              <label for="is_admin" class="form-label">Is admin?</label>
              <input
                type="radio"
                id="is_admin"
                v-model="is_admin"
                name="is_admin"
                :value="true"
              />
            </div>
            <button type="submit" class="btn btn-primary">Register</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: "",
      email: "",
      city: "",
      password: "",
      is_admin: false,
    };
  },
  methods: {
    async signup() {
      const formdata = {
        email: this.email,
        name: this.name,
        city: this.city,
        password: this.password,
        is_admin: this.is_admin,
      };
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        });
        console.log(formdata);
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          // push to login
          this.$router.push("/about");
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Registration error:", error);
        alert("An error occurred while attempting to register.");
      }
    },
  },
};
</script>

<style scoped></style>
