<template>
  <div>
      <!-- Include the AppHeader component and pass the user information -->
     <AppHeader :userName="user.name" :userRole="user.role" />
     <div>
     <button class="btn btn-info position-absolute top-10 end-0" @click="goToCart">Go to Cart</button>      
          <h1><b>User Services</b></h1>
          <router-link to="/user-membership">
            <button class="btn btn-primary">User Membership</button><br>
          </router-link>
       <router-link to="/reports">
        <button class="btn btn-primary">Reports</button><br>
      </router-link>
      <router-link to="/transactions">
        <button class="btn btn-primary">Transactions</button>
      </router-link>

    </div>
    
    <div class="col-md-12 text-center mx-auto mt-5">
       <input type="text" v-model="searchQuery" placeholder="Search by name, price, or count" />
         <button class="btn btn-primary" @click="searchProducts">Search</button>
     </div>
     <div>
      </div>
     <div class="row mt-4">
      <div class="col-md-4" v-for="(product, index) in products" :key="index">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">
              Manufacture Date: {{ product.manufacture_date }} <br>
              Expiry Date: {{ product.expiry_date }} <br>
              Available Quantity: {{ product.count }} <br>
              Price: {{ product.price }}
            </p>
            <button
             class="btn btn-primary"
             @click="promptPurchasedCount(product)"
             :disabled="product.count === 0"
             >
             {{ product.count === 0 ? 'Out of Stock' : 'Add To Cart' }}
    </button>
          </div>
        </div>
      </div>
    </div><hr>
   </div>
</template>

<script>
import AppHeader from './AppHeader.vue';

