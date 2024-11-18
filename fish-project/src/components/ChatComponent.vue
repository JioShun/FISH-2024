<template>
    <div class="chat">

        <!-- チャット -->
        <div class="chat-container">
            <ul class="chat-list">
                <li v-for="(message, index) in messages" :key="index"
                    :class="message.user === 'You' ? 'my-message' : 'other-message'">
                    <div class="message-bubble">
                        {{ message.text }}
                    </div>
                </li>
                <li v-if="isLoading" class="other-message">
                    <div class="message-bubble">
                        <span class="loading">
                            <span class="dot-1"><strong>.</strong></span>
                            <span class="dot-2"><strong>.</strong></span>
                            <span class="dot-3"><strong>.</strong></span>
                        </span>
                    </div>
                </li>
            </ul>
        </div>

        <!-- 案内ボタン -->
        <div v-if="showGuideButton" class="guide-button">
            <v-btn @click="guideOn" color="red-lighten-1" size="x-large" elevation="16" rounded="xl">案内開始</v-btn>
        </div>

        <!-- 入力フォーム -->
        <div class="input-form">
            <v-text-field v-model="userInput" append-inner-icon="double_arrow" label="メッセージを入力" variant="solo"
                @click:append-inner="sendInput" @keyup.enter="sendInput" :disabled="isLoading"></v-text-field>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const userInput = ref('')
const messages = ref([
    { user: 'Chatbot', text: 'こんにちは！私はSarfARです。未来大を案内することができます．' },
    { user: 'Chatbot', text: '質問があれば、何でも聞いてください！' },
])

const showGuideButton = ref(false)
const guideOn = () => {
    showGuideButton.value = false;
}

const isLoading = ref(false)

// ユーザーが入力したメッセージをchatbotに送信する関数
const sendInput = async () => {
    try {
        if (!userInput.value.trim()) return;
        isLoading.value = true; // ローディング表示用
        const currentInput = userInput.value;
        userInput.value = '';
        messages.value.push({ user: 'You', text: currentInput });

        // 案内チェック
        if (currentInput.includes('案内')) {
            showGuideButton.value = true;
            messages.value.push({ user: 'Chatbot', text: '承知しました。それではご案内します！' });
        } else {
            const response = await axios.post('http://127.0.0.1:5000/api/process', {
                input: currentInput,
            });
            messages.value.push({ user: 'Chatbot', text: response.data.message });
        }
    } catch (error) {
        console.error('Error sending input to backend:', error);
    } finally {
        isLoading.value = false;
    }
};

//eslint-disable-next-line
const addMessage = () => { // デバッグ用
    messages.value.push({ user: 'You', text: userInput.value });
    userInput.value = '';
    isLoading.value = true;
};

</script>

<style scoped>
.chat {
    height: 100%;
}

.chat-container {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    background-color: #f2f2f2;
    max-height: calc(100vh - 175px);
    display: flex;
    flex-direction: column-reverse;

}

.chat-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
}

.my-message,
.other-message {
    display: flex;
    margin: 5px 0;
    text-align: left;
}

.my-message {
    justify-content: flex-end;
}

.other-message {
    justify-content: flex-start;
}

.message-bubble {
    display: inline-block;
    max-width: 80%;
    padding: 10px;
    margin: 2px 6px;
    border-radius: 15px;
    background-color: #ffffff;
    color: black;
    white-space: normal;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

.my-message .message-bubble {
    background-color: #fcd093;
    color: black;
}

.guide-button {
    position: fixed;
    bottom: 150px;
    width: 100%;
    display: flex;
    justify-content: center;
    z-index: 100;
}

.input-form {
    position: fixed;
    bottom: 34px;
    width: 100%;
    z-index: 1;
}

.loading .dot-1,
.loading .dot-2,
.loading .dot-3 {
    opacity: 0;
    animation: loading-dots 1.3s infinite;
}

.loading .dot-1 {
    animation-delay: 0.2s;
}

.loading .dot-2 {
    animation-delay: 0.4s;
}

.loading .dot-3 {
    animation-delay: 0.6s;
}

@keyframes loading-dots {
    0% {
        opacity: 0;
    }

    50% {
        opacity: 1;
    }

    100% {
        opacity: 0;
    }
}
</style>
