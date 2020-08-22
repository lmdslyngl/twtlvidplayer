<template>
  <div class="vid">
    <div id="player-youtube"></div>
  </div>
</template>

<style scoped>
.vid {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
</style>

<script>
export default {
  name: "PlayerYouTube",
  props: ["url"],
  data: function() {
    return {
      player: null
    }
  },
  mounted: function() {
    this.updateYoutubeIFrame();
  },
  beforeDestroy: function() {
    this.player.stopVideo();
    this.player.clearVideo();
    this.player = null;
  },
  methods: {
    updateYoutubeIFrame: function() {
      if( this.player === null ) {
        let vidElem = document.getElementsByClassName("vid")[0];
        let vidWidth = vidElem.clientWidth;
        let vidHeight = vidElem.clientHeight;

        this.player = new YT.Player("player-youtube", {
          height: vidHeight,
          width: vidWidth,
          videoId: this.videoId,
          events: {
            "onReady": this.onPlayable,
            "onStateChange": this.onStateChange,
            "onError": this.onError
          }
        });
      } else {
        this.player.loadVideoById({ videoId: this.videoId });
      }
    },
    onPlayable: function(evt) {
      this.player.playVideo();
    },
    onStateChange: function(evt) {
      if( evt.data === YT.PlayerState.ENDED ) {
        this.$emit("ended");
      }
    },
    onError: function(evt) {
      this.$emit("ended");
    }
  },
  computed: {
    videoId: function() {
      let urlObj = new URL(this.url);
      return urlObj.searchParams.get("v");
    }
  },
  watch: {
    url: function() {
      this.updateYoutubeIFrame();
    }
  }
}
</script>
