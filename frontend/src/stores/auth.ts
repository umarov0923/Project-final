import { defineStore } from 'pinia';
import axios from 'axios';
import router from '@/router'; // <--- Добавь этот импорт

interface User {
  id: string;
  email: string;
  user_roles: string;
  full_name: string;
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    accessToken: localStorage.getItem('accessToken') || '',
  }),

  actions: {
    setUser(user: User) {
      this.user = user;
    },

    setToken(token: string) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
      this.fetchUser();
    },

    async fetchUser() {
      if (!this.accessToken) {
        this.user = null;
        this.logout();
      }
      try {
        const response = await axios.get('/user/me', {
          headers: { Authorization: `Bearer ${this.accessToken}` },
        });
        this.user = response.data;
      } catch (error) {
        console.error('Ошибка загрузки пользователя', error);
        this.logout();
      }
    },

    async logout() {
      this.user = null;
      this.accessToken = '';
      localStorage.removeItem('accessToken');
      await router.push('/login'); // <-- Перенаправление после выхода
    },
  },
});
