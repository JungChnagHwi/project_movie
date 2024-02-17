<template>
  <!-- <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap"> -->
  <nav class="navbar fixed-top">
    <div class="container-fluid justify-content-between">
      
      <img src="src/assets/logo_remove_bg.png" alt="" class="logo">
      
      <Search class="form-inline d-flex justify-content-center"/>
      
      
      <div class="navbar-links">
  <RouterLink to="/" class="nav-link logout-link" style="color: white; font-size: 30px;">Home</RouterLink>
  <RouterLink to="/community" class="nav-link logout-link" @click="checkLogin('Community')" style="color: white; font-size: 30px;">Community</RouterLink>
  
 
  <template v-if="store.isLogin">
    <span class="nav-link logout-link" @click="logOutOrToLogin" style="color: white; font-size: 30px;">Logout</span>
  </template>
  <template v-else>
    <RouterLink to="/login" class="nav-link logout-link" style="color: white; font-size: 30px;">Login</RouterLink>
  </template>
</div>
    </div>
  </nav>
</template>
  
<script setup>
import Search from '../components/Search.vue';
import { RouterLink, useRouter } from 'vue-router';
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import LoginView from '../views/LoginView.vue';

const store = useCounterStore();
const router = useRouter();

const checkLogin = (page) => {
  if (!store.isLogin) {
    alert(`로그인이 필요합니다. ${page} 페이지를 이용하려면 먼저 로그인하세요.`);
    router.push('/login');
  }
};

const logOutOrToLogin = () => {
  if (store.isLogin) {
  
    router.push('/login');
    store.logOut();
  }
  } 

</script>
  
  
<style scoped>




  .navbar {
  background-color: black;
  padding: 12px 40px;
  font-family: Cute Font;
}

.container-fluid {
  display: flex;
  align-items: center;
  gap: 20px; 
}

.router-link {
  display: flex;
  align-items: center;
  gap: 10px; 
}
  .btn-style {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 0;
    border-radius: 4px;
    overflow: hidden;
    cursor: pointer;
    font-family: 'Noto Sans KR', sans-serif; 
    font-size: 25px;
    font-weight: 500;
    letter-spacing: 0px;
    line-height: 18px;
    background: #f82f62;
    text-decoration: none;
    color: #fff;
    padding: 7px 12px;
  }
.search-button {
  white-space: nowrap;
  padding-left: 10px;
}

.logo {
  width: 100px;
  height: auto;
}

.recommend-container {
  margin-top: 100px; 
}

@media (max-width: 768px) {
  .navbar {
    padding: 5px;
  }
  
  .container-fluid {
    gap: 10px; 
  }
  
  .search-button {
    padding-left: 5px;
  }
  
  .logo {
    width: 80px;
  }
  
  .recommend-container {
    margin-top: 70px;
  }
}




.navbar-links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: white;
  font-size: 18px;
  font-weight: 1000;
}

.nav-link:hover{
  color: #f82f62; 
  scale: 1.1;
}

.logout-link {
  text-decoration: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  font-weight: 1000;
  
}

.logout-link:hover {
  color: #f82f62; 
  scale: 1.1;
}

</style>
