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

        </div>
      </div>
      <hr>

      <h3>
        Show Area
      </h3>

    </div>

    <div v-for="entry in pageStatus.visiblePosts" :key="entry.id" class="container markdown-body p-3 p-md-4">
      <!-- TITLE -->
      <router-link :to="`/${entry.section}/${entry.id}`" class="text-reset">
        <h3 class="text-left m-0 p-0">
          {{ entry.title }}
        </h3>
      </router-link>

      <!-- Arena Area -->
      <p class="font-weight-light font-italic m-0 p-0" :class="!section ? 'text-right' : 'mb-3'">
        {{ entry.date }}
      </p>
      <router-link v-if="!section" :to="`/${entry.section}`" class="text-reset">
        <h6 class="m-0 p-0 text-right font-weight-bold">
          #{{ entry.section }}
        </h6>
      </router-link>

      <!-- POST INTRO -->
      <p class="font-weight-light mt-1">
        {{ entry.description }}
      </p>
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
