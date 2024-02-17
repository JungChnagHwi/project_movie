<template>
    <div>
      <select v-model="selectedComponent" class="form-select language-select" style=" margin-right: 0;">
        <option value="recommend2">인기순</option>
        <option value="recommend1">평점순</option>
        <!-- <recommend1 /> -->
        <option value="recommend3">최신영화</option>
        <option value="recommend9">Coming soon...</option>
      </select>
  
      <!-- 선택된 컴포넌트 렌더링 -->
      <!-- <component :is="selectedComponent" /> -->

    <component :is="selectedComponent === 'recommend1' ? recommend1 : ''" />
    <component :is="selectedComponent === 'recommend2' ? recommend2 : ''" />
    <component :is="selectedComponent === 'recommend3' ? recommend3 : ''" />
    <component :is="selectedComponent === 'recommend9' ? recommend9 : ''" />
  </div>
    
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import recommend1 from '@/components/recommend1.vue';
  import recommend2 from '@/components/recommend2.vue';
  import recommend3 from '@/components/recommend3.vue';
  import recommend9 from '@/components/recommend9.vue';
  
  const selectedComponent = ref('recommend2'); // 초기 선택값
  </script>
  
  <style scoped>
  .form-select {
    /* 부트스트랩 클래스를 사용하여 셀렉트 박스 스타일링 */
    padding: 0.375rem 2rem 0.375rem 1rem;
    font-size: 1.1rem;
    font-weight: 1000;
    line-height: 1.5;
    color: white;
    background-color: black;
    background-clip: padding-box;
    border: solid 1px rgb(27, 27, 27);
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    width: 200px; 
    margin-right: 800px;
    margin-top: 20px;
    margin-left: 20px;
    margin-bottom: 10px;
    
  }
  </style>
  