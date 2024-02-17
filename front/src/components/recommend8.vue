<template>
  <div>
    <div class="card recommend-container" >
      <div style="display: flex; align-items: center; text-align: center;">
        <select v-model="selectedLanguage" @change="fetchMovies" class="form-select language-select" style=" margin-right: 0;">
          <option value="ko">한국</option>
          <option value="en">미국</option>
          <option value="ja">일본</option>
          <option value="fr">프랑스</option>
          <option value="cn">중국</option>
          <!-- 필요한 경우 다른 언어 옵션을 추가하세요 -->
        </select>
        <!-- <h1 style=" margin-left: 280px;">Language</h1> -->
      </div>
      <div class="card-list px-3" ref="cardList">
        <card class="cardrev" v-for="movie in movies" :key="movie.id" @click="openModal(movie)">
          <img :src="getMoviePosterUrl(movie.poster_path)" alt="Movie Poster" style="width: 200px; height: auto;">
          <!-- <p style="text-align: center; margin-top: 30px; font-size: 24px; font-family: 'Noto Sans KR', sans-serif; font-weight: bold;">{{ movie.title }}</p> -->
        </card>
      </div>
      <button class="arrow-button right" @click="navigateCards('right')">▶</button>
      <button class="arrow-button left" @click="navigateCards('left')">◀</button>
    </div>

    <div id="langModal" class="modal" @click="closeModalOutside">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <div v-if="selectedMovie" class="movie-info">
          <div v-if="selectedMovie.video_url">
            <iframe :src="'https://www.youtube.com/embed/' + extractVideoId(selectedMovie.video_url)" frameborder="0" allowfullscreen style="justify-content: center; align-items: center; width: 100%; height: 400px; margin-top: 40px;"></iframe>
          </div>
          <h2>{{ selectedMovie.title }}</h2>
          <p class="info"> {{ selectedMovie.tagline }}</p>
          <div class="movie-details">
            <img :src="getMoviePosterUrl(selectedMovie.poster_path)" alt="Movie Poster" class="poster">
            <div class="overview-rating">
              <p class="overview">{{ selectedMovie.overview }}</p>
              <p class="rating">평점: {{ selectedMovie.vote_average }}</p>
              <p class="info"><strong>개봉일:</strong> {{ selectedMovie.release_date }}</p>
              <p class="info"><strong>런타임:</strong> {{ selectedMovie.runtime }} 분</p>
              <p class="info"><strong>감독:</strong> {{ selectedMovie.director }}</p>
            </div>
          </div>
          <br>    
          <!-- <br>
          <button @click="toggleLike" v-if="!isLiked">좋아요 취소</button>
          <button @click="toggleLike" v-if="isLiked">좋아요</button>
          <br>
          <br> -->
          <div class="related-movies">
            <h3 style="margin-bottom: 12px; margin-left: 5px;">비슷한 콘텐츠</h3>
            <div class="movie-grid">
              <div v-for="relatedMovie in getRelatedMovies" :key="relatedMovie.id" @click="openModal(relatedMovie)">
                <img :src="getMoviePosterUrl(relatedMovie.poster_path)" alt="Related Movie Poster" class="movie-poster">
                <!-- <p>{{ relatedMovie.title }}</p> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const movies = ref([]);
const selectedMovie = ref(null);
const selectedLanguage = ref('ko');
const store = useCounterStore();
const cardList = ref(null)
const fetchMovies = function () {
  axios({
    method: 'GET',
    url: `http://127.0.0.1:8000/movies/lang/`,
    params: {
      language: selectedLanguage.value,
    },
  })
  .then((res) => {
    movies.value = res.data;
  })
  .catch((err) => {
    console.log(err);
  });
};
onMounted(() => {
  fetchMovies();
});


const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

function openModal(movie) {
  selectedMovie.value = movie;
  document.getElementById('langModal').style.display = 'block';
}

function closeModal() {
  selectedMovie.value = null;
  document.getElementById('langModal').style.display = 'none';
}

function closeModalOutside(event) {
  if (event.target === document.getElementById('langModal')) {
    closeModal();
  }
}

window.onclick = function (event) {
  closeModalOutside(event);
};



const allmovies = ref([]);

