<template>
  <div class="recommend-container">
    <!-- <Search /> -->
    <recommend5 />
    <!-- <recommend1 /> -->
    <recommend1239 />
    <!-- <recommend1 />
    <recommend2 />
    <recommend3 /> -->
    <recommend8 />
    <recommend4 />
    <recommend6 />
    <!-- <recommend7 /> -->
  </div>
  
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';


// import Search from '../components/Search.vue';
import recommend1 from '@/components/recommend1.vue';
import recommend2 from '@/components/recommend2.vue';
import recommend3 from '@/components/recommend3.vue';
import recommend4 from '@/components/recommend4.vue';
import recommend5 from '@/components/recommend5.vue';
import recommend8 from '@/components/recommend8.vue';
import recommend6 from '@/components/recommend6.vue';
import recommend7 from '@/components/recommend7.vue';
import recommend1239 from '@/components/recommend1239.vue';
</script>

<style scoped>
.recommend-container {
    margin-top: 100px; /* Nav 아래로 내리기 위한 상단 여백 */
    
  }
</style>