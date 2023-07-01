#!/usr/bin/env python
# coding: utf-8

# ## Analyser les données d'une société qui vend des smartphones(et autres gadgets) et répondre à certaines questions business 

# #### Quel est le mois durant lequel nous avons réalisé le meilleur chiffre d'affaire ?

# #### Dans quelle ville nous avons enregistré un maximum de commandes ?

# #### À quelle moment doit on faire une compagne publicitaire pour avoir plus de ventes ?

# #### Quel produit se vend le plus ?

# # Découverte des Données

# In[6]:


# importer des packages 
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# In[7]:


# collecter les noms des fichiers (datasets)
files=[file for file in os.listdir(r'C:\Users\GSarah\DATA\Donnée_entrepriseOPA')]
for file in files:
    for file in files:
        print(file)
    


# In[8]:


# regrouper dans un seul fichier 
path=r'C:\Users\GSarah\DATA\Donnée_entrepriseOPA'

# créer une base de données vide
all_data=pd.DataFrame()

for file in files:
    current_data=pd.read_csv(path+'/'+file)
    all_data=pd.concat([all_data,current_data])
    print(all_data)


# In[9]:


all_data.to_csv(path+'/all_data.csv',index=False)


# In[10]:


# explorer cette base de données 
all_data.dtypes


# In[11]:


all_data.head()


# In[12]:


# voir les valeurs manquantes 
all_data.isnull().sum()


# In[13]:


# supprimer les valeurs manquantes
all_data=all_data.dropna(how='all')
all_data.shape


# ## Quel est le mois durant lequel nous avons réalisé le meilleur chiffre d'affaire ?

# In[14]:


all_data


# In[15]:


def month(x):
    
   return x.split('/')[0]



# In[16]:


all_data['Month']=all_data['Order Date'].apply(month)
all_data


# In[17]:


all_data['Month'].unique()


# In[18]:


all_data=all_data[all_data['Month']!='Order Date']
all_data['Month'].unique()


# In[19]:


all_data.dtypes


# In[20]:


all_data['Month']=all_data['Month'].astype(int)
all_data.dtypes


# In[21]:


all_data['Price Each']=all_data['Price Each'].astype(float)
all_data['Quantity Ordered']=all_data['Quantity Ordered'].astype(int)
all_data.dtypes


# In[22]:


all_data['Sales']=all_data['Quantity Ordered']*all_data['Price Each']
all_data


# In[23]:


all_data.groupby('Month')['Sales'].sum()


# In[24]:


months=range(1,13)
plt.bar(months, all_data.groupby('Month')['Sales'].sum())
plt.xticks(months)
plt.ylabel('Ventes en USD')
plt.xlabel('Mois')
plt.show()


# ##### Le mois avec le meilleur chiffre d'affaire c'est Décembre 

#  ## Dans quelle ville nous avons enregistré un maximum de commandes ?¶

# In[25]:


all_data


# In[26]:


def city(x):
     return x.split(',')[1]


# In[27]:


all_data['city']=all_data['Purchase Address'].apply(city)
all_data


# In[28]:


all_data.groupby('city')['city'].count()


# In[81]:


plt.bar(all_data.groupby('city')['city'].count().index, all_data.groupby('city')['city'].count().values)
plt.xticks(rotation='vertical')
plt.ylabel('Commandes reçues')
plt.xlabel('Nom de Ville')
plt.show()



# ## La ville qui a le maximum de commandes enregistré est San Francisco

# # À quelle moment doit on faire une compagne publicitaire pour avoir davantage de ventes ?

# In[30]:


all_data


# In[31]:


all_data['Hour']=pd.to_datetime(all_data['Order Date']).dt.hour


# In[32]:


all_data


# In[35]:


keys=[]
hours=[]
for key, hour in all_data.groupby('Hour'):
    keys.append(key)
    hours.append(len(hour))
    hours
    


# In[36]:


plt.grid()
plt.plot(keys,hours)
plt.xlabel('heure de la journée')
plt.ylabel('nombre des commandes')


# #### Meilleurs créneaux pour lancer des campagnes publicitaires 12h et 20h
# 

# # Quel produit se vend le plus ?

# In[38]:


all_data.groupby('Product')['Quantity Ordered'].sum().plot(kind='bar')


# In[39]:


all_data.groupby('Product')['Price Each'].mean()


# In[51]:


products=all_data.groupby('Product')['Quantity Ordered'].sum().index
quantity=all_data.groupby('Product')['Quantity Ordered'].sum()
prices=all_data.groupby('Product')['Price Each'].mean()


# In[58]:


plt.figure(figsize=(40,24))
fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products,quantity,color='g')
ax2.plot(products,prices, 'b-')
ax1.set_xticklabels(products,rotation='vertical', size=8)

plt.ylabel('Prix')


# ## Bleu = prix moyen      ##Vert =la quantité vendu

# #### Les produits pas cher sont le mieux vendus 

# ## Quelles sont les combinaisons de produits qui se vendent le plus ?

# In[66]:


df=all_data[all_data['Order ID'].duplicated(keep=False)]


# In[67]:


df['Grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))


# In[72]:


df


# In[78]:


df2=df.drop_duplicates(subset=['Order ID'])
df


# In[79]:


df2['Grouped'].value_counts()[0:5].plot.pie()


# In[ ]:




