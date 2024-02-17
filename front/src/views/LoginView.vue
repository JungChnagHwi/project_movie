<template>
  <div class="login-container">
    <h2 style="color:white">로그인</h2>
    <form @submit.prevent="logIn">
      <div class="form-group">
        <input type="text" id="username" v-model.trim="username" placeholder="Username" />
        <input type="password" id="password" v-model.trim="password" placeholder="Password" />
      </div>
      <input style= "width: 400px;" class="btn-login" type="submit" value="로그인">

      <br>
      <button @click="goToSignupView" class="btn btn-secondary btn-signup">회원가입</button>
    </form>
    
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import axios from 'axios';

const username = ref(null);
const password = ref(null);
const token = ref(/* 초기 토큰 값 */); // 토큰 상태에 따라 초기 값을 설정해주세요.

const store = useCounterStore()
const router = useRouter()

// const isLogin = computed(() => {
//   return token.value !== null;
// });

const logIn = function() {
  const payload = {
    username: username.value,
    password: password.value,
  }
  axios(
    store.logIn(payload)

  ) .then(()=>{router.push('/')})
    // .catch((err)=> {alert('로그인 실패')})
}

const goToSignupView = function() {
  router.push('/signup');
}
</script>

<style scoped>
.btn-login {
  background-color: #e50914;
  color: rgb(255, 255, 255);
  font-weight: 700;
  letter-spacing: -0.1px;
  text-align: center;
  width: 100%;
  border-radius: 40px;
  /* border-color: rgb(248, 47, 98); */
  font-size: 16px;
  line-height: 47px;
  height: 48px;
  font-size: 20px;
  line-height: 30px;
}

.btn-signup {
  background-color: #e50914; /* 수정된 부분: 버튼 색상 변경 */
  color: #fff;
  font-weight: 700;
  letter-spacing: -0.1px;
  text-align: center;
  width: 400px;
  border-radius: 40px;
  /* border-color: #28a745;  */
  font-size: 16px;
  line-height: 47px;
  height: 48px;
  font-size: 20px;
  line-height: 30px;
}

.login-container {
  max-width: 400px auto;
  margin: auto;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-top: 200px;
  color: white;
}

h2 {
  color: #333;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  text-align: left;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-top: 5px;
}

/* button {
  background-color: #1a237e;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
} */

button:hover {
  background-color: #4caf50; 
}
.btn-login:hover {
  background-color: #4caf50; 
}
</style>
