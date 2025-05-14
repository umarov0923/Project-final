<script setup lang="ts">
import { ref } from 'vue';
import api from '../api/index';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const form = ref({ email: '', password: '' });
const error = ref('');
const loading = ref(false); // Флаг загрузки
const authStore = useAuthStore();
const router = useRouter();

const login = async () => {
  error.value = '';
  loading.value = true;

  try {
    const { data } = await api.post('/users/login/', form.value);
    authStore.setToken(data.access);
    authStore.setUser(data.user);
    router.push('/clients');
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Ошибка входа';
  } finally {
    loading.value = false;
  }
};

// Очистка ошибки при вводе
const clearError = () => {
  error.value = '';
};
</script>

<template>
  <div class="login-container">
    <div class="form-card">
      <h1 class="section-header">Авторизация</h1>
      
      <form @submit.prevent="login" class="auth-form">
        <input 
          v-model="form.email" 
          type="email"
          placeholder="Электронная почта"
          class="styled-input"
          @input="clearError"
        >
        
        <input 
          v-model="form.password" 
          type="password"
          placeholder="Пароль"
          class="styled-input"
          @input="clearError"
        >
        
        <button
          type="submit"
          class="gradient-button"
          :disabled="loading"
        >
          <span v-if="loading">Вход...</span>
          <span v-else>Вход</span>
        </button>
        <p> Если Нет Аккаунт<a href="/register">Регистрация</a></p>
        
        <p v-if="error" class="error-message">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<style scoped>
/* Стили остаются без изменений из предыдущего варианта */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background: #f8fafc;
}

.form-card {
  background: white;
  padding: 2.5rem;
  border-radius: 1.5rem;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 420px;
}

.section-header {
  text-align: center;
  font-size: 1.8rem;
  color: var(--dark-gray);
  margin-bottom: 2rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.styled-input {
  width: 100%;
  padding: 1rem;
  border: 2px solid var(--medium-gray);
  border-radius: 0.75rem;
  font-size: 1rem;
  transition: all 0.2s ease;
}

.styled-input:focus {
  border-color: var(--emerald-green);
  outline: none;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.gradient-button {
  background: linear-gradient(135deg, var(--emerald-green) 0%, var(--dark-emerald) 100%);
  color: var(--white);
  padding: 0.75rem 10rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2);
  display: block;
  margin: 1rem auto 0;
  min-width: 160px;
}

.gradient-button:disabled {
  background: #cbd5e1;
  cursor: not-allowed;
  opacity: 0.8;
}

.gradient-button:not(:disabled):hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25);
}

.error-message {
  color: #ef4444;
  font-size: 0.9rem;
  text-align: center;
  margin: 0.5rem 0 0;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background: #fef2f2;
}
</style>
