import 'bootstrap/dist/css/bootstrap.min.css';
import { createApp } from 'vue';
import { createRouter, createWebHistory } from 'vue-router'; 
import App from './App.vue';
import UserDashboard from './components/UserDashboard.vue';
import ManagerDashboard from './components/ManagerDashboard.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import LoginForm from './components/LoginForm.vue';
import RegistrationForm from './components/RegistrationForm';
import UserMaintenance from './components/UserMaintenance';
import UserReports from './components/UserReports';
import UserTransactions from './components/UserTransactions';
import UserMembership from './components/UserMembership';
import CartComponent from './components/CartComponent';
import axios from 'axios';
import store from './store'; // Import the Vuex store

const app = createApp(App);

app.config.productionTip = false;

app.config.globalProperties.$axios = axios;

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/register' },
    { path: '/login', component: LoginForm },
    { path: '/register', component: RegistrationForm },
    { path: '/user-dashboard', component: UserDashboard },
    { path: '/manager-dashboard', component: ManagerDashboard },
    { path: '/admin-dashboard', component: AdminDashboard },
    {
      path: '/cart',
      component: CartComponent,
    },
    {
      path: '/maintenance',
      name: 'Maintenance',
      component: () =>  UserMaintenance
    },
    {
      path: '/reports',
      name: 'Reports',
      component: () => UserReports
    },
    {
      path: '/transactions',
      name: 'Transactions',
      component: () => UserTransactions
    },
    {
      path: '/user-membership',
      name: 'UserMembership',
      component: UserMembership,
    },
    // ... other routes
  ],
});

app.use(store);
app.use(router);

app.mount('#app');
