
<!-- src/components/report.vue -->
<template>
  <div>
    <AppHeader :userName="user.name" :userRole="user.role" />

    <div>
      <h2>Product Report</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Manufacture Date</th>
            <th>Expiry Date</th>
            <th>Count</th>
            <th>Price</th>
            <th>Section ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in products" :key="product.id">
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.manufacture_date }}</td>
            <td>{{ product.expiry_date }}</td>
            <td>{{ product.count }}</td>
            <td>{{ product.price }}</td>
            <td>{{ product.section_id }}</td>
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
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://localhost:5000/getProducts');
        this.products = response.data.products;
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
  },
};
</script>
