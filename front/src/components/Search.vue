<template>
  <div class="search-container">
    <input v-model="searchQuery" class="search-input" placeholder="영화를 검색하세요..." @input="searchMovies" />

    <ul v-if="searchResults.length > 0" class="search-results">
      <li v-for="movie in searchResults" :key="movie.id" @click="selectMovie(movie)">
        {{ movie.title }}
      </li>
    </ul>

    <!-- <button class="search-button" @click="openModal">Search</button> -->
  </div>

  <div id="SearchModal" class="modal" @click="closeModalOutside">
    <div class="modal-content" @click.stop>
      <span class="close" @click="closeModal">&times;</span>
      <div v-if="selectedMovie" class="movie-info">
        <div v-if="selectedMovie.video_url">
          <iframe
            :src="'https://www.youtube.com/embed/' + extractVideoId(selectedMovie.video_url)"
            frameborder="0"
            allowfullscreen
            style="justify-content: center; align-items: center; width: 100%; height: 400px; margin-top: 40px;"
          ></iframe>
        </div>
        <h2>{{ selectedMovie.title }}</h2>
        <p class="info"> {{ selectedMovie.tagline }}</p>
        <div class="movie-details">
          <img :src="getMoviePosterUrl(selectedMovie.poster_path)" alt="Movie Poster" class="poster" />
          <div class="overview-rating">
            <p class="overview">{{ selectedMovie.overview }}</p>
            <p class="rating">평점: {{ selectedMovie.vote_average }}</p>
            <p class="info"><strong>개봉일:</strong> {{ selectedMovie.release_date }}</p>
            <p class="info"><strong>런타임:</strong> {{ selectedMovie.runtime }} 분</p>
            <p class="info"><strong>감독:</strong> {{ selectedMovie.director }}</p>
          </div>
        </div>
        <br />
        <div class="related-movies">
          <h3 style="margin-bottom: 12px; margin-left: 5px;">비슷한 콘텐츠</h3>
          <div class="movie-grid">
            <div v-for="relatedMovie in getRelatedMovies" :key="relatedMovie.id" @click="openModal(relatedMovie)">
              <img :src="getMoviePosterUrl(relatedMovie.poster_path)" alt="Related Movie Poster" class="movie-poster" />
              <!-- <p>{{ relatedMovie.title }}</p> -->
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

const searchQuery = ref('');
const searchResults = ref([]);
const selectedMovie = ref(null);
const movies = ref([]);

const searchMovies = async () => {
  try {
    if (searchQuery.value.trim() === '') {
      searchResults.value = [];
      return;
    }

    const response = await axios.get('https://api.themoviedb.org/3/search/movie', {
      params: {
        api_key: '69b934b0175eaae9758e75483f1b07e2',
        language: 'ko-KR',
        query: searchQuery.value,
      },
    });

    // 검색 결과가 있을 때만 업데이트
    if (response.data.results.length > 0) {
      searchResults.value = response.data.results;
      // searchQuery.value = '';
    }
  } catch (error) {
    console.error('Failed to search movies:', error);
  }
};

const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

const selectMovie = async (movie) => {
  try {
    const response = await axios.get(`https://api.themoviedb.org/3/movie/${movie.id}`, {
      params: {
        api_key: '69b934b0175eaae9758e75483f1b07e2',
        language: 'ko-KR',
        append_to_response: 'videos,credits',
      },
    });
    
    const tmdbMovie = response.data; // 수정된 부분

    const videoUrl = tmdbMovie.videos.results.length > 0 ? `https://www.youtube.com/watch?v=${tmdbMovie.videos.results[0].key}` : null;
    const director = tmdbMovie.credits.crew.find(person => person.job === 'Director');
    // 상세 정보 업데이트
    selectedMovie.value = {
      ...movie,
      director: director ? director.name : 'N/A', // 이부분은 실제 데이터에 따라서 수정이 필요할 수 있습니다.
      runtime: tmdbMovie.runtime, // 이부분은 실제 데이터에 따라서 수정이 필요할 수 있습니다.
      video_url: videoUrl,
      tagline: tmdbMovie.tagline,
      // 추가적인 필요한 정보들을 tmdbMovie에서 가져와 추가할 수 있습니다.
    };
    selectedMovie.value.genres = tmdbMovie.genres.map(genre => genre.id);
    searchQuery.value = movie.title;

    // 모달 열기
    document.querySelector('.modal').style.display = 'block';
    // 검색 결과 초기화
    searchResults.value = [];
    searchQuery.value = '';
  
  } catch (error) {
    console.error('Failed to fetch movie details:', error);
  }
};

const openModal = () => {
  // 검색 결과와 검색어가 같을 때만 모달을 열기
  if (selectedMovie.value && selectedMovie.value.title.toLowerCase() === searchQuery.value.trim().toLowerCase()) {
    document.querySelector('.modal').style.display = 'block';
    searchQuery.value = '';
    searchResults.value = [];
  }
};

const closeModal = () => {
  document.querySelector('.modal').style.display = 'none';
};

function closeModalOutside(event) {
  if (event.target === document.getElementById('SearchModal')) {
    closeModal();
  }
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
    console.log('Selected Movie Genres:', selectedMovie.value.genres);
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
}
</script>


<style scoped>
  .search-container {
    position: relative;
    width: 300px;
    margin: 20px auto;
    margin: 5px ;
    margin-left: 135px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: none;
  }

  .search-input {
    width: 200px;
    padding: 8px;
    font-size: 14px;
    background-color: #333; /* 검은 배경색 */
    color: #fff; /* 폰트 색상 */
    border: 1px solid #555; /* 테두리 스타일 및 색상 */
    border-radius: 5px; /* 모서리 둥글게 */
    margin-right: 5px;
    font-family: none;
  }

  .search-button {
    width: 0px;
    padding: 8px;
    font-size: 14px;
    cursor: pointer;
    background-color: #ff9800; /* 원하는 버튼 색상 */
    color: #333; /* 버튼 폰트 색상 */
    border: 1px solid #ff9800; /* 버튼 테두리 스타일 및 색상 */
    border-radius: 5px; /* 모서리 둥글게 */
    
  }

  .search-results {
    list-style: none;
    padding: 0;
    margin: 0;
    position: absolute;
    width: 100%;
    background-color: #333;
    border: 1px solid #333;
    top: 38px; /* Adjusted to position below the search input */
  }

  search-results li {
    padding: 10px;
    cursor: pointer;
    /* border-bottom: 1px solid #ddd; */
    transition: background-color 0.3s; /* 배경색 변화에 트랜지션 효과 추가 */
  }

  .search-results li:hover {
    background-color: #555; /* 마우스 호버 시 배경색 변경 */
    color: white; /* 마우스 호버 시 글자색 변경 */
    scale: 1.05;
    cursor: pointer;
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
    margin-top: 60px;
    font-family: none;
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
    background-color: #1c1c1c;
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

  .modal-title {
    text-align: center;
    font-size: 24px;
    margin-bottom: 10px;
  }

  .modal-body {
    text-align: left;
    line-height: 1.6;
  }

  .movie-grid {
    display: grid;
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
    font-family: 'Teko';
    /* 기타 스타일 속성 추가 가능 */
  }
</style>
