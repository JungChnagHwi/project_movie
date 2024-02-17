import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useCounterStore = defineStore('counter', () => {
  
  const movies = ref([])
  const API_URL = 'http://127.0.0.1:8000'
  const router = useRouter()
  const allmovies = ref([])

  // token 새로고침 이후에도 유지하는 코드 1
  const token = ref(localStorage.getItem('token') || null);

  const allMovies = function () {
    axios({
      method: 'GET',
      url: `${API_URL}/movies/`,
      
    })
    .then((res) => {
      allmovies.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  }

  const signUp = function (payload){
    const username = payload.username
    const password1 = payload.password1
    const password2 = payload.password2

    axios({
      method: 'post',
      url: `${API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
    .then(res=>{
      console.log('회원가입 완료')
      console.log(res)
      const password = password1
      logIn({ username, password })
    })
    .catch(err=>console.log(err))
  }

  // const token = ref(null)

  const logIn = function(payload){
    const username = payload.username
    const password = payload.password
    axios({
      method:'post',
      url: `${API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
    .then(res=>{
      console.log('로그인 완료')
      console.log(res.data)
      token.value = res.data.key
      localStorage.setItem('token', token.value);
      router.push('/')
    })
    .catch(err=>console.log(err))
  }
  
  const reviewList = ref([])
  const getReviewList = function () {
    axios({
      method: 'get',
      url: `${API_URL}/reviews/review_create/`,
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then((res) =>{
        // console.log(res)
        reviewList.value = res.data
      })
      .catch((err) => {
        console.log(err)
      })
  }


  const isLogin = computed(()=>{
    if(token.value === null){
      return false
    } else {
      return true
    }
  })

  const logOut = function () {
    axios({
      method: 'post',
      url: `${API_URL}/accounts/logout/`,
    })
      .then((res) => {
        localStorage.removeItem('token');
        token.value = null
        router.push({ name: 'LoginView' })
      })
      .catch((err) => {
        console.log(err)
      })
  }



  const postList = ref([])
  const getPostList = function () {
    axios({
      method: 'get',
      url: 'http://127.0.0.1:8000/reviews/review_create/',
      headers: {
        Authorization: `Token ${token.value}`
      }
    })
      .then(res => {
        // console.log(res)
        postList.value = res.data
      })
      .catch(err => {
        console.log(err)
      })
    }


    const post = ref({})
    const getDetailPost = function (pk) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/reviews/reviews/${pk}/`
      })
        .then(res => post.value = res.data)
        .catch(err => console.log(err))
    }


    const Username = ref('')
    const Email = ref('')


    const getProfile = async function () {
      try {
        const response = await axios.get(`${API_URL}/accounts/user/`, {
          headers: {
            Authorization: `Token ${token.value}`
          }
        });
    
        // 여기서 문제가 있는 것 같습니다.
        Username.value = response.data.username; // 이 부분을 Username.value = response.data.username; 로 수정해야 합니다.
        Email.value = response.email;
      } catch (error) {
        console.error(error);
      }
    };


  
  // // 영화 API를 불러오는 함수
  // const getMovies = function () {
  //   axios({
  //     method:'get',
  //     url: `${API_URL}/movies/toprated/`,
  //     // url: 'https://api.themoviedb.org/3/movie/toprated',
      
  //     params: {
  //       api_key: '69b934b0175eaae9758e75483f1b07e2',
  //       language: 'ko-KR'
  //     }
  //     })
  //     .then((res)=>{
  //       movies.value = response.data.results
  //     })
  //     .catch (error) {
  //     console.error('Failed to fetch movies:', error)

  
  return { getReviewList, allMovies, signUp, logIn, 
    token, isLogin, logOut, reviewList, API_URL,
  postList, getPostList, post, getDetailPost, 
  Email, Username, getProfile, allmovies}

} , { persist: true })






