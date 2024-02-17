<template>
  <!-- 영화포스터 출력 -->
  <div>
    <h1 class="text-sort">BoxOffice</h1>
    <br>
    <div class="swiper-container" style="height:450px;  padding: 0 200px;">
      <div class="swiper-wrapper">
        <div class="swiper-slide movie" v-for="movie in movies" :key="movie.id" @click="openModal(movie)">
          <img :src="getMoviePosterUrl(movie.poster_path)" alt="Movie Poster" style="width: 300px; height: auto;">
          <!-- <p class = "swiper-title">{{ movie.title }}</p> -->
        </div>
      </div>
      <!-- 추가적인 Swiper 설정 -->
      <!-- <div class="swiper-button-next"></div>
      <div class="swiper-button-prev"></div> -->
    </div>


    <div id="boxOfficeModal" class="modal" @click="closeModalOutside">
      <div class="modal-content" @click.stop>
        <span class="close" @click="closeModal">&times;</span>
        <div v-if="selectedMovie" class="movie-info">
          <div v-if="selectedMovie.video_url">
            <iframe :src="'https://www.youtube.com/embed/' + extractVideoId(selectedMovie.video_url)" frameborder="0" allowfullscreen style="justify-content: center; align-items: center; width: 100%; height: 400px; margin-top: 40px;"></iframe>
          </div>
          <h2>{{ selectedMovie.title }}</h2>
          <p class="info">{{ selectedMovie.tagline }}</p>
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
          
          
          <!-- <br>
          <button @click="toggleLike" v-if="!isLiked">좋아요 취소</button>
          <button @click="toggleLike" v-if="isLiked">좋아요</button>
          <br> -->
          <br>
          <div class="related-movies">
            <!-- <h3 style="margin-bottom: 12px; margin-left: 5px;">비슷한 콘텐츠</h3> -->
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
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useCounterStore } from '@/stores/counter';
import Swiper from 'swiper';
import 'swiper/swiper-bundle.css';

const movies = ref([]);
const selectedMovie = ref(null);
const store = useCounterStore()



const getFormattedDate = (date) => {
  return date.toISOString().slice(0, 10).replace(/-/g, '');
};

// 박스오피스 API를 불러오는 함수
const fetchBoxOffice = async () => {
  try {
    const today = new Date();
    today.setDate(today.getDate() - 1);

    const kobisResponse = await axios.get('http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json', {
      params: {
        key: '168017cd1cd66a141f455aca1e70e5a8',
        targetDt: getFormattedDate(today), // 오늘 날짜로 변경하세요
      },
    });

    // 순위 10위까지만 가져오기
    const boxOfficeMovies = kobisResponse.data.boxOfficeResult.dailyBoxOfficeList.slice(0, 10);

    // 각 영화에 대한 TMDb 정보를 가져오기
    const tmdbPromises = boxOfficeMovies.map(async (movie) => {
      const tmdbSearchResponse = await axios.get('https://api.themoviedb.org/3/search/movie', {
        params: {
          api_key: '69b934b0175eaae9758e75483f1b07e2',
          query: movie.movieNm,
          language: 'ko-KR',
        },
      });

      // 검색 결과에서 첫 번째 영화의 ID를 가져옴
      const firstMovie = tmdbSearchResponse.data.results[0];
      const tmdbMovieId = firstMovie ? firstMovie.id : null;

      if (tmdbMovieId) {
        // 영화의 ID를 사용하여 상세 정보를 가져옴
        const tmdbDetailResponse = await axios.get(`https://api.themoviedb.org/3/movie/${tmdbMovieId}`, {
          params: {
            api_key: '69b934b0175eaae9758e75483f1b07e2',
            language: 'ko-KR',
            append_to_response: 'videos,credits,genres', // videos 및 credits 추가
          },
        });

        const tmdbMovie = tmdbDetailResponse.data;
        
        // videos 및 credits를 확인하고 필요한 정보 추출
        const videoUrl = tmdbMovie.videos.results.length > 0 ? `https://www.youtube.com/watch?v=${tmdbMovie.videos.results[0].key}` : null;
        const director = tmdbMovie.credits.crew.find(person => person.job === 'Director');

        return {
          id: tmdbMovie.id,
          title: tmdbMovie.title,
          poster_path: tmdbMovie.poster_path,
          overview: tmdbMovie.overview,
          vote_average: tmdbMovie.vote_average,
          release_date: tmdbMovie.release_date,
          tagline: tmdbMovie.tagline,
          runtime: tmdbMovie.runtime,
          genres: tmdbMovie.genres,
          video_url: videoUrl,
          director: director ? director.name : 'Unknown', // 감독 정보가 없을 경우 'Unknown'으로 처리
        };
      }
    });
    
    // 모든 TMDb 정보를 기다려서 movies에 저장
    movies.value = await Promise.all(tmdbPromises);
  } catch (error) {
    console.error('Failed to fetch movies:', error);
  }
};

// 이미지 URL을 가져오는 함수
const getMoviePosterUrl = (posterPath) => {
  if (!posterPath) {
    return '';
  }
  return `https://image.tmdb.org/t/p/w200${posterPath}`;
};

// 현재 라우터 가져오기
const router = useRouter();

// 컴포넌트가 마운트될 때 영화 데이터를 불러옴
onMounted(() => {
  fetchBoxOffice();
  initializeSwiper();
});

const initializeSwiper = () => {
  const mySwiper = new Swiper('.swiper-container', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    spaceBetween: 250, // movie 요소 포스터 간격 조절
    coverflowEffect: {
      rotate: 50,
      stretch: 0,
      depth: 100,
      modifier: 1,
      slideShadows: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    
  });
    // Swiper 초기화 후에 버튼 동작하도록 설정
  mySwiper.init();
  // 슬라이드 각도 업데이트
  mySwiper.update();
};

function openModal(movie) {
  selectedMovie.value = movie;
  document.getElementById('boxOfficeModal').style.display = 'block';
}

function closeModal() {
  selectedMovie.value = null;
  document.getElementById('boxOfficeModal').style.display = 'none';
}

function closeModalOutside(event) {
  if (event.target === document.getElementById('boxOfficeModal')) {
    closeModal();
  }
}

window.onclick = function (event) {
  closeModalOutside(event);
}


const allmovies = ref([]);

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
    console.log("Related Movies:", randomRelatedMovies);
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
.recommend-container {
  margin-top: 100px;
}

.swiper-title {
  text-align: center; 
  margin-top: 25px; 
  font-size: 24px; 
  font-family: 'Noto Sans KR', sans-serif; 
  font-weight: bold;
  width: 300px;
}
.text-sort {
  text-align: center;
  color: white;
  font-weight: 1000;
  font-family: Cute Font;
  font-size: 80px;
}
.card-list {
  display: flex;
  flex-wrap: nowrap;
  overflow: auto;
}

.cardrev {
  margin-right: 30px;
}

.cardrev img {
  transition: transform 0.3s; /* 변환 효과에 대한 전환 설정 추가 */
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
  color: whitesmoke
  /* 기타 스타일 속성 추가 가능 */
}

/* .movie-info {
  display: flex;
  flex-direction: column;
  align-items: center;
} */

.swiper-container {
  color: white;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.swiper-slide {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  width: 100px;
  height: auto;
  transition: transform 0.3s ease-in-out;
}

.swiper-slide:hover {
  transform: translateY(-30px); /* 아래로 5px 이동 */
}

.swiper-button-next,
.swiper-button-prev {
  color: #fff;
}

</style>
