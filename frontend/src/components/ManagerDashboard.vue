<template>
<div>
      <!-- Include the AppHeader component and pass the user information -->
     <AppHeader :userName="user.name" :userRole="user.role" />
    <div class="card-deck mt-4">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">Vendor Services</h5>
          <router-link to="/user-membership">
            <button class="btn btn-primary">Vendor Membership</button><br>
          </router-link>
       <router-link to="/reports">
        <button class="btn btn-primary">Reports</button><br>
      </router-link>
      <router-link to="/transactions">
        <button class="btn btn-primary">Transactions</button>
      </router-link>
     </div>
        </div>
      </div>
    <h2>Add Section</h2>
    <form @submit.prevent="addSection">
      <label for="sectionName">Section Name:</label>
      <input type="text" id="sectionName" v-model="sectionName" required />
      <button type="submit">Add Section</button>
    </form>

    <h2>Sections</h2>
    <ul>
      <li v-for="(section, index) in sections" :key="index">
        {{ section.name }}
        <button @click="editSection(section)">Edit</button>
        <button @click="deleteSection(section)">Delete</button>
      </li>
    </ul>
  </div>
  <div>
    
    <h2>Add Product</h2>
    <form @submit.prevent="addProduct">
      <label for="productName">Product Name:</label>
      <input type="text" id="productName" v-model="productName" required />

      <label for="manufactureDate">Manufacture Date:</label>
      <input type="date" id="manufactureDate" v-model="manufactureDate" required />

      <label for="expiryDate">Expiry Date:</label>
      <input type="date" id="expiryDate" v-model="expiryDate" required />

      <label for="count">Count:</label>
      <input type="number" id="count" v-model="count" required />

      <label for="price">Price:</label>
      <input type="number" id="price" v-model="price" required /><br>

      <label for="section">Section:</label>
      <select id="section" v-model="selectedSection" required>
        <option v-for="section in sections" :key="section.id" :value="section.id">{{ section.name }}</option>
      </select>

      <button type="submit">Add Product</button><br><br>
    </form>

    <h2>Products</h2>
    <div class="row">
      <div class="col-md-4" v-for="(product, index) in products" :key="index">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">
              Manufacture Date: {{ product.manufacture_date }} <br>
              Expiry Date: {{ product.expiry_date }} <br>
              Count: {{ product.count }} <br>
              Price: {{ product.price }}
            </p>
            <button class="btn btn-primary" @click="editProduct(product)">Edit</button>
            <button class="btn btn-danger" @click="deleteProduct(product)">Delete</button>
          </div>
        </div>
      </div>
    </div>
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
    };
  },
  methods: {
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
  },
};
</script>

<style scoped>
/* Add your component styles here */
</style>
