<template>
  <div>
          <div style="position: relative;">
              <v-parallax :fixed="true" height="700" src="../assets/home1.jpg">
              <h1>守ろう、個人情報</h1>
              </v-parallax>
            </div>
          <div style="background-color: #fff; height: 10vh;"></div>
            <h1 style="margin-top: 0; padding-top: 20px;">What this</h1>
            <h3>ここになんか説明を入れる.</h3>
            <h1 style="margin-top: 0; padding-top: 20px;">HOW TO USE</h1>
            <div class="section_1 ratio">
              <div class="content_left">
                <div class="ratioImg" v-bind:class={active:isloaded1}>
                  <p>1</p>
                </div>
                <div class="detail" style="transition-delay: 0.2s" v-bind:class={active:isloaded1}>
                  <p>画像を用意</p>
                </div>
              </div>
              <div class="content_right">
                <div class="detail" style="transition-delay: 0.6s" v-bind:class={active:isloaded1}>
                  <p>アップロード</p>
                </div>
                <div class="ratioImg type02" style="transition-delay: 0.4s" v-bind:class={active:isloaded1}>
                  <p>2</p>
                </div>
              </div>
              <div class="content_left">
                <div class="ratioImg" style="transition-delay: 0.8s" v-bind:class={active:isloaded1}>
                  <p>3</p>
                </div>
                <div class="detail" style="transition-delay: 1.0s" v-bind:class={active:isloaded1}>
                  <p>選択</p>
                </div>
              </div>
              <div class="content_right">
                <div class="detail" style="transition-delay: 1.4s" v-bind:class={active:isloaded1}>
                  <p>完成！</p>
                </div>
                <div class="ratioImg" style="transition-delay: 1.2s" v-bind:class={active:isloaded1}>
                  <p>4</p>
                </div>
              </div>
            </div>
            
            <div style="position: relative; z-index: 9999; background-color: #fff;">
              <h1 style="margin:0;">モザイク処理後の写真</h1>
              <v-parallax :fixed="true" height="600" src="../assets/home2.jpg">
              </v-parallax>
            </div>
            <div style="background-color: #fff; height: 10vh"></div>
            <h1>特徴</h1>
            <div style="background-color: #fff; height: 100vh;"></div>
    </div>
</template>
<script>
export default {
  data(){
    return{
      isloaded1:false,
      isloaded2:false,
      isloaded3:false
    }
  },
  mounted() {
    let self = this
    const scene1 = this.$scrollmagic
      .scene({
        triggerElement: '#work-trigger',
        triggerHook: 0.5,
        offset:100,
        duration: 900,
        reverse: false
      })
      .setTween('#work-image', {
        css: {
          opacity: '1'
        }
      })
    const scene2 = this.$scrollmagic
      .scene({triggerElement: '#parallax1',triggerHook: "onEnter", duration: "200%",reverse:true})
      .setTween("#parallax1 > div", {css:{y: "60%"}})
    const scene3 = this.$scrollmagic
      .scene({triggerElement: '#parallax2',triggerHook: "onEnter", duration: "200%",reverse:true})
      .setTween("#parallax2 > div", {css:{y: "60%"}})
    const scene4 = this.$scrollmagic
      .scene({triggerElement: '#parallax3',triggerHook: "onEnter", duration: "200%",reverse:true})
      .setTween("#parallax3 > div", {css:{y: "60%"}})

    const scene5 = this.$scrollmagic
      .scene({triggerElement: '.section_1.ratio',triggerHook: "onEnter",reverse:true})
      .on("enter", function(event) {
        console.log("Scene progress changed to " + event.progress)
        self.isloaded1 = true
      })
    // ---- ↓ triggerのヘルプを表示 ----
    // .addIndicators({ name: 'OK' })

    this.$scrollmagic.addScene(scene1)
    this.$scrollmagic.addScene(scene2)
    this.$scrollmagic.addScene(scene3)
    this.$scrollmagic.addScene(scene4)
    this.$scrollmagic.addScene(scene5)
  }
}
</script>
<style  scoped  lang="scss">
  .parallaxParent {
      height: 100vh;
      overflow: hidden;
    }
  .parallaxParent > * {
    height: 200%;
    position: relative;
    top: -100%;
  }

// ---- ↓ アニメーション実行前のスタイル（非表示にしておく） ----
 #work-image {
   opacity: 0;
 }

.content_left {
  text-align:left;
  width: 100%;
  .ratioImg {
    margin: 1%;
    width: 160px;
    transition: 0.4s;
    transform: scale(0);
    display: inline-block;
    vertical-align: middle;
    &.active {
      transform: scale(1);
    }
    &.type02 {
      transition-delay: 0.4s; // ここがポイント！！
    }
    &.type03 {
      transition-delay: 0.8s; // ここがポイント！！
    }
    &.type04 {
      transition-delay: 1.2s; // ここがポイント！！
    }
    &.type05 {
      transition-delay: 1.6s; // ここがポイント！！
    }
    p {
      text-align: center;
      font-size: 60px;
      border: 4px solid #000;
      border-radius: 50%;
      width: 160px;
      height: 160px;
      line-height: 145px;
      position: relative;
    }
    .active {
      transform: scale(1);
    }
    .type02 {
      transition-delay: 0.4s; // ここがポイント！！
    }
    .type03 {
      transition-delay: 0.8s; // ここがポイント！！
    }
    .type04 {
      transition-delay: 1.2s; // ここがポイント！！
    }
    .type05 {
      transition-delay: 1.6s; // ここがポイント！！
    }
  }
  .detail {
    transition: 0.4s;
    transition-delay: 0.4s;
    transform: scale(0);
    display: inline-block;
    vertical-align: middle;
  &.active {
      transform: scale(1);
  &.type02 {
      transition-delay: 0.4s; // ここがポイント！！
    }
    &.type03 {
      transition-delay: 0.8s; // ここがポイント！！
    }
    &.type04 {
      transition-delay: 1.2s; // ここがポイント！！
    }
    &.type05 {
      transition-delay: 1.6s; // ここがポイント！！
    }
    }
    p {
      text-align: center;
      font-size: 40px;
      line-height: 145px;
      position: relative;
    }
  }
}

.content_right {
  text-align:right;
  width: 100%;
  .ratioImg {
    margin: 1%;
    width: 160px;
    transition: 0.4s;
    transform: scale(0);
    display: inline-block;
    vertical-align: middle;
    &.active {
      transform: scale(1);
    }
    &.type02 {
      transition-delay: 0.4s; // ここがポイント！！
    }
    &.type03 {
      transition-delay: 0.8s; // ここがポイント！！
    }
    &.type04 {
      transition-delay: 1.2s; // ここがポイント！！
    }
    &.type05 {
      transition-delay: 1.6s; // ここがポイント！！
    }
    p {
      text-align: center;
      font-size: 60px;
      border: 4px solid #000;
      border-radius: 50%;
      width: 160px;
      height: 160px;
      line-height: 145px;
      position: relative;
    }
  }
  .detail {
    transition: 0.4s;
    transition-delay: 0.4s;
    transform: scale(0);
    display: inline-block;
    vertical-align: middle;
  &.active {
      transform: scale(1);
    }
  &.type02 {
      transition-delay: 0.4s; // ここがポイント！！
    }
    &.type03 {
      transition-delay: 0.8s; // ここがポイント！！
    }
    &.type04 {
      transition-delay: 1.2s; // ここがポイント！！
    }
    &.type05 {
      transition-delay: 1.6s; // ここがポイント！！
    }
    p {
      text-align: center;
      font-size: 40px;
      line-height: 145px;
      position: relative;
    }
  }
}
</style>