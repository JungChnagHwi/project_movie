<template>
  <div>
    <table class="custom-table">
      <thead>
      <tr>
          <th colspan="1" style="width: 5%;"><span class = "th">No.</span></th>
          <th colspan="1" style="width: 30%"><span class = "th">MovieTitle</span></th>
          <th colspan="1" style="width: 40%"><span class = "th">ArticleTitle</span></th>
          <th colspan="1" style="width: 10%"><span class = "th">User</span></th>
          <th colspan="1" style="width: 15%"><span class = "th">rating</span></th>
      </tr>
     
    </thead>

        <ReviewListItem
        v-for="review in paginatedReviews"
        :key="review.id"
        :review="review"
        />
      <!-- </tr> -->
    </table>
    
    <nav v-if="totalPages > 1" style="text-align: center;"> 
      <ul class="pagination" style="list-style: none; display: inline-block; padding: 0;">
        <li v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }" style="display: inline-block; margin: 0 5px;">
          <a @click="changePage(page)" href="#" style="text-decoration: none; color: white;">{{ page }}</a>
        </li>
      </ul>
    </nav>
  </div>

</template>

<script setup>
import { useCounterStore } from '@/stores/counter';
import ReviewListItem from '@/components/ReviewListItem.vue';
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const store = useCounterStore();

const currentPage = ref(1);
const pageSize = 10;

const paginatedReviews = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize
  const endIndex = startIndex + pageSize
  return store.reviewList.slice(startIndex, endIndex)
});

const totalPages = computed(() => Math.ceil(store.reviewList.length / pageSize))

const changePage = (page) => {
  currentPage.value = page
};

onMounted(() => {
  store.getReviewList()
});

console.log(store.reviewList)


</script>

<style>
.pagination {
  display: flex;
  list-style: none;
  padding: 0;
}

.pagination li {
  margin-right: 5px;
}

.pagination a {
  text-decoration: none;
  color: #333;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.pagination a:hover {
  background-color: #f0f0f0;
}

.pagination .active a {
  background-color: #007bff;
  color: #fff;
}
.custom-table {
  border-collapse: collapse;
  width: 100%;
}

th, td {
  border: 0;
  border-bottom: 1px solid white;
  padding: 8px;
  text-align: left;
  color: white; /* 글자색을 흰색으로 설정 */
}

/* 헤더 배경 투명하게 설정 */
th {
  background-color: transparent;
  color: #333;
}
.th {
  color: white;
}
.custom-table {
  margin-bottom: 10px;
}

@media (max-width: 768px) {
  th, td {
    display: block;
    width: 100%;
    box-sizing: border-box;
  }

  th {
    text-align: center;
  }
}



</style>