// allMovies를 함수가 아닌, 함수의 결과로 사용할 수 있도록 수정합니다
// 여기서 axios 함수는 비동기로 데이터를 가져오기 때문에 promise를 반환합니다
const allMovies = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/movies/`);
    // axios로 받은 데이터를 allmovies에 할당합니다
    allmovies.value = res.data;
  } catch (error) {
    console.error('Error fetching movies:', error);
  }
};

// 컴포넌트가 마운트되었을 때 allMovies 함수를 호출하여 데이터를 가져옵니다
onMounted(() => {
  allMovies();
});

const getRelatedMovies = computed(() => {
  if (selectedMovie.value && selectedMovie.value.genres) {
    const genreId = selectedMovie.value.genres[0];
    
    // 장르가 같은 영화들
    const sameGenreMovies = allmovies.value.filter(movie => movie.genres.includes(genreId) && movie.id !== selectedMovie.value.id);
    
    // 랜덤으로 8개를 선택
    const randomRelatedMovies = getRandomMovies(sameGenreMovies, 8);
    
    return randomRelatedMovies;
  } else {
    return [];
  }
});

function getRandomMovies(movies, count) {
  const shuffled = movies.sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}


const extractVideoId = (url) => {
  // YouTube 링크에서 동영상 ID를 추출하는 로직을 구현
  // 예: https://www.youtube.com/watch?v=p-XYgNKT7-o 에서 "p-XYgNKT7-o" 추출
  const match = url.match(/(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  return match ? match[1] : null;
};

function navigateCards(direction) {
  if (!cardList.value) return;

  if (direction === 'left') {
    cardList.value.scrollLeft -= 250; // 조절 가능한 값
  } else if (direction === 'right') {
    cardList.value.scrollLeft += 250; // 조절 가능한 값
  }
}
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
    width: 200px; /* 셀렉트 박스 너비 자동 조절 */
    margin-right: 800px;
    margin-top: 0px;
    margin-left: 20px;
    margin-bottom: 10px;
    
  }

  
 .recommend-container {
    margin-top: 5px;
    background-color: black;
    color: white;
    display: flex;
  }

  .card-list {
    display: flex;
    flex-wrap: nowrap;
    overflow: hidden;
  }

  .cardrev {
    margin-right: 15px;
    margin-bottom: 30px;
  }

  .cardrev img {
    transition: transform 0.3s;
  }

  .cardrev:hover img {
    transform: scale(1.2);
  }

  .modal {
    display: none;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.9);
    margin-top:60px;
  }

  .modal-content {
    position: relative;
    background-color: #fefefe;
    margin: 5% auto;
    padding: 10px; /* 변경된 부분 */
    border: 1px solid #888;
    width: 60%;
    max-height: 80%; /* 추가된 부분 */
    overflow-y: auto; /* 추가된 부분 */
    background-color: #1c1c1c; /* 넷플릭스 스타일에 맞게 배경색 변경 */
    color: white; /* 폰트 색상을 밝게 설정 */
  }

  .close {
    position: absolute;
    right: 15px;
    top: 5px;
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }

  .modal-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 10px;
  }

  .modal-body {
    text-align: left; /* 텍스트 정렬을 왼쪽으로 변경 */
    line-height: 1.6; /* 줄간격을 늘려 가독성을 높임 */
  }
  .movie-grid {
  display: grid ; 
  grid-template-columns: repeat(4, 1fr); /* 한 줄에 4개의 열 */
  gap: 5px; /* 그리드 간격 설정 */
}

.movie-poster {
  width: 200px; /* 포스터 크기 조절 */
  height: auto;
  cursor: pointer;
  transition: transform 0.3s;
  border-radius: 8px;
}

.movie-poster:hover {
  transform: scale(1.1); /* 호버 시 포스터 확대 */
}

.movie-details {
  display: flex;
  margin-top: 20px; /* 포스터와 overview 간의 간격 조절 */
}

.poster {
  width: 400px; /* 포스터 크기 조절 */
  height: auto;
  margin-right: 20px; /* 포스터와 overview 간의 간격 조절 */
}

.overview-rating {
  flex-grow: 1;
}

.overview {
  font-size: 16px;
  color: #ccc;
}

.rating {
  font-size: 18px;
  font-weight: bold;
  color: #ff9800; /* 원하는 평점 색상으로 변경 */
}
.info {
  font-family: 'Teko'
  /* 기타 스타일 속성 추가 가능 */
}

.arrow-button {
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    font-size: 24px;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    outline: none;
  }

  .left {
    left: -40px;
  }

  .right {
    right: -40px;
  }
</style>
