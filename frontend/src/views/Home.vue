<template>
  <PatchMeta :title="section ? section : 'Minimal Vue3 + Markdown blog engine'" />

  <div :style="`background-color: ${VUE_APP_MAIN_BG_CSS_COLOR}; color: ${VUE_APP_MAIN_TEXT_CSS_COLOR};`">
    <!-- HEADER -->
    <BlogHeader class="mb-5" />

    <div class="container p-2">
      <div class="row border">
        <div class="col border">
          <h3>
            Attack Area
          </h3>
          <hr>
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
        </div>
        <div class="col border">
          <h3>Defend Area</h3>
          <hr>
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
          <img style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
        </div>
      </div>
      <hr>

      <h3> Hero Pool </h3>
      <div class="col border">
        <h4>Selected Items</h4>
        <div class="row border">
          <div class="col-md-12">
            <ul class="group" style="height: 300px; overflow-y: auto;">
              <img v-for="i in 50" :key="i" style="height: 100px; width: 100px; margin: 3px; background-color: rgba(255,0,0,0.1);" class="rounded" src="../assets/logo.png">
            </ul>
          </div>
        </div>
      </div>

      <br>
      <div class="text-center">
        <button type="button" class="btn btn-primary">Submit</button>
      </div>


    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, inject } from 'vue'
import BlogHeader from '../components/BlogHeader.vue'
import PatchMeta from '../components/PatchMeta.vue'
import paginate from '../utils/paginate'
import { PostIndex } from '../types/PostIndex'
import blogConfig from '../blog_config'

const { VUE_APP_POSTS_PER_PAGE, VUE_APP_MAIN_BG_CSS_COLOR, VUE_APP_MAIN_TEXT_CSS_COLOR } = blogConfig

const props = defineProps({
  section: {
    type: String,
    default: ''
  }
})

const postsIndex: PostIndex[] = inject<PostIndex[]>('postsIndex', [])
const currentPage = ref(1)

const pageStatus = computed(() => {
  const categoryPosts = props.section ? postsIndex.filter(({ section }) => section === props.section) : postsIndex
  const { startPage, endPage, startIndex, endIndex } = paginate(categoryPosts.length, currentPage.value, VUE_APP_POSTS_PER_PAGE)
  const prev = currentPage.value - 1 >= startPage ? currentPage.value - 1 : 0
  const next = currentPage.value + 1 <= endPage ? currentPage.value + 1 : 0
  const midPages = [prev, currentPage.value, next].filter(p => p > startPage && p < endPage)

  const visiblePosts = categoryPosts.slice(startIndex, endIndex + 1)

  return {
    startPage,
    midPages,
    endPage,
    visiblePosts
  }
})
</script>
