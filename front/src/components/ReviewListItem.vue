<template>

  <tr>

    <td style="width: 5%;"><RouterLink :to="{ name: 'DetailView', params: { id: review.id }}" class="custom-link">
      <p><h5>{{ review.id }}</h5></p>
    </RouterLink></td>
    <td style="width: 30%"><RouterLink :to="{ name: 'DetailView', params: { id: review.id }}" class="custom-link">
      <p class="title">{{ review.movie_title }}</p>
    </RouterLink></td>
    <td style="width: 40%"><RouterLink :to="{ name: 'DetailView', params: { id: review.id }}" class="custom-link">
      <p>{{ review.article_title }}</p>
    </RouterLink></td>
    <!-- <td><p class="content">{{ review.article_content }}</p></td> -->
    <td style="width: 10%"><p>{{ review.username }}</p></td>
    
    <td style="width: 15%"><div class="rating">
      <span v-for="star in parseInt(review.rating)" :key="star">⭐</span>
    </div></td>
    
    <!-- <button @click="toggleLike">
      {{ isLiked ? 'Unlike' : 'Like' }}
    </button>
  -->
    </tr>

</template>

<script setup>
import { RouterLink, useRouter } from 'vue-router';
import { onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const store = useCounterStore();

onMounted(() => {
store.getReviewList();
});

defineProps({
review: Object,
});


</script>

<style scoped>
.review-item {

display: flex;
width: 100%;
}

.title {
/* font-size: 18px;
font-weight: bold; */
}
.custom-link {
text-decoration: none;
color: white;
}
.custom-link:hover {
color: #ff0000;
}
.content {
margin-top: 10px;
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