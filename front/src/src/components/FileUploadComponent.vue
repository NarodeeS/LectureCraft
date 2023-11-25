<template>
    <div class="container" style="margin-top: 50px;">
        <div id="drop-zone" @dragover.prevent @drop.prevent="handleDrop">
            Перетащите ваш файл сюда или
            <br />
            <label for="fileElem" class="file-input-label">кликните для выбора файла</label>
            <input type="file" id="fileElem" accept="video/*,audio/*" @change="handleChange" hidden />
            <br />
            <input type="text" placeholder="Введите ссылку на прямую трансляцию " />

            <div class="centered-content">
                <video ref="videoPreview" controls style="max-width: 100%; height: auto; display: none;"></video>
                <audio ref="audioPreview" controls style="max-width: 100%; display: none;"></audio>
            </div>
            <div class="progress custom-progres" v-if="uploadPercentage > 0" role="progressbar"
                aria-label="Example with label" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"
                id="custom-progres">
                <div id="bar-color" class="progress-bar " :style="{ width: uploadPercentage + '%' }">
                    {{ uploadPercentage }}
                </div>
            </div>

            <button v-if="showSubmitButton" @click="submitFiles" class="button">
                Загрузить файл
            </button>

            <div>
                <button @click="getFileList" class="button">
                    Обновить для получения резльтатов
                </button>
                <p>Результат появляется не сразу :(</p>
            </div>
            <div class="recognizer">
                <FileDownloadComponent v-for="filename in responseList" :key="filename" :fileName="filename" />
            </div>

        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue"
import ResponseData from "@/types/response"
import FileDownloadComponent from "@/components/FileDownloadComponent"

import axios, { AxiosResponse, AxiosError } from 'axios';
const videoPreview = ref<HTMLVideoElement | null>(null);
const audioPreview = ref<HTMLAudioElement | null>(null);
const files = ref<File[]>([]);
const showSubmitButton = ref(false);

const succsess = ref<boolean>(false)
const isloaded = ref<boolean>(false)
const uploadPercentage = ref<number>(0)

const isRecognizing = ref<boolean>(false)

const responseList = ref<string[]>([]);


const handleDrop = (e: DragEvent) => {
    const dtFiles = e.dataTransfer?.files;
    if (dtFiles) {
        processFiles(dtFiles);
        showSubmitButton.value = true;
    }
};

const handleChange = (e: Event) => {
    const input = e.target as HTMLInputElement;

    if (input.files) {
        processFiles(input.files);
        showSubmitButton.value = true;
    }
};

const processFiles = (fileList: FileList) => {
    isloaded.value = true;
    succsess.value = false;
    uploadPercentage.value = 0;
    showSubmitButton.value = false;
    isRecognizing.value = false;
    responseList.value = [];
    files.value = [];

    for (let i = 0; i < fileList.length; i++) {
        const file = fileList[i];
        if (file.type.startsWith('video/')) {
            if (videoPreview.value) {
                videoPreview.value.src = URL.createObjectURL(file);
                videoPreview.value.style.display = 'block';
            }
        } else if (file.type.startsWith('audio/')) {
            if (audioPreview.value) {
                audioPreview.value.src = URL.createObjectURL(file);
                audioPreview.value.style.display = 'block';
            }
        }
        files.value.push(file);
    }
};

const submitFiles = async () => {
    const formData = new FormData();
    files.value.forEach(file => formData.append('lecture', file));

    try {
        showSubmitButton.value = false
            ;
        await axios.post('/lecture', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: function (progressEvent) {

                uploadPercentage.value = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            },
        })
            .then((response: AxiosResponse) => {
                uploadPercentage.value = 0;
                isRecognizing.value = true;
                // showSubmitButton.value = false;
                succsess.value = true;
                isloaded.value = false;
                files.value = [];
            })
            .catch((error: AxiosError) => {
                let errors: string[] = []
                uploadPercentage.value = 0
                if (error.response) {
                    const response: AxiosResponse = error.response

                    if (response.data) {
                        const data: ResponseData = response.data

                        for (let key in data) {
                            errors.push(`${key} ${data[key]}`)
                        }
                    }
                    console.error(response)
                }
            })
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        showSubmitButton.value = true;
    }
};


const getFileList = async () => {
    try {
        await axios.get('/synopsis')
            .then((response: AxiosResponse) => {
                responseList.value = response.data
            })
            .catch((error: AxiosError) => {
                let errors: string[] = []
                uploadPercentage.value = 0
                if (error.response) {
                    const response: AxiosResponse = error.response

                    if (response.data) {
                        const data: ResponseData = response.data

                        for (let key in data) {
                            errors.push(`${key} ${data[key]}`)
                        }
                    }
                    console.error(response)
                }
            })
    } catch (error) {
        console.error('Ошибка загрузки:', error);
    }
};
</script>

<style>
.recognizer {
    margin-top: 20px;
}

#custom-progres {
    height: 40px;
    /* margin: 10px; */
    /* border-radius: 25px; */
    background-color: #4CAF50;

}

#bar-color {
    padding: 5px;
    font-size: 20px;
    font-weight: bold;
    background-color: #11782d;
    color: #121212;
    border-radius: 25px;
}


input[type="text"] {
    margin: 10px;
    width: 45%;
    flex-grow: 1;
    /* Поле ввода займет все доступное пространство */
    padding: 8px;
    border-radius: 4px;
    border: 1px solid #ccc;
}
</style>
