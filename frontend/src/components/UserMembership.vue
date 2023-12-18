
<template>
  <div>
    <AppHeader :userName="user.name" :userRole="user.role" />
    <h2>Membership</h2>

    <div>
      <label>
        <input
          type="radio"
          v-model="selectedDuration"
          value="6 months"
          @change="updatePrice"
        />
        6 months - $500
      </label>
    </div>

    <div>
      <label>
        <input
          type="radio"
          v-model="selectedDuration"
          value="1 year"
          @change="updatePrice"
        />
        1 year - $900
      </label>
    </div>

    <div>
      <label>
        <input
          type="radio"
          v-model="selectedDuration"
          value="2 years"
          @change="updatePrice"
        />
        2 years - $1300
      </label>
    </div>

    <button @click="purchaseMembership">Purchase</button>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import axios from 'axios';

export default {
  components: {
    AppHeader,
  },
  computed: {
    user() {
      return this.$store.getters.getUser;
    },
  },
  data() {
    return {
      selectedDuration: '6 months',
      price: 500,
    };
  },
  methods: {
    updatePrice() {
      switch (this.selectedDuration) {
        case '6 months':
          this.price = 500;
          break;
        case '1 year':
          this.price = 900;
          break;
        case '2 years':
          this.price = 1300;
          break;
        default:
          this.price = 500;
      }
    },
    purchaseMembership() {
      const data = {
        user_id: this.user.id,
        selected_duration: this.selectedDuration,
        price: this.price,
      };

      // Make a POST request to the Flask server
      axios.post('http://localhost:5000/update-membership', data)
        .then(response => {
          console.log(response.data);
          // Show a success message to the user
          alert('Membership purchased successfully!');
        })
        .catch(error => {
          console.error(error);
          // Show an error message to the user
          alert('Failed to purchase membership.');
        });
    },
  },
};
</script>

<style scoped>
/* Add your component styles here */
</style>
