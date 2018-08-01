<template>
  <div class="col-sm-12 col-md-12">
    <div v-for="(sublist, sublistIndex) in sublists" :key="sublistIndex" class="row sublist">
      <div v-for="(article, index) in sublists[sublistIndex]" :key="index" class="col-sm-12 col-md-3">
        <div class="card" id="card">
          <div class="card-header">
            {{ article.name }}
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ article.title }}</h4>
            <a @click="openLink(article)" class="btn btn-sm btn-outline-secondary">link</a>
          </div>
          <div class="card-footer text-muted">
            {{ formatKeywords(article.keywords) }}
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
    return {};
  },
  methods: {
    formatKeywords(keywords) {
      var str = keywords.reduce(function(pre, next) {
        return pre + ", " + next;
      });
      return str;
    },
    openLink(article) {
      window.open(article.link, "_blank");
    }
  },
  computed: {
    sublists() {
      var sublists = [];
      var chunk = [];
      var chunkCounter = 0;
      for (var i = 0; i < this.articles.length; i++) {
        chunk.push(this.articles[i]);
        if (chunk.length == 4 | chunk.length == this.articles.length - chunkCounter*4) {
          sublists.push(chunk);
          chunk = [];
          chunkCounter += 1;
        }
      }
      return sublists;
    }
  }
};
</script>

<style scoped>
#card {
  text-align: left;
  margin: 1.5em;
}
a {
  min-width: 100%;
}
.card-footer {
  font-size: 0.75em;
}

@media screen and (min-width: 600px) {
    .sublist{
      margin-bottom: 2em;
    }
    #card{
      text-align: center;
      margin: 0.25em;
    }
}
</style>
