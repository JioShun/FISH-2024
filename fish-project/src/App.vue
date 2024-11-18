<template>
    <v-app class="app-wrapper">
        <!-- ヘッダー -->
        <v-app-bar :elevation="4" color="#A0BDE6">
            <template v-slot:prepend>
                <v-app-bar-nav-icon
                    variant="text"
                    @click.stop="drawer = !drawer"
                ></v-app-bar-nav-icon>
            </template>
            <v-app-bar-title><strong>SarfAR</strong></v-app-bar-title>
        </v-app-bar>

        <v-navigation-drawer
            v-model="drawer"
            :location="$vuetify.display.mobile ? 'left' : undefined"
            temporary
        >
            <p>何もないよ</p>
        </v-navigation-drawer>

        <!-- メイン部分 -->
        <v-main class="main-content">
            <div v-if="currentView === 'chat'">
                <ChatComponent />
            </div>

            <div v-if="currentView === 'map'">
                <p>マップが欲しかった</p>
                <img :src="require('@/assets/map.png')" alt="" />
            </div>

            <div v-if="currentView === 'list'">
                <p>教室を一覧表示したかった</p>
                <v-container fluid>
                    <v-row dense>
                        <v-col v-for="n in 8" :key="n" cols="6">
                            <v-sheet height="96">教室だよ</v-sheet>
                        </v-col>
                    </v-row>
                </v-container>
            </div>
        </v-main>

        <!-- フッター -->
        <v-bottom-navigation
            :elevation="4"
            grow
            v-model="currentView"
            class="footer"
        >
            <v-btn value="chat" class="back-color">
                <v-icon color="black">forum</v-icon>
                <span>チャット</span>
            </v-btn>

            <v-btn value="map" class="back-color">
                <v-icon>map</v-icon>
                <span>マップ</span>
            </v-btn>

            <v-btn value="list" class="back-color">
                <v-icon>view_list</v-icon>
                <span>リスト</span>
            </v-btn>
        </v-bottom-navigation>
    </v-app>
</template>

<script setup>
import { ref } from "vue";
import ChatComponent from "./components/ChatComponent.vue";

const currentView = ref("chat"); // メニュー
const drawer = ref(false); // サイドバー
</script>

<style>
* {
    margin: 0;
    padding: 0;
    /* cssデバッグ用 */
    /* border: 1px solid #ccc; */
}

.app-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.main-content {
    background-color: #f2f2f2;
    overflow-y: auto;
}

.footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    z-index: 1001;
}

.back-color {
    background-color: #a0bde6;
}

img {
    width: 100%;
    height: auto;
}
</style>
