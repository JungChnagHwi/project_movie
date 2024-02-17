<template>
  <div>
    <div class="card recommend-container">
      <!-- <h1 style="text-align:center;">Popular</h1> -->
      <div class="card-list px-3" ref="cardList">
        <card class="cardrev" v-for="movie in movies" :key="movie.id" @click="openModal(movie)">
          <img :src="getMoviePosterUrl(movie.poster_path)" alt="Movie Poster" style="width: 200px; height: auto;">
          <!-- <p style="text-align: center; margin-top: 30px; font-size: 24px; font-family: 'Noto Sans KR', sans-serif; font-weight: bold;">{{ movie.title }}</p> -->
        </card>
      </div>
      <button class="arrow-button right" @click="navigateCards('right')">▶</button>
      <button class="arrow-button left" @click="navigateCards('left')">◀</button>
    </div>

    <div id="popularModal" class="modal" @click="closeModalOutside">
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
import { ref, computed, onMounted, watch } from 'vue';
import axios from 'axios';
import { useCounterStore } from '@/stores/counter';


const store = useCounterStore();
const movies = ref([]);
const selectedMovie = ref(null);
const cardList = ref(null); // ref 추가


const getMovies = function () {
  axios({
    method: 'GET',
    url: `http://127.0.0.1:8000/movies/popular/`,
  })
  .then((res) => {
    movies.value = res.data;
  })
  .catch((err) => {
    console.log(err);
    
  });
};
onMounted(() => {
  getMovies();
  cardList.value = document.getElementById('cardList');
});
const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

function openModal(movie) {
  selectedMovie.value = movie;
  document.getElementById('popularModal').style.display = 'block';
}

function closeModal() {
  selectedMovie.value = null;
  document.getElementById('popularModal').style.display = 'none';
}

function closeModalOutside(event) {
  if (event.target === document.getElementById('popularModal')) {
    closeModal();
  }
}

window.onclick = function (event) {
  closeModalOutside(event);
};


const allmovies = ref([]);

const allMovies = async () => {
  try {
    const res = await axios.get(`http://127.0.0.1:8000/movies/`)
  
    allmovies.value = res.data
  } catch (error) {
    console.error('Error fetching movies:', error)
  }
};

onMounted(() => {
  allMovies()
});

const getRelatedMovies = computed(() => {
  if (selectedMovie.value && selectedMovie.value.genres) {
    const genreId = selectedMovie.value.genres[0]
    
    // 장르가 같은 영화들
    const sameGenreMovies = allmovies.value.filter(movie => movie.genres.includes(genreId) && movie.id !== selectedMovie.value.id);
    
    // 랜덤으로 8개를 선택
    const randomRelatedMovies = getRandomMovies(sameGenreMovies, 8)
    
    return randomRelatedMovies;
  } else {
    return []
  }
});

function getRandomMovies(movies, count) {
  const shuffled = movies.sort(() => 0.5 - Math.random());
  return shuffled.slice(0, count);
}

const extractVideoId = (url) => {

  const match = url.match(/(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/);
  return match ? match[1] : null
}

function navigateCards(direction) {
  if (!cardList.value) return;

  if (direction === 'left') {
    cardList.value.scrollLeft -= 250
  } else if (direction === 'right') {
    cardList.value.scrollLeft += 250
  }
}
</script>

<style scoped>
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
    margin-top: 60px;
  }

  .modal-content {
    position: relative;
    background-color: #fefefe;
    margin: 5% auto;
    padding: 10px;
    border: 1px solid #888;
    width: 60%;
    max-height: 80%;
    overflow-y: auto;
    background-color: #1c1c1c;
    color: white;
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

  .movie-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
  }

  .movie-poster {
    width: 200px;
    height: auto;
    cursor: pointer;
    transition: transform 0.3s;
    border-radius: 8px;
  }

  .movie-poster:hover {
    transform: scale(1.1);
  }

  .movie-details {
    display: flex;
    margin-top: 20px;
  }

  .poster {
    width: 400px;
    height: auto;
    margin-right: 20px;
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
    color: #ff9800;
  }

  .info {
    font-family: 'Teko';
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
