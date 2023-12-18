
<template>
  <div>
    <!-- Include the AppHeader component and pass the user information -->
    <AppHeader :userName="user.name" :userRole="user.role" />

    <!-- Navigation cards -->
    <div class="card-deck mt-4">
      <!-- Maintenance Card -->
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Maintenance</h5>
          <p class="card-text">Perform system maintenance tasks.</p>
          <router-link to="/maintenance">
            <button class="btn btn-primary">Go to Maintenance</button>
          </router-link>
        </div>
      </div>

      <!-- Reports Card -->
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Reports</h5>
          <p class="card-text">View detailed reports and analytics.</p>
          <router-link to="/reports">
            <button class="btn btn-primary">Go to Reports</button>
          </router-link>
        </div>
      </div>

      <!-- Transactions Card -->
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Transactions</h5>
          <p class="card-text">Review and manage transaction history.</p>
          <router-link to="/transactions">
            <button class="btn btn-primary">Go to Transactions</button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Import the AppHeader component
import AppHeader from './AppHeader.vue';

export default {
  components: {
    AppHeader, // Register the AppHeader component
  },
  computed: {
    user() {
      // Assuming you have Vuex store getters for user information
      return this.$store.getters.getUser;
    },
  },
};
</script>
