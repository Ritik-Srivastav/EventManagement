<!-- src/components/AdminDashboard.vue -->
<template>
  <div>
    <!-- Include the AppHeader component and pass the user information -->
    <AppHeader :userName="user.name" :userRole="user.role" />

    <!-- Display vendors -->
    <div>
      <h2>Vendors</h2>
      <ul>
        <li v-for="vendor in vendors" :key="vendor.id">
          {{ vendor.name }} - {{ vendor.email }}
          <button @click="handleMembership(vendor.id, 'vendor')">Add Membership</button>
          <button @click="handleUpdateMembership(vendor.id, 'vendor')">Remove Membership</button>
        </li>
      </ul>
    </div>

    <!-- Display regular users -->
    <div>
      <h2>Regular Users</h2>
      <ul>
        <li v-for="user in regularUsers" :key="user.id">
          {{ user.name }} - {{ user.email }}
          <button @click="handleMembership(user.id, 'user')">Add Membership</button>
          <button @click="handleUpdateMembership(user.id, 'user')">Remove Membership</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
// Import the AppHeader component
import AppHeader from './AppHeader.vue';
import axios from 'axios';

export default {
  components: {
    AppHeader, // Register the AppHeader component
  },
  computed: {
    user() {
      // Assuming you have Vuex store getters for user information
      return this.$store.getters.getUser;
    },
    vendors() {
      // Assuming you have Vuex store getters for vendors information
      return this.$store.getters.getVendors;
    },
    regularUsers() {
      // Assuming you have Vuex store getters for regular users information
      return this.$store.getters.getRegularUsers;
    },
  },
  mounted() {
    // Fetch users when the component is mounted
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      // Make an API request to fetch users
      // Assuming you have Axios or another HTTP library installed
      axios.get('http://localhost:5000/getUsersByRole')
        .then(response => {
          // Update Vuex store with the fetched users
          this.$store.commit('setVendors', response.data.vendors);
          this.$store.commit('setRegularUsers', response.data.regularUsers);
        })
        .catch(error => {
          console.error('Error fetching users:', error);
        });
    },
    handleMembership(userId) {
      // Make an API request to add membership
      axios.post('http://localhost:5000/update-membership', { user_id: userId })
        .then(response => {
          console.log(response.data.message);
          alert('Membership Added successfully!');
          // Optionally, you can update the user's membership status in the Vuex store
        })
        .catch(error => {
          console.error('Error updating membership:', error);
        });
    },
    handleUpdateMembership(userId,) {
      // Make an API request to remove membership
      axios.post('http://localhost:5000/remove-membership', { user_id: userId })
        .then(response => {
          console.log(response.data.message);
          alert('Membership Removed successfully!');
          // Optionally, you can update the user's membership status in the Vuex store
        })
        .catch(error => {
          console.error('Error updating membership:', error);
        });
    },
  },
};
</script>

