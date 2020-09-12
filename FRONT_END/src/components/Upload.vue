<template>
  <v-row justify="center">
    <v-col fluid>
      <v-sheet class="pa-3">
        <h1>Plese input image file</h1>
        <v-form ref="form">
          <!--動画用
          <video v-if="uploadVideoUrl" controls>
            <source :src="uploadVideoUrl" />
            このブラウザではビデオ表示がサポートされていません
          </video>
          <v-file-input
            v-model="input_video"
            accept="video/*"
            show-size
            label="動画ファイルをアップロードしてください"
            prepend-icon="mdi-video"
            @change="onVideoPicked"
          ></v-file-input>
          -->
          <!--face textの選択は移動しました-->
          <!--隠し方のスタイルの選択は移動しました-->
          <!--"detectImageURL"がある場合、"uploadImageURL"に代わり表示する-->
          <img v-if="detectImageURL" :src="detectImageURL" width="80%" />
          <img v-else-if="uploadImageUrl" :src="uploadImageUrl" width="80%" />
          <v-file-input
            v-model="input_image"
            accept="image/*"
            show-size
            label="画像ファイルをアップロードしてください"
            prepend-icon="mdi-image"
            @change="onImagePicked"
          ></v-file-input>
          <!--確認用
          <h3>{{checkedfaces}}</h3>
          -->
          <div v-if="uploadImageUrl">
            <h2>How do you want to hide?</h2>
            <div>
              <v-row  justify="space-around" class="mx-2">
                <v-select :items="styles"
                          v-model="checkedstyle"
                          label="How to hide"
                          outlined></v-select>
              </v-row>
            </div>
            <h2>Which contents do you want to hide?</h2>
            <div>
              <v-row justify="space-around">
                <v-checkbox v-model="isface" class="mx-2" label="face"></v-checkbox>
                <v-checkbox v-model="istext" class="mx-2" label="text"></v-checkbox>
              </v-row>
            </div>
            <v-btn class="ma-4"
                   :loading="isloadging_detext"
                   :disabled="isloadging_detext"
                   color="deep-purple lighten-3"
                   @click="makeDetectImg">
              DETECT
            </v-btn>
          </div>
          <!--face,textの選択はDETECT実行後---------------------------->
          <div v-if="detectImageURL">
            <h2>Chose the items that you want to hide.</h2>
            <v-card class="mx-auto my-1"
                    max-width="500">
              <v-container v-if="isface" fluid>
                <v-row align="center">
                  <v-select v-model="checkedfaces"
                            :items="faces"
                            item-text="id"
                            :menu-props="{ maxHeight: '400' }"
                            label="Face"
                            multiple
                            hint="Pick some faces"
                            persistent-hint></v-select>
                </v-row>
              </v-container>
            </v-card>
            <v-card class="mx-auto"
                    max-width="500">
              <v-container v-if="istext" fluid>
                <v-row align="center">
                  <v-select v-model="checkedtexts"
                            :items="texts"
                            item-text="id"
                            :menu-props="{ maxHeight: '400' }"
                            label="Text"
                            multiple
                            hint="Pick some texts"
                            persistent-hint></v-select>
                </v-row>
              </v-container>
            </v-card>
            <!--UPLAODボタンは移動しました-->
            <v-btn class="ma-4"
                   :loading="isloading_run"
                   :disabled="isloading_run"
                   color="deep-purple lighten-3"
                   @click="makeMosaicImg">
              RUN
            </v-btn>
          </div>
          <div v-if="mosaicImageUrl">
            <img :src="mosaicImageUrl"
                   width="80%" />
            <div class="text-center">
              <a :href="mosaicImageUrl" download style="color: white; font-weight: bold; text-decoration: none;">
                <v-btn class="ma-4" rounded color="green darken-3" dark>save</v-btn>
              </a>
            </div>
          </div>
        </v-form>
        <!--twitter-->
        <div class="twitter_share">
          <v-btn @click="twitterShare" color="#00acee"><i class="fab fa-twitter"></i><v-text>Tweet</v-text></v-btn>
        </div>
      </v-sheet>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      input_video: null,
      input_image: null,
      uploadVideoUrl: '',
      uploadImageUrl: '',
      imgName:'',
      imgExtent:'',
      //顔検出後の画像のURL
      detectImageURL:'',
      //生成したモザイク画像のURL
      mosaicImageUrl: '',
      //ここには認識した顔の画像を入れてもろて
      //faces: null,
      //texts: null,
      faces: [],
      texts: [],
      //ここにはチェックしたface.idが入るからよろしく
      checkedfaces: [],
      checkedtexts: [],
      //ボタン関係
      loader: null,
      loading: false,
      //顔と文字の選択
      isface: true,
      istext: false,
      //隠し方のスタイル
      styles: ["mosaic", "smyle", "sad"],
      checkedstyle: "",
      isloadging_detext:false,
      isloading_run:false,
    }
  },
  watch: {
    //ボタン関係
    loader () {
      const l = this.loader
      this[l] = !this[l]
    },
  },
  methods: {
    onVideoPicked(file) {
      if (file !== undefined && file !== null) {
        if (file.name.lastIndexOf('.') <= 0) {
          return
        }
        const fr = new FileReader()
        fr.readAsDataURL(file)
        fr.addEventListener('load', () => {
          this.uploadVideoUrl = fr.result
        })
      } else {
        this.uploadVideoUrl = ''
      }
    },
    onImagePicked(file) {
      if (file !== undefined && file !== null) {
        if (file.name.lastIndexOf('.') <= 0) {
          return
        }
        const dotpos = file.name.lastIndexOf('.')
        const fr = new FileReader()
        fr.readAsDataURL(file)
        fr.addEventListener('load', () => {
          this.uploadImageUrl = fr.result
          //ここに顔検出後の画像を入れる処理
          //detectImageURL=顔検出した四角つき画像のURL
          //
          //
          this.imgName = file.name.slice(0,dotpos-1)
          this.imgExtent = file.name.slice(dotpos+1)
          console.log(this.uploadImage)
        })
      } else {
        this.uploadImageUrl = ''
      }
    },
    makeDetectImg() {
      let self = this
      this.isloadging_detext=true
      this.loader = 'loading'//https://cos5year-hacku2020.azurewebsites.net
      this.$axios.post('https://cos5year-hacku2020.azurewebsites.net/api/mosaic/upload', {
        image: this.uploadImageUrl,
        name: this.imgName,
        extent:this.imgExtent,
        face:this.isface,
        text:this.istext
      },{withCredentials : true})
      .then(function (response) {
        console.log(response.data.image);
        self.uploadImageUrl = response.data.image;
        self.detectImageURL =response.data.image;
        self.faces = response.data.list.face
        self.texts = response.data.list.text
        self.isloadging_detext=false
      })
      .catch(function(error){
        self.isloadging_detext=false
        console.log(error);
      })
            
      //モザイク画像を生成する処理をここに入れられる？
      //右辺のthis.uploadImgUrlを生成したモザイク画像に差し変えてほしい
            
    },
    makeMosaicImg() {
      this.loader = 'loading'
      this.isloading_run=true
      let self = this
      //https://cos5year-hacku2020.azurewebsites.net
      this.$axios.post('https://cos5year-hacku2020.azurewebsites.net/api/mosaic/mosaicaction', {
        list_face: this.checkedfaces.map(function(item){
          return {box:self.faces[item-1].box,type:self.faces[item-1].type}
      }),
        list_text: this.checkedtexts.map(function(item){
          return {box:self.texts[item-1].box,type:self.texts[item-1].type}
      })
      },{withCredentials : true})
      .then(function (response) {
        console.log(response.data.image);
        self.mosaicImageUrl = response.data.image;
        self.isloading_run=false
      })
      .catch(function(error){
        console.log(error);
        self.isloading_run=false
      })
    },
    twitterShare(){
      //シェアする画面を設定
      var shareURL = 'https://twitter.com/intent/tweet?text=' + "ツイッターシェアボタンのサンプルコード" + "%20%23Cos5year";  
      //シェア用の画面へ移行
      location.href = shareURL
    },
  }
}
</script>
