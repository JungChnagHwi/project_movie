<template class="global_background">
  <div class="back">
    <div>
      <Navbar />
      <div class="content-container">
      
        <RouterView style="padding: 0 200px"/>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Navbar from '@/components/Navbar.vue';
import LoginView from '@/views/LoginView.vue';
import SignupView from '@/views/SignupView.vue';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
</script>

<style scoped>
/* .content-container {
  margin-top: 100px; 
} */
.global_background {
  background-color: black;
}

.content-container {
  margin-top: 100px;
  opacity: 1;
  z-index: 3; /* 배경 이미지 위에 나타나도록 하는 더 높은 z-index 설정 */
}

.back_ground {
  color: white;
  background-color: black;
}

</style>




