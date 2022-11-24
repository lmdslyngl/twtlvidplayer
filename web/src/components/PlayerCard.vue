<template>
  <div
      class="player-area-inner"
      v-if="sharedState.playingVideoTweet !== null">

    <div class="uk-card uk-card-default player-card">
      <div class="uk-card-media-top">
        <div class="video-wrapper">
          <PlayerMultiplexer
              v-bind:url="sharedState.playingVideoTweet['video_url']"
              v-bind:video-type="sharedState.playingVideoTweet['video_type']"
              v-on:ended="onVideoEnded"
              v-on:error="onError">
          </PlayerMultiplexer>
        </div>
      </div>

      <div class="uk-card-body">
        <div class="tweet-card-grid">
          <div class="tweet-card-thumbnail">
            <img v-bind:src="sharedState.playingVideoTweet['author_thumbnail_url']">
          </div>
          <div>
            <p
                class="retweeted-author"
                v-show="sharedState.playingVideoTweet['retweeted_author_name'] !== null">
              {{ sharedState.playingVideoTweet["retweeted_author_name"] }} がリツイート
            </p>
            <p class="author">
              {{ sharedState.playingVideoTweet["author_name"] }}
              (@{{ sharedState.playingVideoTweet["author_screen_name"] }})
            </p>
            <p>{{ sharedState.playingVideoTweet["body"] }}</p>
            <a v-bind:href="tweetUrl" target="_blank">Twitterで開く</a>
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

.tweet-card-grid .retweeted-author{
  font-size: 80%;
  color: rgb(150, 150, 150);
  margin: 0;
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
    return {
      privateState: {
        errorHistory: []
      },
      sharedState: Store.state
    }
  },
  components: {
    PlayerMultiplexer
  },
  methods: {
    onVideoEnded: function() {
      Store.prevVideo();
    },
    onError: function() {
      let current = new Date();
      this.privateState.errorHistory.push(current);

      // 過去1秒間のエラーが起きた時刻
      let errorInSecond = this.privateState.errorHistory.filter(
        time => current.getTime() - time.getTime() < 1000);

      if( errorInSecond.length < 3 ) {
        // エラーが1秒間に3回以内であれば次の動画に進む
        Store.nextVideo();
      } else {
        // それ以上は次の動画に進まない
        // ※連続してエラーが発生してどんどん動画が飛ばされる問題を防ぐため
      }

      this.privateState.errorHistory = errorInSecond;

    }
  },
  computed: {
    tweetUrl: function() {
      return "https://twitter.com/" +
        this.sharedState.playingVideoTweet["author_screen_name"] + "/status/" +
        this.sharedState.playingVideoTweet["tweet_id"];
    }
  }
}
</script>
