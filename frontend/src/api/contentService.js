import apiClient from './Axios.js';

// ----------------------------------------------------
// POPÜLER ve PUANLI İÇERİK ÇEKME FONKSİYONLARI
// ----------------------------------------------------
const BASE_URL = 'http://127.0.0.1:8000/api/';
export const fetchPopularTitles = async () => {
    try {
        const response = await apiClient.get('/titles/', {
            params: {
                ordering: 'popular'
            }
        });
        return response.data;
    } catch (error) {
        console.error("Popüler içerikler çekilemedi:", error);
        throw error;
    }
};

export const fetchTopRatedTitles = async () => {
    try {
        const response = await apiClient.get('/titles/', {
            params: {
                ordering: 'top_rated'
            }
        });
        return response.data;
    } catch (error) {
        console.error("En yüksek puanlı içerikler çekilemedi:", error);
        throw error;
    }

};

// İstediğiniz diğer içerik çekme fonksiyonlarını buraya ekleyebilirsiniz.