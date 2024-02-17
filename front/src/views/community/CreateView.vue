<template>
  <div class="create-page">
    <h1 v-if="route.name === 'CreateView' || route.name === 'UpdateView'" class="form-title">영화 후기를 남겨주세요!</h1>
    <br>
    <form @submit.prevent="route.name === 'CreateView' ? createPost() : updatePost()" class="form-container">
      <!-- 카테고리 선택 및 다른 입력 요소들... -->

      <div class="input-group">
        <label for="movie_title">영화 제목</label>
        <input type="text" id="movie_title" v-model.trim="movie_title" class="input-field" placeholder="영화 제목을 정확히 입력해주세요!">
      </div>

      <div class="input-group">
        <label for="title">제목</label>
        <input type="text" id="title" v-model.trim="title" class="input-field">
      </div>

      <div class="input-group">
        <label for="rating">별점</label>
        <select id="rating" v-model="rating" class="select-rating">
          <option value="1">⭐</option>
          <option value="2">⭐⭐</option>
          <option value="3">⭐⭐⭐</option>
          <option value="4">⭐⭐⭐⭐</option>
          <option value="5">⭐⭐⭐⭐⭐</option>
        </select>
      </div>

      <div class="input-group">
        <label for="content">내용</label>
        <p></p>
        <textarea class="textarea" id="content" v-model.trim="content"></textarea>
      </div>

      <input type="submit" v-if="route.name === 'CreateView'" value="글 작성" class="create-btn create-btn-create">
      <input type="submit" v-else-if="route.name === 'UpdateView'" value="글 수정" class="create-btn create-btn-update">
    </form>
  </div>
</template>

<script setup>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const title = ref(null);
const content = ref(null);
const store = useCounterStore();
const rating = ref(1);
const movie_title = ref(null);

let post = ref({});

if (route.name === 'UpdateView') {
  post = store.postList;
}

const createPost = function () {
  axios({
    method: 'POST',
    url: `http://127.0.0.1:8000/reviews/review_create/`,
    data: {
      movie_title: movie_title.value,
      article_title: title.value,
      article_content: content.value,
      rating: rating.value,
      // 여기서 review.username에 사용자 이름을 저장합니다.
      username: store.Username
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => router.push({ name: 'community', params: { id: res.data.id } }), console.log(rating))
    .catch(err => console.log(err));
};

onMounted(async () => {
  await store.getProfile();
  createPost();
});





const updatePost = function () {
  axios({
    method: 'PUT',
    url: `http://127.0.0.1:8000/reviews/reviews/${route.params.id}/`,
    data: {
      movie_title: movie_title.value,
      article_title: title.value,
      article_content: content.value,
      rating: rating.value
    },
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => router.push({ name: 'DetailView', params: { id: res.data.id } }))
    .catch(err => console.log(err));
};
</script>

  
<style scoped>
.create-page {
  text-align: center;
  height: 100%;
  margin-top: 100px;
  margin-bottom: 100px;
}

.form-title {
  margin-top: 0;
  padding-top: 1rem;
}

.form-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  max-width: 400px;
  margin: 0 auto;
}

.input-group {
  margin-bottom: 10px;
}

.input-field {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.select-rating {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  margin-bottom: 10px;
  text-align: center;
}

.textarea {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  resize: vertical;
  height: 150px;
}

.create-btn {
  display: inline-block;
  margin-top: 10px;
  padding: 10px 20px;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}

.create-btn-create {
  background-color: #e50914; /* Netflix red */
}

.create-btn-update {
  background-color: #4caf50; /* Green color */
}

.create-btn:hover {
  opacity: 0.8;
}
</style>