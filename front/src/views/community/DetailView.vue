<template>
  <div class="review-detail-container">
    
    <div v-if="review" class="review-details">
      <h1 class="" style="border: solid white; text-align: center;">{{ review.movie_title }}</h1>
      <div class="rating" style="font-size: 20px; margin: 0;">
        <span v-for="star in parseInt(review.rating)" :key="star"> ⭐ </span>
      </div>
      
      <p class="title">Title : {{ review.article_title }}</p>
      <p class="content">Review : {{ review.article_content }}</p>
      <p class="author">작성자 : {{ review.username }}</p>
      <p class="date">작성일: {{ formatTimestamp(review.created_at) }}</p>
    </div>
    <hr>
    <button @click="gotoUpdate" class="action-button">게시글 수정</button>
    <button @click="goToDelete" class="action-button">게시글 삭제</button>
    <hr>

    <!-- 댓글 목록 -->
    <div>
      <h2 class="comment-heading">댓글 목록</h2>
      <hr>
      <ul v-if="comments.length > 0" class="comment-list">
        <li v-for="comment in comments" :key="comment.id" class="comment-item">
          <p class="comment-content">{{ comment.content }}</p>
          <div class="comment-info">
            <p class="comment-author">작성자: {{ comment.username }}</p>
            <!-- 수정된 부분 -->
            <div class="comment-metadata">
              <p class="comment-date">작성일: {{ formatTimestamp(comment.created_at) }}</p>
              <button @click="deleteComment(comment.id)" class="delete-button">삭제</button>
            </div>
            <!-- -------------- -->
          </div>
          <hr class="comment-divider">
        </li>
      </ul>
      <p v-else class="no-comments">댓글이 없습니다.</p>
    </div>
    <!-- 댓글 작성 폼 -->
    <div class="comment-form">
      <textarea v-model="newComment" placeholder="댓글을 입력하세요" class="comment-input"></textarea>
      <button @click="postComment" class="comment-button">댓글 작성</button>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import { useRoute, useRouter } from 'vue-router';

const store = useCounterStore();
const route = useRoute();
const review = ref(null);
const router = useRouter();
const pk = route.params.pk;
const newComment = ref('');
const comments = ref([]);

const fetchComments = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/reviews/${route.params.id}/comments/`);
    comments.value = response.data;
  } catch (error) {
    console.error('댓글을 불러오는 중 에러 발생:', error);
  }
};

const formatTimestamp = (timestamp) => {
  const options = { year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric', second: 'numeric', timeZone: 'Asia/Seoul' };
  return new Date(timestamp).toLocaleDateString('ko-KR', options);
};

onMounted(() => {
  fetchComments();
});

const deleteComment = async (commentId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/reviews/${route.params.id}/comments/${commentId}/`, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    });
    fetchComments();
  } catch (error) {
    console.error('댓글 삭제 중 에러 발생:', error, alert('내가 쓴 댓글만 삭제할 수 있어요!'));
  }
};

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/reviews/reviews/${route.params.id}/`
  })
    .then((res) => {
      review.value = res.data;
      comments.value = res.data.comments;
    })
    .catch((err) => {
      console.log(err);
    });
});

const gotoUpdate = function () {
  router.push({ name: 'UpdateView', params: { pk: pk },  });
};

// const gotoUpdate = function () {
//   axios({
//     method: 'P',
//     url: `${store.API_URL}/reviews/reviews/${route.params.id}/`,
//     headers: {
//       Authorization: `Token ${store.token}`
//     }
//   }) .then(res=>{
//     router.push({ name: 'DetailView' })
//   }) .catch(err => console.log(err));
// }

const goToDelete = function () {
  axios({
    method: 'DELETE',
    url: `${store.API_URL}/reviews/reviews/${route.params.id}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
      console.log(res);
      router.push({ name: 'community' });
    })
    .catch(err => console.log(err));
};

const refreshComments = async () => {
  await fetchComments();
};

const postComment = function () {
  if (!newComment.value.trim()) {
    alert('댓글 내용을 입력하세요.')
    return;
  }

  axios({
    method: 'post',
    url: `${store.API_URL}/reviews/${route.params.id}/comments/`,
    headers: {
      Authorization: `Token ${store.token}`,
    },
    data: {
      content: newComment.value,
    },
  })
    .then((res) => {
      comments.value.push(res.data);
      newComment.value = '';
      refreshComments();
    })
    .catch((err) => console.log(err));
};

const postList = ref([])
const getPostList = function () {
  axios({
    method: 'get',
    url: 'http://127.0.0.1:8000/reviews/review_create/',
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then(res => {
      postList.value = res.data
    })
    .catch(err => {
      console.log(err)
    })
}

const Username = ref('')
const Email = ref('')

onMounted(() => {
  fetchComments();
  getPostList
});

</script>

<style>
.review-detail-container {
  margin-top: 150px;
  margin-bottom: 100px;
}

.review-details {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 20px;
}

.author {
  margin: 0;
}

.title {
  font-size: 18px;
}

.content {
  margin-top: 10px;
}

.date {
  font-style: italic;
  color: #888;
  margin: 0;
}

.like-button,
.unlike-button,
.action-button,
.comment-button {
  background-color: #3498db;
  color: #fff;
  padding: 8px 12px;
  margin: 5px;
  cursor: pointer;
  border: none;
  border-radius: 3px;
}

.unlike-button {
  background-color: #e74c3c;
}

.comment-form {
  margin-top: 20px;
}

.comment-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
}

.comment-button {
  background-color: #2ecc71;
}

.comment-heading {
  font-size: 1.5em;
  margin-bottom: 10px;
}

.comment-list {
  list-style: none;
  padding: 0;
}

.comment-item {
  padding: 10px;
  margin-bottom: 10px;
  position: relative;
  display: flex;
  flex-direction: column;
}

.comment-content {
  margin-bottom: 5px;
  margin-top: 0;
}

.comment-info {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
}

.comment-author,
.comment-date {
  margin: 0;
}

.delete-button {
  background-color: #e74c3c;
  color: #fff;
  padding: 5px 10px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  /* margin-left: auto; */
}

.comment-divider {
  margin-top: 10px;
}

.no-comments {
  font-style: italic;
  color: #888;
}

.comment-date {
  font-style: italic;
  color: #888;
  margin: 0;
}
</style>
