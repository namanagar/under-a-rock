<template>
  <div class="col-sm-12 col-md-12">
    <div v-for="article in paginatedData" :key="article.url">
        <div class="card" id="card">
          <div class="card-header">
            {{ article.title }}
          </div>
          <div class="card-body text-muted">
            <div style="margin-bottom: .75em">{{ article.lede }}...</div>
            <a @click="openLink(article)" class="btn btn-sm btn-secondary">keep reading on {{ article.name.toLowerCase() }}</a>
          </div>
        </div>
    </div>
    <div class="row no-gutters">
      <div class="ml-auto">
        <button :disabled="this.pageNumber == 0" type="button" class="btn btn-sm btn-outline-light" @click="pageZero()">first</button>
      </div>
      <div class="btn-group ml-auto mr-auto" role="group" aria-label="Page navigation">
        <button :disabled="this.pageNumber == 0" type="button" class="btn btn-sm btn-outline-light" @click="prevPage()">🠄</button>
        <button :disabled="this.pageNumber == this.pageCount - 1 || this.pageCount == 0" type="button" class="btn btn-sm btn-outline-light" @click="nextPage()">🠆</button>
      </div>
      <div class="mr-auto">
        <button :disabled="this.pageNumber == this.pageCount - 1 || this.pageCount == 0" type="button" class="btn btn-sm btn-outline-light" @click="pageLast()">last</button>
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
    },
    pageZero(){
      this.pageNumber = 0;
    },
    pageLast(){
      this.pageNumber = this.pageCount - 1;
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
      return this.sortedArticles.slice(start, end);
    },
    sortedArticles(){
      return this.articles.sort(function(a, b){
        return b.timestamp - a.timestamp;
      })
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
  margin: .5em  0  .5em  .5em;
  font-size: .9em;
  color: #2c3e50;
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

.btn-secondary{
  color: #fff !important;
}

@media screen and (min-width: 600px) {
    #card{
      text-align: center;
      margin: 0.25em 0 0.25em 0.25em;
    }
}
</style>