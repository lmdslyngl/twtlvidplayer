<template>
  <div
      v-bind:id="elemId"
      class="uk-card cursor-pointer"
      v-bind:class="cardStyle"
      v-on:click="onClicked">
    <div class="uk-card-body card-padding">
      <div class="tweet-card-grid">
        <div class="tweet-card-thumbnail">
          <img v-bind:src="videoitem['author_thumbnail_url']">
        </div>
        <div class="tweet-card-body">
          <p class="author">
            {{ videoitem["author_name"] }} (@{{ videoitem["author_screen_name"] }})
          </p>
          <p class="created-at">
            {{ new Date(videoitem["created_at"] * 1000).toLocaleString() }}
          </p>
          <p class="body">{{ videoitem["body"] }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}

.card-padding {
  padding: 5px !important;
}

.tweet-card-grid {
  display: grid;
  grid-template-columns: 55px 1fr;
  justify-content: center;
}

.tweet-card-grid .author {
  font-weight: bold;
  margin: 0;
}

.tweet-card-grid .created-at {
  font-size: 70%;
  opacity: 0.8;
  margin: 0;
}

.tweet-card-grid .body {
  margin: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 280px;
}

.tweet-card-thumbnail {
  text-align: left;
}

.tweet-card-body {
  width: 100%;
}
</style>

<script>
export default {
  name: "VideoListItem",
  props: ["videoitem", "selected"],
  methods: {
    onClicked: function(evt) {
      this.$emit("video-selected", this.videoitem);
    }
  },
  computed: {
    cardStyle: function() {
      if( this.selected ) {
        return "uk-card-primary";
      } else {
        return "uk-card-default";
      }
    },
    elemId: function() {
      return "videolistitem-" + this.videoitem["tweet_id"];
    }
  },
  watch: {
    selected: function(newVal) {
      if( newVal ) {
        let myElem = document.getElementById(this.elemId);
        let clientRect = myElem.getBoundingClientRect();
        this.$emit(
          "request-scroll",
          myElem.offsetTop,
          myElem.offsetTop + clientRect.height);
      }
    }
  }
}
</script>
