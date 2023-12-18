
<!-- src/components/transaction.vue -->
<template>
  <div>
    <AppHeader :userName="user.name" :userRole="user.role" />

    <div>
      <h2>Purchased Transactions</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>User Name</th>
            <th>User Email</th>
            <th>Product Name</th>
            <th>Product Count</th>
            <th>Product Price</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="purchase in purchasedData" :key="purchase.id">
            <td>{{ purchase.id }}</td>
            <td>{{ purchase.user_name }}</td>
            <td>{{ purchase.user_email }}</td>
            <td>{{ purchase.product_name }}</td>
            <td>{{ purchase.product_count }}</td>
            <td>{{ purchase.product_price }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import AppHeader from './AppHeader.vue';
import axios from 'axios';

export default {
  components: {
    AppHeader,
  },
  data() {
    return {
      user: {}, // Assuming you have Vuex store getters for user information
      purchasedData: [],
    };
  },
  mounted() {
    this.fetchPurchasedData();
  },
  methods: {
    async fetchPurchasedData() {
      try {
        const response = await axios.get('http://localhost:5000/getPurchasedData');
        this.purchasedData = response.data.purchased_data;
      } catch (error) {
        console.error('Error fetching purchased data:', error);
      }
    },
  },
};
</script>