export default {
  data() {
    
    return {
      sectionName: "",
      sections: [], // Array to store added sections
      productName: "",
      manufactureDate: "",
      expiryDate: "",
      count: 0,
      price: 0,
      selectedSection: null,
      products: [],
      searchQuery: "",
    };
  },
  methods: {
    goToCart() {
      // Navigate the user to the cart page
      this.$router.push('/cart');
    },
    promptPurchasedCount(product) {
      const purchasedCount = parseInt(prompt(`Enter the quantity for ${product.name}`));
      if (!isNaN(purchasedCount) && purchasedCount <= product.count && purchasedCount>=1) {
        // Valid purchasedCount, add to cart
        this.addToCart(product, purchasedCount);
      } else {
        alert(`Invalid quantity. Maximum allowed quantity is ${product.count} and Minimum allowed quantity is 1`);
      }
    },
    addToCart(product, purchasedCount) {
      this.$store.dispatch('cart/addToCart', { ...product, purchasedCount });

      // Record the interaction
      this.$store.dispatch('recordInteraction', {
        type: 'cartAddition',
        productId: product.id,
      });

      this.$router.push('/cart');
    },


    async backToDashboard() {
  // Reset search-related variables
  this.searchQuery = '';

  // Clear the cart and set the user to null (logout)
  this.$store.dispatch('setUser', null);

  // Fetch the original list of products and wait for it to complete
  await this.fetchProducts();

  // Now, you can navigate to the next route
  this.$router.push('/user-dashboard');
},
async searchProducts() {
      try {
        const response = await fetch(`http://localhost:5000/searchProducts?query=${this.searchQuery}`);
        if (response.ok) {
          const data = await response.json();
          this.products = data.products;

          // Record the interaction
          this.$store.dispatch('recordInteraction', {
            type: 'search',
            query: this.searchQuery,
          });
        } else {
          console.error('Failed to fetch products');
        }
      } catch (error) {
        console.error('Error fetching products:', error);
      }
    },
    async fetchProducts() {
      try {
        const response = await fetch("http://localhost:5000/getProducts");
        if (response.ok) {
          const data = await response.json();
          this.products = data.products;
        } else {
          console.error("Failed to fetch products");
        }
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    },

    async editProduct(product) {
      try {
        const newName = prompt("Enter the new name for the product", product.name);
        const newManufactureDate = prompt("Enter the new manufacture date (YYYY-MM-DD)", product.manufacture_date);
        const newExpiryDate = prompt("Enter the new expiry date (YYYY-MM-DD)", product.expiry_date);
        const newCount = parseInt(prompt("Enter the new count", product.count));
        const newPrice = parseFloat(prompt("Enter the new price", product.price));

        if (newName !== null && newManufactureDate !== null && newExpiryDate !== null && !isNaN(newCount) && !isNaN(newPrice)) {
          const response = await fetch(`http://localhost:5000/editProduct/${product.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              name: newName,
              manufacture_date: newManufactureDate,
              expiry_date: newExpiryDate,
              count: newCount,
              price: newPrice,
            }),
          });

          if (response.ok) {
            console.log("Product edited successfully");
            // Optionally, you can update the products array to reflect the changes
            await this.fetchProducts();
          } else {
            console.error("Failed to edit product");
          }
        }
      } catch (error) {
        console.error("Error editing product:", error);
      }
    },

    async deleteProduct(product) {
      try {
        const confirmDelete = confirm(`Are you sure you want to delete ${product.name}?`);

        if (confirmDelete) {
          const response = await fetch(`http://localhost:5000/deleteProduct/${product.id}`, {
            method: "DELETE",
          });

          if (response.ok) {
            console.log("Product deleted successfully");
            // Optionally, you can update the products array to reflect the changes
            await this.fetchProducts();
          } else {
            console.error("Failed to delete product");
          }
        }
      } catch (error) {
        console.error("Error deleting product:", error);
      }
    },

    async addProduct() {
      try {
        const response = await fetch("http://localhost:5000/addProduct", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: this.productName,
            manufacture_date: this.manufactureDate,
            expiry_date: this.expiryDate,
            count: this.count,
            price: this.price,
            section_id: this.selectedSection,
          }),
        });

        if (response.ok) {
          console.log("Product added successfully");

          // Optionally, you can reset the form fields
          this.productName = "";
          this.manufactureDate = "";
          this.expiryDate = "";
          this.count = 0;
          this.price = 0;
          this.selectedSection = null;

          // Fetch and update the products array to display the added product
          await this.fetchProducts();
        } else {
          console.error("Failed to add product");
        }
      } catch (error) {
        console.error("Error adding product:", error);
      }
    },

    async addSection() {
      try {
        const response = await fetch("http://localhost:5000/addSection", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ name: this.sectionName }),
        });

        if (response.ok) {
          console.log("Section added successfully");

          // Reset the sectionName after successfully adding a section
          this.sectionName = "";

          // Fetch and update the sections array to display the added sections
          await this.fetchSections();
        } else {
          console.error("Failed to add section");
        }
      } catch (error) {
        console.error("Error adding section:", error);
      }
    },
    async fetchSections() {
      try {
        const response = await fetch("http://localhost:5000/getSections");
        if (response.ok) {
          const data = await response.json();
          this.sections = data.sections;
        } else {
          console.error("Failed to fetch sections");
        }
      } catch (error) {
        console.error("Error fetching sections:", error);
      }
    },
    async editSection(section) {
      try {
        const newName = prompt("Enter the new name for the section", section.name);

        if (newName !== null) {
          const response = await fetch(`http://localhost:5000/editSection/${section.id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ name: newName }),
          });

          if (response.ok) {
            console.log("Section edited successfully");
            // Update the sections array to reflect the changes
            await this.fetchSections();
          } else {
            console.error("Failed to edit section");
          }
        }
      } catch (error) {
        console.error("Error editing section:", error);
      }
    },

    async deleteSection(section) {
      try {
        const confirmDelete = confirm(`Are you sure you want to delete ${section.name}?`);

        if (confirmDelete) {
          const response = await fetch(`http://localhost:5000/deleteSection/${section.id}`, {
            method: "DELETE",
          });

          if (response.ok) {
            console.log("Section deleted successfully");
            // Update the sections array to reflect the changes
            await this.fetchSections();
          } else {
            console.error("Failed to delete section");
          }
        }
      } catch (error) {
        console.error("Error deleting section:", error);
      }
    },
  },
  mounted() {
    // Fetch sections when the component is mounted
    this.fetchSections();
     // Fetch products when the component is mounted
     this.fetchProducts();
  },
  components: {
    AppHeader, // Register the AppHeader component
  },
  computed: {
    user() {
      // Assuming you have Vuex store getters for user information
      return this.$store.getters.getUser;
    },
    filteredProducts() {
    const query = this.searchQuery.toLowerCase();

    return this.products.filter((product) => {
      return (
        product.name.toLowerCase().includes(query) ||
        product.price.toString().includes(query) ||
        product.count.toString().includes(query)
      );
    });
  },
  },
};
</script>

<style scoped>
/* Add your component styles here */
</style>
