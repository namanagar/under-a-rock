<template>
  <div class="col-sm-12 col-md-12">
    <div v-for="(sublist, sublistIndex) in sublists" :key="sublistIndex" class="row sublist">
      <div v-for="(article, index) in sublists[sublistIndex]" :key="index" class="col-sm-12 col-md-4">
        <div class="card" id="card">
          <div class="card-header">
            <h5>{{ article.name }} - {{ article.title }}</h5>
          </div>
          <div class="card-body text-muted">
            <div style="margin-bottom: 1em">{{ article.lede }}...</div>
            <a @click="openLink(article)" class="btn btn-sm btn-outline-secondary">keep reading</a>
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
        if (chunk.length == 3 | chunk.length == this.articles.length - chunkCounter*3) {
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
      margin-bottom: 1.5em;
    }
    #card{
      text-align: center;
      margin: 0.25em;
    }
}
</style>
