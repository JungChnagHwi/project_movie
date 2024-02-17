<template>
  <div style="margin-bottom: 100px;">
    <div class="card recommend-container">
    <!-- 국가 선택 셀렉트 박스 -->
    <!-- <label for="countrySelect">Country:</label> -->
    <div style="display: flex; align-items: center; text-align: center;">
      <select id="countrySelect" v-model="selectedCountry" @change="filterByCountry" class="form-select language-select" style=" margin-right: 0;">
        <option value="">All Countries</option>
        <option v-for="country in uniqueCountries" :key="country" :value="country">{{ country }}</option>
      </select>
    <h1 style="margin-left: 280px;">Country</h1>
    </div>
    <!-- 영화 목록 -->
      <div class="card-list px-3">
        <!-- 각 영화에 대한 카드 -->
        <card class="cardrev" v-for="movie in movies" :key="movie.id" @click="openModal(movie)">
          <img :src="getMoviePosterUrl(movie.poster_path)" alt="Movie Poster" style="width: 200px; height: auto;">
          <!-- <p style="text-align: center; margin-top: 30px; font-size: 24px; font-family: 'Noto Sans KR', sans-serif; font-weight: bold;">{{ movie.title }}</p> -->
        </card>
      </div>
    </div>

    <!-- 영화 정보 모달 -->
    <div id="countryModal" class="modal" @click="closeModalOutside">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <div v-if="selectedMovie" class="movie-info">
          <!-- 비디오 프레임 또는 이미지 -->
          <div v-if="selectedMovie.video_url">
            <iframe :src="'https://www.youtube.com/embed/' + extractVideoId(selectedMovie.video_url)" frameborder="0" allowfullscreen style="justify-content: center; align-items: center; width: 100%; height: 400px; margin-top: 40px;"></iframe>
          </div>
          <!-- 영화 정보 -->
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
          <!-- 관련 영화 목록 -->
          <div class="related-movies">
            <h3 style="margin-bottom: 12px; margin-left: 5px;">비슷한 콘텐츠</h3>
            <div class="movie-grid">
              <div v-for="relatedMovie in getRelatedMovies" :key="relatedMovie.id" @click="openModal(relatedMovie)">
                <img :src="getMoviePosterUrl(relatedMovie.poster_path)" alt="Related Movie Poster" class="movie-poster">
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';

const store = useCounterStore();
const movies = ref([]);
const selectedMovie = ref(null);

const getMovies = function () {
  axios({
    method: 'GET',
    url: `http://127.0.0.1:8000/movies/country/`,
  })
  .then((res) => {
    movies.value = res.data.slice(0, 10);
  })
  .catch((err) => {
    console.log(err);
  });
};
onMounted(() => {
  getMovies();
});

const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

function openModal(movie) {
  selectedMovie.value = movie;
  document.getElementById('countryModal').style.display = 'block';
}

function closeModal() {
  selectedMovie.value = null;
  document.getElementById('countryModal').style.display = 'none';
}

function closeModalOutside(event) {
  if (event.target === document.getElementById('countryModal')) {
    closeModal();
  }
}

window.onclick = function (event) {
  closeModalOutside(event);
};

const isLiked = ref(false);

const toggleLike = () => {
  if (selectedMovie.value) {
    const movieId = selectedMovie.value.id;
    axios.post(`http://127.0.0.1:8000/movies/${movieId}/movie_like/`, {}, {
      headers: {
        Authorization: `Token ${store.token}`
      }
    })
    .then((res) => {
      selectedMovie.value.isLiked = !selectedMovie.value.isLiked;
      isLiked.value = selectedMovie.value.isLiked;
    })
    .catch((err) => {
      console.error(err);
    });
  }
};
const allmovies = ref([]);

const allMovies = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/movies/`);
    allmovies.value = res.data;
  } catch (error) {
    console.error('Error fetching movies:', error);
  }
};

onMounted(() => {
  allMovies();
});

const getRelatedMovies = computed(() => {
  if (selectedMovie.value && selectedMovie.value.genres) {
    const genreId = selectedMovie.value.genres[0];
    
    const sameGenreMovies = allmovies.value.filter(movie => movie.genres.includes(genreId) && movie.id !== selectedMovie.value.id);
    
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
  const match = url.match(/(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  return match ? match[1] : null;
};
const selectedCountry = ref('');
const extractCountries = () => {
  const countriesSet = new Set();
  allmovies.value.forEach(movie => {
    if (movie.countries) {
      const movieCountries = movie.countries.split(',');
      movieCountries.forEach(country => countriesSet.add(country.trim()));
    }
  });
  return Array.from(countriesSet);
};

const uniqueCountries = computed(() => extractCountries());

const filterByCountry = () => {
  if (selectedCountry.value) {
    const filteredMovies = allmovies.value.filter(movie => {
      if (movie.countries) {
        const movieCountries = movie.countries.split(',').map(country => country.trim());
        return movieCountries.includes(selectedCountry.value);
      }
      return false;
    });
    movies.value = filteredMovies;
  } else {
    movies.value = allmovies.value;
  }
};

</script>

<style scoped>
  .form-select {
    /* 부트스트랩 클래스를 사용하여 셀렉트 박스 스타일링 */
    padding: 0.375rem 2rem 0.375rem 1rem;
    font-size: 1rem;
    font-weight: 1000;
    line-height: 1.5;
    color: white;
    background-color: black;
    background-clip: padding-box;
    border: solid 1px rgb(27, 27, 27);
    border-radius: 0.25rem;
    transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
    width: auto; /* 셀렉트 박스 너비 자동 조절 */
    margin-right: 800px;
    margin-top: 20px;
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
    overflow: auto;
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
</style>
