export default {
  data() {
    return {
      user: null,
      isadmin: false,
      loggedin: false,
    };
  },
  async created() {
    await this.checklogin();
  },
  methods: {
    async checklogin() {
      const access_token = localStorage.getItem("access_token");
      if (!access_token) {
        this.loggedin = false;
        this.isadmin = false;
        return;
      }
      try {
        this.user = await this.fetchuserinfo(access_token);
        this.loggedin = true;
        if (this.user.is_admin) {
          this.isadmin = true;
        }
      } catch (error) {
        console.error("Error fetching user info:", error);
        this.loggedin = false;
      }
    },
    async fetchuserinfo(access_token) {
      const response = await fetch("http://localhost:5000/fetchuserinfo", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });
      if (response.status === 401) {
        this.loggedin = false;
        return null;
      }
      return await response.json();
    },
    logout() {
      fetch("http://localhost:5000/logout", {
        method: "POST",
        credentials: "include",
      })
        .then(() => {
          localStorage.removeItem("access_token");
          this.user = null;
          this.loggedin = false;
          this.$router.push("/login");
        })
        .catch((error) => {
          console.error("Logout error:", error);
        });
    },
  },
};
