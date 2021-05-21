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

    let lastPlayingVideoId = 0;
    let api = new API();

    api.getConfig("last_playing_video_id")
      .then((response) => {
        lastPlayingVideoId = response["value"];
      }).then(() => {
        return api.getVideoListSince(lastPlayingVideoId, 20);
      }).then((response) => {
        Store.setVideoList(response);

        // 直近再生した動画を探す
        let lastPlayingVideo = response.find((x) => {
          return x["tweet_id"] === lastPlayingVideoId;
        });

        if( lastPlayingVideo === undefined ) {
          // 直近再生した動画が見つからなかった場合は，リストの最初の動画を選択
          Store.setPlayingVideoTweet(response[0]);
        } else {
          Store.setPlayingVideoTweet(lastPlayingVideo);
        }
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

