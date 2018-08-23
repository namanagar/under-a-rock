<template>
    <transition name="modal">
        <div class="modal">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">about</h3>
                        <button type="button" class="close" @click="$emit('close')" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        <p>
                            <span id="logo">under a rock<span style="font-size: 2em; color: #4CB191">.</span></span> is a unique news aggregator, 
                            displaying the world’s top trending news in the form of a web. 
                            the network allows you to see the relationships between articles from around the world, 
                            giving them meaning in a larger context.
                        </p>
                        <p style="margin-top: 1.5em;">
                            just select the time period (in hours or days) you want to catch up on using the slider 
                            and a graph will appear. the bubbles are sized based on how often the topic shows up in the news.
                            clicking bubbles will filter the list of articles on the right (or below, on small screens) to articles
                            about all of the selected bubbles.
                        </p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-sm btn-secondary" @click="$emit('close')">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>
<script>
export default {
  name: "AboutModal",
  props: [],
  data() {
    return {
    };
  },
  methods: {
  }
};
</script>
<style scoped>
.modal{
    display: block;
}
.modal-title{
    color:#2c3e50;
}
p{
    color: #2c3e50;
    text-align: left;
    font-family: 'Work Sans';
}
#logo{
    font-family: "Lato" !important;
}
</style>
