
import {API} from "./api.js";

export default {
  debug: false,
  state: {
    videoList: [],
    playingVideoTweet: null
  },
  setVideoList(videoList) {
    if( this.debug ) {
      console.log("setVideoList called");
      console.log(videoList);
    }
    this.state.videoList = videoList;
  },
  setPlayingVideoTweet(tweet) {
    if( this.debug ) {
      console.log("setPlayingVideoTweet called");
      console.log(tweet);
    }
    this.state.playingVideoTweet = tweet;

    // 直近再生していた動画を登録
    new API().setConfig(
      "last_playing_video_id",
      this.state.playingVideoTweet["tweet_id"]);
  },
  nextVideo() {
    if( this.debug ) {
      console.log("nextVideo called");
    }
    let currentVideoIndex = this.state.videoList.findIndex((v) => {
      return v["tweet_id"] === this.state.playingVideoTweet["tweet_id"];
    });

    if( currentVideoIndex === this.state.videoList.length - 1 ) {
      // 現在の動画が最後の動画だった場合は新しいのを読み込む
      this.loadNewerVideo()
        .then(() => {
          if( currentVideoIndex === this.state.videoList.length - 1 ) {
            // 新しいのを読み込んでもまだこれが最後の動画だった場合はこのまま停止
          } else {
            this.setPlayingVideoTweet(this.state.videoList[currentVideoIndex + 1]);
          }
        });
    } else {
      this.setPlayingVideoTweet(this.state.videoList[currentVideoIndex + 1]);
    }
  },
  loadOlderVideo() {
    if( this.debug ) {
      console.log("loadOlderVideo called");
    }
    let oldestVideoId = this.state.videoList[0]["tweet_id"];
    return new API().getVideoListUntil(oldestVideoId, 20)
      .then((response) => {
        // 末尾に重複があるため削除
        response.pop();
        this.state.videoList = response.concat(this.state.videoList);
      });
  },
  loadNewerVideo() {
    if( this.debug ) {
      console.log("loadNewerVideo called");
    }
    let newestVideoId = this.state.videoList[this.state.videoList.length - 1]["tweet_id"];
    return new API().getVideoListSince(newestVideoId, 20)
      .then((response) => {
        // 先頭に重複があるため削除
        response.shift();
        this.state.videoList = this.state.videoList.concat(response);
      });
  }
};
