<template>
  <div >
    <h1>Community</h1>
      <div>
      <RouterLink :to="{ name: 'CreateView' }" class="create-link">
        글 작성
      </RouterLink>
      <ReviewList />
      </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { RouterLink } from 'vue-router'
import ReviewList from '../components/ReviewList.vue'

const store = useCounterStore();

onMounted(() => {
  store.getReviewList();
});
</script>

<style scoped>
.card {
  max-width: 800px;
  margin: 0 auto;
  margin-top: 200px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.card-content {
  padding: 20px;
  text-align: center;
}

.create-link {
  display: inline-block;
  margin-top: 10px;
  padding: 10px;
  background-color: rgb(229,9,20);
  color: white;
  text-decoration: none;
  border-radius: 5px;
}

.create-link:hover {
  background-color: rgb(229,9,20);
  background-color: #4CAF50;
}

</style>
