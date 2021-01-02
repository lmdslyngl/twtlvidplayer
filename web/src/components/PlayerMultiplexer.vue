<template>
  <div class="player-multiplexer">
    <PlayerNativeVideo
      v-bind:video-url="url"
      v-if="videoType === 1"
      v-on:ended="onEnded"
      v-on:error="onError">
    </PlayerNativeVideo>
    <PlayerSoundCloud
      v-bind:url="url"
      v-if="videoType === 2"
      v-on:ended="onEnded"
      v-on:error="onError">
    </PlayerSoundCloud>
    <PlayerYouTube
      v-bind:url="url"
      v-if="videoType === 3"
      v-on:ended="onEnded"
      v-on:error="onError">
    </PlayerYouTube>
  </div>
</template>

<style scoped>
.player-multiplexer {
  width: 100%;
  height: 100%;
}
</style>

<script>
import PlayerNativeVideo from "./PlayerNativeVideo.vue";
import PlayerSoundCloud from "./PlayerSoundCloud.vue";
import PlayerYouTube from "./PlayerYouTube.vue";

export default {
  name: "PlayerMultiplexer",
  props: ["url", "videoType"],
  methods: {
    onEnded: function() {
      this.$emit("ended");
    },
    onError: function() {
      this.$emit("error");
    }
  },
  components: {
    PlayerNativeVideo,
    PlayerSoundCloud,
    PlayerYouTube
  }
}
</script>
