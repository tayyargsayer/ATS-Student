## ATS Sistemi: Öğrenci Kılavuzu

Bu repo, Google Gemini'nin gücünden yararlanarak, ATS (Applicant Tracking System) olarak çalışan bir sistemdir. Bu sistem, CV'leri otomatik olarak analiz ederek, iş ilanlarına göre uygunluğunu değerlendirir.

### 1. Repo'yu İndirme

1.  **GitHub'dan Klonlama:**  [https://github.com/tayyargsayer/mext_2](https://github.com/tayyargsayer/mext_2) adresinden repoyu bilgisayarınıza klonlayın.
2.  **Gerekli Kütüphaneler:**  `pip install -r requirements.txt` komutunu kullanarak gerekli kütüphaneleri yükleyin.
3.  **Google API Anahtarını Ayarlama:** Google Cloud Platform hesabınızda bir API anahtarı oluşturun ve `.env` dosyasına aşağıdaki formatta ekleyin:
    ```
    GOOGLE_API_KEY=YOUR_API_KEY
    ```

### 2. Uygulamayı Çalıştırma

1.  **Streamlit'i Başlatma:**  `streamlit run main.py` komutunu çalıştırarak uygulamayı başlatın.
2.  **Kullanıcı Arayüzü:** Uygulama tarayıcınızda açılacaktır. Sol taraftaki yan panelde aşağıdaki seçenekler mevcuttur:
    *   **Departman:** Hedef meslek grubunu seçin.
    *   **Deneyim Süresi:** Adayın minimum deneyim süresini belirtin.
    *   **Döküman Uzantısı:**  CV'yi PDF veya görsel olarak yükleme seçeneği.
    *   **Dosya Yükleme:**  CV'yi yüklemek için "CV Dosyası" veya "CV Fotoğrafı" seçeneğini kullanın.
    *   **Çalıştır Butonu:** Yüklediğiniz CV'yi analiz etmek için "Çalıştır" butonuna tıklayın.

### 3. Uygulamanın Çalışması

1.  **Analiz:**  Uygulama, yüklediğiniz CV'yi analiz ederek, seçilen departmana ve deneyim süresine göre uygunluğunu belirler.
2.  **Yorum:**  Analizin sonucu, ekrana markdown formatında bir rapor olarak gösterilir. Rapor, adayın güçlü ve zayıf yönlerini, uygunluk yüzdesini ve ek yorumları içerir.

### 4. Uygulamayı GitHub'da Paylaşma

1.  **Değişiklikleri Kaydetme:**  Uygulamayı kişiselleştirdikten sonra, yaptığınız değişiklikleri git'e kaydedin.
2.  **Yeni Bir Repo Oluşturma:**  Kendi GitHub hesabınızda yeni bir repo oluşturun.
3.  **Yerel Repo'yu Bağlama:**  Yeni oluşturulan repo'ya yerel repo'nuzu bağlayın.
4.  **Değişiklikleri Gönderme:**  Yerel repo'daki değişiklikleri GitHub repo'nuza gönderin.

### Önemli Notlar

*   Bu uygulama, Google Gemini'nin Türkçe dil desteği kullanarak çalışır. Ancak, modelin dil anlama yeteneklerinde sınırlamalar olabilir.
*   Uygulama, CV'lerin analizinde temel bir yaklaşım kullanır. Daha gelişmiş bir ATS sistemi için, daha kapsamlı bir model eğitimi ve daha detaylı analiz algoritmaları gerekebilir.
*   Google Gemini'nin kullanım koşullarını ve gizlilik politikasını dikkate alın.

Umarım bu repo, ATS sistemleri hakkında bilgi edinmenize ve kendi uygulamalarınızı geliştirmenize yardımcı olur. Herhangi bir sorunuz veya öneriniz için lütfen bana ulaşmaktan çekinmeyin.
