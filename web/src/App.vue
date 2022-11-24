<template>
  <div id="app">
    <div class="wrapper">
      <div class="video-list-area">
        <VideoList
            v-bind:videolist="videoList">
        </VideoList>
      </div>
      <div class="player-area">
        <PlayerCard
            v-bind:video-tweet="playingVideoTweet">
        </PlayerCard>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  display: grid;
  grid-template-columns: 360px 1fr;
  height: 100vh;
}

.video-list-area {
  padding: 0;
  height: 100vh;
}

.player-area {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>

<script>
import VideoList from "./components/VideoList.vue";
import PlayerCard from "./components/PlayerCard.vue";
import {API} from "./api.js";
import Store from "./store.js";
import {Hotkey} from "./hotkey.js";

export default {
  name: "App",
  data: function() {
    return Store.state;
  },
  mounted: function() {
    Hotkey.init();

    let api = new API();

    // 最新の20件の動画を取得し，最新の動画を選択する
    api.getVideoListUntil(null, 20)
      .then((response) => {
        Store.setVideoList(response);
        Store.setPlayingVideoTweet(response[response.length - 1]);
      });
  },
  methods: {
    onVideoSelected: function(video) {
      Store.setPlayingVideoTweetId(video);
    }
  },
  components: {
    VideoList,
    PlayerCard
  }
}

</script>

