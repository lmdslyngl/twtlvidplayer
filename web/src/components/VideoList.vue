<template>
  <div id="videolist" class="video-list-inner">
    <div class="button-wrapper">
      <button class="uk-button" v-on:click="onLoadOlder">Load older</button>
    </div>
    <div
        v-for="video in videoList"
        v-bind:key="video['tweet_id']">
      <VideoListItem
          v-bind:videoitem="video"
          v-bind:selected="isSelected(video)"
          v-on:video-selected="onVideoSelected"
          v-on:request-scroll="onRequestScroll">
      </VideoListItem>
    </div>
    <div class="button-wrapper">
      <button class="uk-button" v-on:click="onLoadNewer">Load newer</button>
    </div>
  </div>
</template>

<style scoped>
.video-list-inner {
  height: 100%;
  overflow-y: scroll;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  align-content: center;
  padding: 10px;
}

</style>

<script>
import VideoListItem from "./VideoListItem.vue"
import Store from "../store.js";

export default {
  name: "VideoList",
  data: function() {
    return Store.state;
  },
  methods: {
    onVideoSelected: function(video) {
      Store.setPlayingVideoTweet(video);
    },
    onRequestScroll: function(top, bottom) {
      let myElem = document.getElementById("videolist");
      let visibleTop = myElem.scrollTop;
      let visibleBottom = myElem.scrollTop + myElem.clientHeight;
      if( top < visibleTop ) {
        myElem.scrollTo(0, top);
      }
      if( visibleBottom < bottom ) {
        myElem.scrollTo(0, top - (myElem.clientHeight - (bottom - top)));
      }
    },
    onLoadOlder: function() {
      Store.loadOlderVideo();
    },
    onLoadNewer: function() {
      Store.loadNewerVideo();
    },
    isSelected: function(video) {
      if( this.playingVideoTweet === null ) {
        return false;
      } else {
        return this.playingVideoTweet['tweet_id'] === video['tweet_id'];
      }
    }
  },
  components: {
    VideoListItem
  }
}
</script>
