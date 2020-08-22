<template>
  <div class="vid" v-html="iframeHtml"></div>
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
  name: "PlayerSoundCloud",
  props: ["url"],
  data: function() {
    return {
      iframeHtml: ""
    }
  },
  mounted: function() {
    this.updateIFrameHtml();
  },
  methods: {
    updateIFrameHtml: function() {
      this.fetchIFrameHtml(this.url)
        .then((html) => {
          this.iframeHtml = html;
          this.$nextTick(() => {
            // 次のフレーム（iframeが追加されたとき）に
            // SoundCloudWidgetのイベントのバインドを行う
            this.bindPlayerEvent();
          });
        }).catch(() => {
          this.iframeHtml = "";
        });
    },
    fetchIFrameHtml: function(url) {
      let vidElem = document.getElementsByClassName("vid")[0];
      let vidHeight = vidElem.clientHeight;

      return axios.get("https://soundcloud.com/oembed", {
        params: {
          format: "json",
          url: url,
          maxheight: vidHeight,
          auto_play: "true"
        }
      }).then((response) => {
        return Promise.resolve(response.data["html"]);
      });
    },
    bindPlayerEvent: function() {
      let widgetElem = document.querySelector(".vid iframe");
      let widget = SC.Widget(widgetElem);
      widget.bind(SC.Widget.Events.READY, this.onPlayable);
      widget.bind(SC.Widget.Events.FINISH, this.onEnded);
    },
    onPlayable: function() {
      let widgetElem = document.querySelector(".vid iframe");
      let widget = SC.Widget(widgetElem);
      widget.play();
    },
    onEnded: function() {
      this.$emit("ended");
    }
  },
  watch: {
    url: function() {
      this.updateIFrameHtml();
    }
  }
}
</script>
