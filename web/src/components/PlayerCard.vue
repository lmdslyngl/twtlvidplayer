<template>
  <div
      class="player-area-inner"
      v-if="playingVideoTweet !== null">

    <div class="uk-card uk-card-default player-card">
      <div class="uk-card-media-top">
        <div class="video-wrapper">
          <PlayerMultiplexer
              v-bind:url="playingVideoTweet['video_url']"
              v-bind:video-type="playingVideoTweet['video_type']"
              v-on:ended="onVideoEnded">
          </PlayerMultiplexer>
        </div>
      </div>

      <div class="uk-card-body">
        <div class="tweet-card-grid">
          <div class="tweet-card-thumbnail">
            <img v-bind:src="playingVideoTweet['author_thumbnail_url']">
          </div>
          <div>
            <p class="author">
              {{ playingVideoTweet["author_name"] }}
              (@{{ playingVideoTweet["author_screen_name"] }})
            </p>
            <p>{{ playingVideoTweet["body"] }}</p>
            <a href="#" target="_blank">Twitterで開く</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.video-wrapper {
  width: 640px;
  height: 480px;
  background-color: black;
}

.player-card {
  max-width: 640px;
}

.tweet-card-grid {
  display: grid;
  grid-template-columns: 55px 1fr;
  justify-content: center;
}

.tweet-card-grid p {
  margin: 0 0 5px 0;
}

.tweet-card-grid .author {
  font-weight: bold;
}

.tweet-card-thumbnail {
  text-align: left;
}

.tweet-card-body {
  width: 100%;
}
</style>

<script>
import PlayerMultiplexer from "./PlayerMultiplexer.vue";
import Store from "../store.js";

export default {
  name: "PlayerCard",
  data: function() {
    return Store.state;
  },
  components: {
    PlayerMultiplexer
  },
  methods: {
    onVideoEnded: function() {
      Store.nextVideo();
    }
  }
}
</script>
