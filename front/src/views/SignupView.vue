<template>
  <div class="signup-page">
    <h2>회원 가입</h2>
    <form @submit.prevent="signUp">
      <div class="form-group">
        <!-- <label for="username">사용자 이름:</label> -->
        <input type="text" id="username" v-model.trim="username" placeholder="username" required />
      </div>
      <div class="form-group">
        <!-- <label for="email">이메일:</label> -->
        <input type="email" id="email" v-model.trim="email" placeholder="email" required />
      </div>
      <div class="form-group">
        <!-- <label for="password1">비밀번호:</label> -->
        <input type="password" id="password1" v-model.trim="password1" placeholder="password" required />
      </div>
      <div class="form-group">
        <!-- <label for="password2">비밀번호 확인:</label> -->
        <input type="password" id="password2" v-model.trim="password2" placeholder="password" required />
      </div>
      
      <input type="submit" class="btn-signup" value="회원가입">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const router = useRouter()

const signUp = async function() {
  try {
    const payload = {
      username: username.value,
      password1: password1.value,
      password2: password2.value
    };
  
    await store.signUp(payload);
    
    // 회원가입이 성공하면 홈 페이지로 이동
    router.push('/');
  } catch (error) {
    // 회원가입 실패 처리 (예: 에러 메시지 표시)
    console.error('회원가입 실패:', error);
  }
};

</script>

<style scoped>
.signup-page {
  color: white;
  text-align: center;
  max-width: 600px;
  margin: auto;
  margin-top: 200px;
  /* margin-bottom: 100px; */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.form-group {
  width: 400px;
  max-width: 500px;
  margin-bottom: 15px;
}


input,
select {
  width: 100%;
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-top: 5px;
}

button {
  background-color: #1a237e;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #3949ab;
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

.btn-signup:hover {
  background-color: #4caf50; 
}
</style>
