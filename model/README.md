---
tags:
- summarization
- news
language: tr
datasets:
- mlsum
widget:
- text: "Ankara'da oto hırsızlık çetesine yönelikdüzenlenen ‘Balta’ operasyonunda, çete lideri‘balta’ lakaplı şahıs ile 7 kişi gözaltına alındı.Diğer bir operasyonda ise 3 şüpheli çaldıklarıaraçları parçalarken yapılan baskında suçüstüyakalandı. Ankara Emniyet Müdürlüğü’ne bağlıAsayiş Şube Müdürlüğü Oto Hırsızlık Büro Amirliğiekipleri, Ankara ilinde meydana gelen, otohırsızlık olaylarına karşı Ankara CumhuriyetBaşsavcılığı’nın izniyle yürüttükleri 3 aylıkçalışma sonucunda operasyon düğmesine bastı.Yapılan teknik ve fiziki takip sonucunda, ‘Balta’çetesine ulaşıldı. Çeteyi izleyen ekipler, Ankara,Konya ve Antalya’da eş zamanlı operasyondüzenleyerek çete lideri ‘Balta’ lakaplı Necati D.ve çete üyesi 7 kişiyi yakaladı. Takip edildiğinianlayınca ortadan kayboldu Çete lideri ‘Balta’nın,polis ekipleri tarafından izlendiğini anladığı veaylarca ortada görünmediğini tespit eden HırsızlıkBüro ekipleri, ‘Balta’nın kendi suç ortaklarını dadolandırmaya çalıştığını saptadı. Adliyeye sevkedilen şüphelilerden haklarında çok sayıda otohırsızlık kaydı bulunan çete lideri Necati D.,Ferhat K., Atakan A. ve Tayfun G., çıkarıldıklarınöbetçi sulh hakimliğince tutuklanarak cezaevinegönderildi. Diğer 3 şüpheli ise adli kontrolşartıyla serbest bırakıldı. Çaldıkları araçlarıparçalarken polis bastı Diğer bir olay iseAltındağ ilçesinde meydana geldi. Hırsızlık Büroekipleri inceledikleri 2 oto hırsızlık olayınınsonucunda 3 şüpheliyi takibe aldı. Şüphelilerinçaldıkları 2 aracı İvedik Hurdacılar Sitesi’ndekidepolarında parçalayacaklarını belirleyen ekiplerharekete geçti. Depoya baskın yapan polisekipleri, 3 şüpheliyi suçüstü yakaladı.Emniyetteki işlemlerinin ardından adliyeye sevkedilen hırsızlık zanlıları, çıkarıldıkları nöbetçimahkeme tarafından adli kontrol şartıyla serbestbırakıldı."
---


# Turkish BERT2BERT (shared) fine-tuned on MLSUM TR for summarization


## Model
[dbmdz/bert-base-turkish-cased](https://huggingface.co/dbmdz/bert-base-turkish-cased) (BERT Checkpoint)

## Dataset
**MLSUM** is the first large-scale MultiLingual SUMmarization dataset. Obtained from online newspapers, it contains 1.5M+ article/summary pairs in five different languages -- namely, French, German, Spanish, Russian, **Turkish**. Together with English newspapers from the popular CNN/Daily mail dataset, the collected data form a large scale multilingual dataset which can enable new research directions for the text summarization community. We report cross-lingual comparative analyses based on state-of-the-art systems. These highlight existing biases which motivate the use of a multi-lingual dataset.

[MLSUM tu/tr](https://huggingface.co/datasets/viewer/?dataset=mlsum)

## Results

|Set|Metric| Value|
|----|------|------|
| Test  |Rouge2 - mid -precision | **32.41**|
| Test | Rouge2 - mid - recall | **28.65**|
| Test | Rouge2 - mid - fmeasure | **29.48**|

## Usage

 ```python
 import torch
 from transformers import BertTokenizerFast, EncoderDecoderModel
 device = 'cuda' if torch.cuda.is_available() else 'cpu'
 ckpt = 'mrm8488/bert2bert_shared-turkish-summarization'
 tokenizer = BertTokenizerFast.from_pretrained(ckpt)
model = EncoderDecoderModel.from_pretrained(ckpt).to(device)

def generate_summary(text):

    inputs = tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    input_ids = inputs.input_ids.to(device)
    attention_mask = inputs.attention_mask.to(device)
    output = model.generate(input_ids, attention_mask=attention_mask)
    return tokenizer.decode(output[0], skip_special_tokens=True)
    
text = "Your text here..."
generate_summary(text)
```

> Created by [Manuel Romero/@mrm8488](https://twitter.com/mrm8488) with the support of [Narrativa](https://www.narrativa.com/)

> Made with <span style="color: #e25555;">&hearts;</span> in Spain

