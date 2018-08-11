<template>
  <div class="col-sm-12 col-md-12">
    <div v-for="article in paginatedData" :key="article.url">
        <div class="card" id="card">
          <div class="card-header">
            {{ article.title }}
          </div>
          <div class="card-body text-muted">
            <div style="margin-bottom: 1em">{{ article.lede }}...</div>
            <a @click="openLink(article)" class="btn btn-sm btn-outline-secondary">keep reading on {{ article.name.toLowerCase() }}</a>
          </div>
        </div>
    </div>
    <div class="row">
      <div class="btn-group ml-auto mr-auto" role="group" aria-label="Basic example">
        <button :disabled="this.pageNumber == 0" type="button" class="btn btn-sm btn-outline-secondary" @click="prevPage()">left</button>
        <button :disabled="this.pageNumber == this.pageCount -1" type="button" class="btn btn-sm btn-outline-secondary" @click="nextPage()">right</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ArticleView",
  props: ["articles"],
  data() {
    return {
      pageNumber: 0,
      size: 3 //3 articles per "page"
    };
  },
  methods: {
    formatKeywords(keywords) {
      var str = keywords.reduce(function(pre, next) {
        return pre + ", " + next;
      });
      return str;
    },
    openLink(article) {
      window.open(article.url, "_blank");
    },
    nextPage(){
      this.pageNumber++;
    },
    prevPage(){
      this.pageNumber--;
    }
  },
  computed: {
    pageCount(){
      let l = this.articles.length,
          s = this.size;
      return Math.floor(l/s);
    },
    paginatedData(){
      const start = this.pageNumber * this.size,
      end = start + this.size;
      return this.articles.slice(start, end);
    }
  },
  watch: {
    articles: function(){
      this.pageNumber = 0;
    }
  }
};
</script>

<style scoped>
#card {
  text-align: left;
  margin: .5em;
  font-size: .9em;
}
a {
  min-width: 100%;
  font-family: "Lato", sans-serif;
}
.card-footer {
  font-size: 0.75em;
}
.card-body {
  font-size: 0.85em;
}
.card-header {
  font-family: "Lato", sans-serif;
}
@media screen and (min-width: 600px) {
    #card{
      text-align: center;
      margin: 0.25em;
    }
}
</style>
