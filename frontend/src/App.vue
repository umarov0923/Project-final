<script setup lang="ts">
import { useAuthStore } from './stores/auth';
import { useRoute } from 'vue-router';
import { ref, watchEffect } from 'vue';
import {
  UserGroupIcon,
  CurrencyDollarIcon,
  CreditCardIcon,
  ArrowLeftOnRectangleIcon
} from '@heroicons/vue/24/outline';

const authStore = useAuthStore();
const route = useRoute();
const showMenu = ref(true);


watchEffect(() => {
  showMenu.value = route.path !== '/login', route.path !== '/register' && true;
});
</script>

<template>
  <header v-if="showMenu" class="app-header">
    <nav v-if="authStore.accessToken" class="main-nav">
      <div class="nav-brand">
        <a href ="/">
        <span class="logo">💼</span>
        <span class="app-name">Главная (финансы)</span>
        </a>
      </div>
      
      <div class="nav-links">
        <RouterLink 
          to="/clients" 
          class="nav-link"
          :class="{ active: route.path === '/clients' }"
        >
          <UserGroupIcon class="nav-icon" />
          <span>Клиенты</span>
        </RouterLink>
        
        <RouterLink 
          to="/debts" 
          class="nav-link"
          :class="{ active: route.path === '/debts' }"
        >
          <CurrencyDollarIcon class="nav-icon" />
          <span>Долги</span>
        </RouterLink>
        
        <RouterLink 
          to="/payments" 
          class="nav-link"
          :class="{ active: route.path === '/payments' }"
        >
          <CreditCardIcon class="nav-icon" />
          <span>Платежи</span>
        </RouterLink>
      </div>

      <button @click="authStore.logout" class="logout-btn">
        <ArrowLeftOnRectangleIcon class="nav-icon" />
        <span>Выход</span>
      </button>
    </nav>
  </header>

  <RouterView />
</template>


<style scoped>
.app-header {
  background: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.main-nav {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logo {
  font-size: 1.8rem;
}

.app-name {
  font-size: 1.4rem;
  font-weight: 600;
  color: #1f2937;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  flex-grow: 1;
  justify-content: center;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  color: #4b5563;
  text-decoration: none;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background: #f3f4f6;
  color: #1f2937;
}

.nav-link.active {
  background: #e0f2fe;
  color: #0ea5e9;
  font-weight: 500;
}

.nav-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  background: #fef2f2;
  color: #dc2626;
  border: none;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #fee2e2;
}

@media (max-width: 768px) {
  .main-nav {
    flex-direction: column;
    padding: 1rem;
    gap: 1rem;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link, .logout-btn {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
}
</style>