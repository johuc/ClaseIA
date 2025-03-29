import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class SpamDetector:
    def __init__(self, file_path):
        """Inicializa la clase SpamDetector con el archivo CSV."""
        self.file_path = file_path
        self.data = pd.read_csv(file_path)  # Cargar el archivo CSV
        self.stopwords = set(['el', 'y', 'es', 'en', 'para', 'de', 'a', 'por', 'con', 'esto'])  # Lista ejemplo de stopwords
        self.spam_keywords = ['whatsapp', 'dinero', 'gratis', 'oportunidad', 'iphone']  # Palabras clave de spam

    def preprocess_text(self):
        """Realiza el preprocesamiento del texto: eliminación de duplicados, minúsculas, caracteres especiales, etc."""
        # Eliminar correos duplicados
        self.data = self.data.drop_duplicates(subset='contenido')
        
        # Convertir todo el texto a minúsculas
        self.data['contenido'] = self.data['contenido'].str.lower()  # Minusculas
        
        # Eliminar caracteres especiales
        self.data['contenido'] = self.data['contenido'].str.replace(r'[^a-zA-Z0-9\s]', '')  # Eliminar caracteres especiales
        
        # Dividir el texto en palabras (tokenización)
        self.data['contenido'] = self.data['contenido'].str.split()  # Dividir en palabras
        
        # Eliminar las stopwords
        self.data['contenido'] = self.data['contenido'].apply(lambda x: [word for word in x if word not in self.stopwords])  # Eliminar stopwords

    def vectorize_text(self):
        """Vectoriza el texto utilizando TfidfVectorizer."""
        self.data['contenido'] = self.data['contenido'].str.join(' ')  # Juntar las palabras nuevamente en una cadena
        vectorizer = TfidfVectorizer(stop_words='english')  # Crear vectorizador
        features = vectorizer.fit_transform(self.data['contenido'])  # Vectorizar el texto
        return features, vectorizer.get_feature_names_out()

    def apply_rules(self):
        """Aplica las reglas de clasificación para identificar los correos spam."""
        for index, row in self.data.iterrows():
            # Regla 1: Si el correo electrónico contiene la palabra clave "Whatsapp", entonces es Spam.
            if 'whatsapp' in row['contenido']:
                self.data.at[index, 'etiqueta'] = 'spam'
            # Regla 2: Si el correo electrónico contiene un enlace a un sitio web conocido por distribuir malware, entonces es spam.
            elif 'spamlink.com' in row['enlaces'] or 'spamiphone.com' in row['enlaces']:
                self.data.at[index, 'etiqueta'] = 'spam'
            # Regla 3: Si el correo electrónico tiene un remitente desconocido, entonces es Spam.
            elif row['remitente'] not in ['SPAM1@mail.com', 'amigo@mail.com', 'SPAM2@mail.com', 'boss@mail.com']:  # Remitentes conocidos
                self.data.at[index, 'etiqueta'] = 'spam'
            # Regla 4: Si el correo electrónico tiene un asunto que es demasiado bueno para ser verdad, entonces es Spam.
            elif 'dinero' in row['asunto'] or 'iphone' in row['asunto']:
                self.data.at[index, 'etiqueta'] = 'spam'
            # Regla 5: Si el correo electrónico está mal escrito o tiene errores gramaticales, entonces es Spam.
            # (Aquí, por simplicidad, consideramos un ejemplo básico de errores gramaticales)
            elif 'haz sido' in row['contenido'] or 'gratis' in row['contenido']:
                self.data.at[index, 'etiqueta'] = 'spam'

    def calculate_spam_probability(self):
        """Calcula la probabilidad previa de spam P(Spam)."""
        total_correos = len(self.data)  # Total de correos en el dataset
        correos_spam = len(self.data[self.data['etiqueta'] == 'spam'])  # Número de correos spam
        P_spam = correos_spam / total_correos  # Probabilidad previa de spam
        return P_spam

    def calculate_caracteristicas(self):
        """Calcula las características de cada correo y devuelve un DataFrame con las características y el correo asociado."""
        features, feature_names = self.vectorize_text()
        features_array = features.toarray()
        df_features = pd.DataFrame(features_array, columns=feature_names)
        df_features['correo'] = self.data['contenido']
        return df_features
    
    def get_processed_data(self):
        """Devuelve el DataFrame procesado (sin duplicados y con texto preprocesado)."""
        return self.data

# Uso de la clase SpamDetector

# Crear una instancia de la clase SpamDetector con el archivo CSV
spam_detector = SpamDetector('Correo.csv')  # Asegúrate de que el archivo spam.csv esté en el mismo directorio o proporciona la ruta completa

# Preprocesar el texto
spam_detector.preprocess_text()

# Aplicar las reglas para clasificar los correos
spam_detector.apply_rules()

# Calcular la probabilidad previa de spam
P_spam = spam_detector.calculate_spam_probability()

# Mostrar la probabilidad de spam
print(f'La probabilidad previa de spam (P(Spam)) es: {P_spam:.4f}')

# Vectorizar el texto
features, feature_names = spam_detector.vectorize_text()

# Mostrar las características generadas (palabras/bigrams)
features_array = features.toarray()
df_features = pd.DataFrame(features_array, columns=feature_names)

# Mostrar las primeras filas de las características
print(df_features.head())

# Mostrar el DataFrame procesado con la etiqueta 'spam' o 'not_spam'
print(spam_detector.get_processed_data())
# Verificación de correos específicos (fuera de la clase)
# Ejemplo de cómo acceder a un correo específico
remitente = 'boss@mail.com', 'amigo@mail.com'
contenido = spam_detector.get_processed_data()
# Filtrar para comprobar si alguno de los correos en 'contenido' corresponde al remitente deseado
filtered_data = contenido[contenido['remitente'] == remitente]

print('correo spam:', filtered_data[filtered_data['etiqueta'] == 'spam'])
print('correo no spam:', filtered_data[filtered_data['etiqueta'] == 'not_spam'])