
import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    user: null,
    vendors: [],
    regularUsers: [],
    userInteractions: [], // Store user interactions (e.g., search and cart additions)
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setVendors(state, vendors) {
      state.vendors = vendors;
    },
    setRegularUsers(state, regularUsers) {
      state.regularUsers = regularUsers;
    },
    addInteraction(state, interaction) {
      state.userInteractions.push(interaction);
    },
  },
  actions: {
    setUser({ commit, dispatch }, user) {
      // Clear the cart when the user logs in or logs out
      dispatch('cart/clearCart');

      commit('setUser', user);

      // You can also add additional logic here if needed for when the user logs in
      // For example, fetch user data or perform other actions.
    },
    recordInteraction({ commit }, interaction) {
      commit('addInteraction', interaction);
    },
    fetchUsersByRole({ commit }) {
      // Make an API request to fetch users by role
      axios.get('/getUsersByRole')
        .then(response => {
          // Update Vuex store with the fetched users
          commit('setVendors', response.data.vendors);
          commit('setRegularUsers', response.data.regularUsers);
        })
        .catch(error => {
          console.error('Error fetching users by role:', error);
        });
    },
  },
  getters: {
    getUser: (state) => state.user,
    getVendors: (state) => state.vendors,
    getRegularUsers: (state) => state.regularUsers,
    getUserInteractions: (state) => state.userInteractions,
  },
  modules: {
    cart: {
      namespaced: true,
      state: {
        items: [],
      },
      mutations: {
        addToCart(state, product) {
          state.items.push(product);
          localStorage.setItem('cart', JSON.stringify(state.items));
        },
        removeFromCart(state, index) {
          state.items.splice(index, 1);
          localStorage.setItem('cart', JSON.stringify(state.items));
        },
        clearCart(state) {
          state.items = [];
          localStorage.removeItem('cart');
        },
      },
      actions: {
        addToCart({ commit }, product) {
          commit('addToCart', product);
        },
        removeFromCart({ commit }, index) {
          commit('removeFromCart', index);
        },
        clearCart({ commit }) {
          commit('clearCart');
        },
      },
      getters: {
        getCartItems: (state) => state.items,
      },
    },
  },
});
