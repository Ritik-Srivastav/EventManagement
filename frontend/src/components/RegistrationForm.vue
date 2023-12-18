<template>
  <div class="container mt-5" style="margin-left: 400px;">
    <div class="row">
      <!-- Form Column -->
      <div class="col-md-6">
        <h1 class="mb-4">Registration Page</h1>
        <form @submit.prevent="registerUser">
          <div class="mb-3">
            <label for="name" class="form-label">Name:</label>
            <input type="text" class="form-control" v-model="name" required />
          </div>

          <div class="mb-3">
            <label for="email" class="form-label">Email:</label>
            <input type="email" class="form-control" v-model="email" required />
          </div>

          <div class="mb-3">
            <label for="address" class="form-label">Address:</label>
            <input type="text" class="form-control" v-model="address" required />
          </div>

          <div class="mb-3">
            <label for="password" class="form-label">Password:</label>
            <input type="password" class="form-control" v-model="password" required />
          </div>

          <button type="submit" class="btn btn-primary">Register</button>
        </form>
        <p class="mt-3">Already have an account? <router-link to="/login">Login</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      name: '',
      email: '',
      address: '',
      password: '',
    };
  },
  methods: {
    registerUser() {
      // Implement API call to register user using Axios
      axios.post('http://localhost:5000/register', {
        name: this.name,
        email: this.email,
        address: this.address,
        password: this.password,
      })
      .then(response => {
        console.log(response.data);  // Handle success response
        this.$router.push('/login');
      })
      .catch(error => {
        console.error(error.response.data);  // Handle error response
      });
    },
  },
};
</script>
