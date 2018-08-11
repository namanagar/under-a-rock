<template>
  <div class="col-sm-12 col-md-12">
    <div v-for="(sublist, sublistIndex) in sublists" :key="sublistIndex" class="row sublist">
      <div v-for="(article, index) in sublists[sublistIndex]" :key="index" class="col-sm-12 col-md-12">
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
    </div>
  </div>
</template>

<script>
export default {
  name: "ArticleView",
  props: ["articles"],
  data() {
    return {
      pageNumber: 0
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
    sublists() {
      var sublists = [];
      var chunk = [];
      var chunkCounter = 0;
      for (var i = 0; i < this.articles.length; i++) {
        chunk.push(this.articles[i]);
        if (chunk.length == 1 | chunk.length == this.articles.length - chunkCounter*1) {
          sublists.push(chunk);
          chunk = [];
          chunkCounter += 1;
        }
      }
      return sublists;
    },
    pageCount(){
      let l = this.articles.length,
          s = 3; // 3 per page
      return Math.floor(l/s);
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
@media screen and (min-width: 600px) {
    .sublist{
      margin-bottom: .5em;
    }
    #card{
      text-align: center;
      margin: 0.25em;
    }
}
</style>
