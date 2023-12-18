<!-- src/components/AppHeader.vue -->
<template>
  <header class="app-header">
    <div class="left-section">
      <h1><i>EventManagement</i></h1>
    </div>
    <div class="right-section">
      <p class="welcome-message">Welcome, {{ getRoleDisplayName }} {{ userName }}!</p>
      <button @click="logout" class="logout-button">Logout</button>
    </div>
  </header>
</template>

<script>
export default {
  props: {
    userName: String,
    userRole: Number,
  },
  methods: {
    logout() {
      // Dispatch the 'logout' action to clear the user state
      this.$store.dispatch('logout');

      // Redirect the user to the login page
      this.$router.push('/login');
      
    },
  },
  computed: {
    getRoleDisplayName() {
      switch (this.userRole) {
        case 0:
          return 'User';
        case 1:
          return 'Vendor';
        case 2:
          return 'Admin';
        default:
          return '';
      }
    },
  },
};
</script>

<style scoped>
.app-header {
  background-color: black;
  color: white;
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

.left-section h1 {
  margin: 0;
}

.right-section {
  display: flex;
  align-items: center; /* Center items vertically */
}

.welcome-message {
  margin: 0;
  margin-right: 10px;
}

.logout-button {
  cursor: pointer;
}
</style>
