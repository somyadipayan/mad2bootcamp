<template>
  <div class="login-container">
    <form @submit.prevent="login" class="login-form">
      <h2>Login</h2>
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          v-model="email"
          type="email"
          id="email"
          class="form-control"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          v-model="password"
          type="password"
          id="password"
          class="form-control"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    async login() {
      const formdata = {
        email: this.email,
        password: this.password,
      };
      try {
        const response = await fetch("http://localhost:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(formdata),
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
          localStorage.setItem("access_token", data.access_token);
          this.$router.push("/");
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Login error:", error);
        alert("An error occurred while attempting to Login.");
      }
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.login-form {
  max-width: 400px;
  width: 100%;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
