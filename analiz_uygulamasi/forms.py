# analiz_uygulamasi/forms.py

from django import forms

class SenaryoForm(forms.Form):
    senaryo_metni = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 10,
            'cols': 80,
            'placeholder': 'Analiz etmek istediğiniz senaryo metnini buraya girin...',
        }),
        required=False, # Ya metin ya da PDF olmalı
        label="Senaryo Metni"
    )
    pdf_dosyasi = forms.FileField(
        required=False, # Ya metin ya da PDF olmalı
        label="PDF Dosyası Yükle",
        widget=forms.FileInput(attrs={
            'hidden': True, # Orijinal input'u gizlemek için eklendi
            'accept': '.pdf' # Sadece PDF dosyalarını kabul etmesi için bu satırı da ekleyin
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        senaryo_metni = cleaned_data.get('senaryo_metni')
        pdf_dosyasi = cleaned_data.get('pdf_dosyasi')

        if not senaryo_metni and not pdf_dosyasi:
            raise forms.ValidationError(
                "Lütfen senaryo metni girin veya bir PDF dosyası yükleyin.",
                code='no_input'
            )
        if senaryo_metni and pdf_dosyasi:
            raise forms.ValidationError(
                "Lütfen sadece bir giriş yöntemi seçin: ya metin ya da PDF.",
                code='both_inputs'
            )
        return cleaned_data
