<template>
  <div class="vid">
    <video
      v-bind:src="videoUrl"
      v-on:loadeddata="onPlayable"
      v-on:ended="onEnded"
      v-on:error="onError"
      playsinline controls />
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

video {
  max-width: 100%;
  max-height: 100%;
}
</style>

<script>
export default {
  name: "PlayerNativeVideo",
  props: ["videoUrl"],
  methods: {
    onPlayable: function() {
      let videoElem = document.getElementsByTagName("video")[0];
      videoElem.play();
    },
    onEnded: function() {
      this.$emit("ended");
    },
    onError: function() {
      this.$emit("ended");
    }
  }
}
</script>
