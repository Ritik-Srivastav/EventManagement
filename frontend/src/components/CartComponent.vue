
<!-- src/views/Cart.vue -->
<template>
    <div>
      <AppHeader :userName="user.name" :userRole="user.role" />
      <button class="btn btn-primary" @click="backToDashboard">Back to Dashboard</button>
      <h1>Cart</h1>
      <div class="row">
        <div class="col-md-4" v-for="(item, index) in cartItems" :key="index">
          <div class="card">
            <h5 class="card-title">{{ item.name }}</h5>
              <p class="card-text">
                Manufacture Date: {{ item.manufacture_date }} <br>
                Expiry Date: {{ item.expiry_date }} <br>
                Available Quantity: {{ item.count }} <br>
                Purchased Quantity: {{ item.purchasedCount }}<br>
                Price: {{ item.price }}
                </p>
                <button class="btn btn-danger" @click="removeFromCart(index)">Remove</button>
            </div>
          </div>
        </div>
        
        <div class="total-price text-center">
          <p>Total Price: {{ totalCartPrice }}</p>
        <button class="btn btn-success" @click="buyProducts">Buy</button>
      </div>
       <!-- Display a success message if the purchase is successful -->
    <div v-if="purchaseStatus === 'success'" class="alert alert-success" role="alert">
      Purchase Successful! Thank you for shopping with us.Continue Your Shopping!
      <button class="btn btn-primary" @click="backToDashboard">Back to Dashboard</button>
    </div>
      </div>
  </template>
  
  <script>
  import AppHeader from './AppHeader.vue';
  export default {
    components: {
      AppHeader, // Register the AppHeader component
    },
    data() {
    return {
      purchaseStatus: null, // Initialize purchase status
    };
  },
    computed: {
      user() {
        // Assuming you have Vuex store getters for user information
        return this.$store.getters.getUser;
      },
      totalCartPrice() {
        // Calculate the total price of purchased products
             // Check if cartItems is defined before using reduce
      return this.cartItems ? this.cartItems.reduce((total, item) => total + (parseFloat(item.price) * item.purchasedCount), 0) : 0;
      },
      cartItems() {
        return this.$store.getters['cart/getCartItems'];
      },
    },
    methods: {
      removeFromCart(index) {
        // Dispatch an action to remove the item from the cart based on the index
        this.$store.dispatch('cart/removeFromCart', index);
      },
      backToDashboard() {
        this.$router.push('/user-dashboard');
      },
      async buyProducts() {
        try {
          // Collect necessary information
          const user = this.user;
          const purchasedItems = this.cartItems.map(item => ({
            product_name: item.name,
            product_count: item.purchasedCount,
            product_price: item.price,
          }));
  
          // Send a request to the server to add purchased items to the Purchased table
          const response = await fetch('http://localhost:5000/buyProducts', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              user_id: user.id,
              user_name: user.name,
              user_email: user.email,
              purchasedItems,
            }),
          });
  
          if (response.ok) {
            console.log('Purchase successful!');
            // Clear the cart after a successful purchase
            this.$store.dispatch('cart/clearCart');
               // Update the purchase status to 'success'
            this.purchaseStatus = 'success';
             // Update the available quantity on the screen
          this.updateAvailableQuantity();
          } else {
            console.error('Failed to complete the purchase');
          }
        } catch (error) {
          console.error('Error during purchase:', error);
          this.purchaseStatus = 'error';
        }
      },
      updateAvailableQuantity() {
      // Dispatch an action to update the available quantity in the store
      this.cartItems.forEach(item => {
        this.$store.dispatch('cart/updateAvailableQuantity', {
          product_id: item.id, // Add the product ID or a unique identifier
          available_quantity: item.count - item.purchasedCount,
        });
      });
    },
    },
  };
  </script>
  <style scoped>
  
  </style>
  
  