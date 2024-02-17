<template>
  <div>
  <div class="card recommend-container">
    <div style="display: flex; align-items: center; text-align: center;">
    <select v-model="selectedGenre" @change="fetchMoviesBySelectedGenre" class="form-select genre-select" style=" margin-right: 0;">
      <!-- <option value="">장르</option> -->
      <option v-for="genre in genres" :key="genre.pk" :value="genre.genre_ids">
        {{ genre.name }}
      </option>
    </select>
    <!-- <h1 style="margin-left: 300px;">Genre</h1> -->
  </div>
    <div class="card-list px-3" ref="cardList">
      <div v-if="movies.length === 0">
        <p>선택한 장르에 대한 인기 영화가 없습니다.</p>
      </div>
      <div class="scrolling-wrapper">
        <div v-for="movie in movies" :key="movie.id" class="cardrev" @click="openModal(movie)">
          <img :src="getMoviePosterUrl(movie.poster_path)" alt="Movie Poster">
          <!-- <p style="text-align: center; margin-top: 30px; font-size: 24px; font-family: 'Noto Sans KR', sans-serif; font-weight: bold;">{{ movie.title }}</p> -->
        </div>
      </div>
      <button class="arrow-button right" @click="navigateCards('right')">▶</button>
      <button class="arrow-button left" @click="navigateCards('left')">◀</button>
    </div>

    <div id="genreModal" class="modal" @click="closeModalOutside">
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
</div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';

const genres = [
    { pk: 28, name: '액션', genre_ids: [28] },
    { pk: 12, name: '모험', genre_ids: [12] },
    { pk: 16, name: '애니메이션', genre_ids: [16] },
    { pk: 35, name: '코미디', genre_ids: [35] },
    { pk: 80, name: '범죄', genre_ids: [80] },
    { pk: 99, name: '다큐멘터리', genre_ids: [99] },
    { pk: 18, name: '드라마', genre_ids: [18] },
    { pk: 10751, name: '가족', genre_ids: [10751] },
    { pk: 14, name: '판타지', genre_ids: [14] },
    { pk: 36, name: '역사', genre_ids: [36] },
    { pk: 27, name: '공포', genre_ids: [27] },
    { pk: 10402, name: '음악', genre_ids: [10402] },
    { pk: 9648, name: '미스터리', genre_ids: [9648] },
    { pk: 10749, name: '로맨스', genre_ids: [10749] },
    { pk: 878, name: 'SF', genre_ids: [878] },
    { pk: 10770, name: 'TV 영화', genre_ids: [10770] },
    { pk: 53, name: '스릴러', genre_ids: [53] },
    { pk: 10752, name: '전쟁', genre_ids: [10752] },
    { pk: 37, name: '서부', genre_ids: [37] },
];

const selectedGenre = ref(genres[0].genre_ids)
const movies = ref([]);
const router = useRouter();
const selectedMovie = ref(null)
const store = useCounterStore()
const cardList = ref(null)

const fetchMoviesBySelectedGenre = () => {
  fetchMoviesByGenre(selectedGenre.value);
};

const fetchMoviesByGenre = (genreIds) => {
  axios({
    method: 'GET',
    url: 'http://127.0.0.1:8000/movies/genre/',
    params: {
      genre_ids: genreIds.join(','), // genre_ids를 쉼표로 구분한 문자열로 변환
    },
  })
  .then((res) => {
    movies.value = res.data;
  })
  .catch((err) => {
    console.log(err);
  });
};

const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

onMounted(() => {
  fetchMoviesBySelectedGenre();
});

const openModal = (movie) => {
  selectedMovie.value = movie;
  document.getElementById('genreModal').style.display = 'block';
};

const closeModal = () => {
  selectedMovie.value = null;
  document.getElementById('genreModal').style.display = 'none';
};

function closeModalOutside(event) {
  if (event.target === document.getElementById('genreModal')) {
    closeModal();
  }
}

window.onclick = function (event) {
  closeModalOutside(event);
}


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
.genres {
  display: flex;
  justify-content: flex-start;
  overflow-x: auto;
  margin-bottom: 20px;
}

.genre-select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 10px;
  cursor: pointer;
  
}

.card-list {
    display: flex;
    flex-wrap: nowrap;
    overflow: hidden;
  }

.scrolling-wrapper {
  display: flex;
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

.recommend-container {
    margin-top: 5px;
    background-color: black;
    color: white;
    display: flex;
  }
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

/* .movie-info {
  text-align: center;
} */

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
