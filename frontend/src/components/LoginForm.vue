
<template>
  <div class="container mt-5 h-100" >
    <div class="row justify-content-center h-100">
      <div class="col-md-6">
        <h1 class="mb-4">Login Page</h1>
        <!-- Login Form -->
        <form @submit.prevent="loginUser" class="mb-4">
          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" class="form-control" v-model="email" required />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input type="password" class="form-control" v-model="password" required />
          </div>

          <button type="submit" class="btn btn-primary">Login</button>
        </form>

        <!-- Registration Link -->
        <router-link to="/register">Don't have an account? Register here</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    loginUser() {
      axios.post('http://localhost:5000/login', {
        email: this.email,
        password: this.password,
      })
      .then(response => {
        const userData = response.data;

        // Save user data to Vuex store
        this.$store.dispatch('setUser', userData);

        console.log(`Logged in with role ${userData.role}`);

        // Redirect based on the role
        if (userData.role === 0) {
          this.$router.push('/user-dashboard');
        } else if (userData.role === 1) {
          this.$router.push('/manager-dashboard');
        } else if (userData.role === 2) {
          this.$router.push('/admin-dashboard');
        }
      })
      .catch(error => {
        console.error(error.response.data);  // Handle error response
      });
    },
  },
};
</script>