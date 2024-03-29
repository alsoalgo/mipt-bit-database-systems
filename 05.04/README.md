# Домашнее задание №2 к 05.04. 

## Описание скриптов.
### run.sh
Скрипт для запуска контейнера с MongoDB. Заполняет базу данных данными из файла `datasets/Mall_Customers.csv`.

### clean.sh
Скрипт для удаления всех созданных контейнеров, виртуальных окружений и т.д.

---

## Инструкция к запуску (делать внутри директории `05.04`).
1. `chmod +x run.sh` - сделать файл запуска исполняемым. 
2. `./run.sh` - запустить скрипт.
3. `chmod +x clean.sh` - сделать файл запуска исполняемым. 
4. `./clean.sh` - удалить все созданные контейнеры, виртуальные окружения и т.д.  

Изначально думал, что с могу через питон позапускать js файлы внутри контейнера, но оказалось, что это вырезали с PyMongo 4. 

---

## Описание CRUD запросов (queries/*).
### Create.
<details>
<summary>Вставка одной записи</summary>

```javascript
db.mall.insertOne({
    "CustomerID": 201,
    "Genre": "Female",
    "Age": 25,
    "Annual Income (k$)": 60,
    "Spending Score (1-100)": 50
})
```
</details>
<details>
<summary>Вставка нескольких записей</summary>

```js
db.mall.insertMany([
    {        
        "CustomerID": 202,        
        "Genre": "Male",        
        "Age": 30,        
        "Annual Income (k$)": 80,        
        "Spending Score (1-100)": 70    
    },    
    {        
        "CustomerID": 203,      
        "Genre": "Female",        
        "Age": 35,        
        "Annual Income (k$)": 75,        
        "Spending Score (1-100)": 80    
    },    {        
        "CustomerID": 204,        
        "Genre": "Male",        
        "Age": 40,        
        "Annual Income (k$)": 90,        
        "Spending Score (1-100)": 60    
    }
])
```
</details>
<details>
<summary>Создание коллекции и вставка записи</summary>

```js
db.createCollection("customers")

db.customers.insertOne({
    "CustomerID": 1,
    "Name": "John Smith",
    "Email": "john.smith@example.com",
    "Phone": "123-456-7890"
})
```
</details>

### Read.
<details>
<summary>Find с Age</summary>

```javascript
db.mall.find({ Age: { $gte: "25" } })
```
</details>
<details>
<summary>Find с Age & Genre</summary>

```javascript
db.mall.find({ Genre: "Male", Age: { $lte: "30" } })
```
</details>
<details>
<summary>Find с Annual Income</summary>

```javascript
db.mall.find({ "Annual Income (k$)": { $lte: "50" } })
```
</details>
<details>
<summary>Find с CustomerID</summary>

```javascript
db.mall.findOne({ CustomerID: "0010" })
```
</details>
<details>
<summary>Find с Spending Score</summary>

```javascript
db.mall.find({ "Spending Score (1-100)": { $gt: "75" } })
```
</details>

### Update.
<details>
<summary>Update с Age</summary>

```javascript
db.mall.updateOne({ CustomerID: "0010" }, { $set: { Age: "35" } })
```
</details>
<details>
<summary>Update типа Annual Income (string -> int)</summary>

```javascript
db.mall.updateMany({}, [{ $set: { "Annual Income (k$)": { $toInt: "$Annual Income (k$)" } } }])
```
</details>
<details>
<summary>Update одной записи</summary>

```javascript
db.mall.updateMany({ Age: { $lt: "30" } }, { $set: { "Annual Income (k$)": 40 } })

```
</details>

### Delete.
<details>
<summary>Delete одной записи</summary>

```javascript
db.mall.deleteOne({ "CustomerID": "0035" })
```
</details>
<details>
<summary>Delete нескольких записей</summary>

```javascript
db.mall.deleteMany({ "Spending Score (1-100)": { $gte: "80" } })
```
</details>

---
   
## Про индекс.
<details>
<summary>Explain для запроса (до создания индекса)</summary>

Запрос:
```js
db.mall.find({"Annual Income (k$)": {"$gt": "50"}}).explain("executionStats")
```  

Вывод:
```javascript
{
  explainVersion: '1',
  ...,
  executionStats: {
    executionSuccess: true,
    nReturned: 0,
    executionTimeMillis: 3,
    totalKeysExamined: 0,
    totalDocsExamined: 200,
    executionStages: {
      stage: 'COLLSCAN',
      filter: {
        'Annual Income (k$)': {
          '$gt': 50
        }
      },
      nReturned: 0,
      executionTimeMillisEstimate: 0,
      works: 202,
      advanced: 0,
      needTime: 201,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      direction: 'forward',
      docsExamined: 200
    }
  },
  ...,
  ok: 1
}
```
</details>

Созданный индекс:
```js
db.mall.createIndex({'Annual Income (k$)': 1})
```

<details>
<summary>Explain для запроса (после создания индекса)</summary>

Запрос:
```js
db.mall.find({"Annual Income (k$)": {"$gt": "50"}}).explain()
```  

Вывод:
```js
{
  explainVersion: '1',
  ...,
  executionStats: {
    executionSuccess: true,
    nReturned: 0,
    executionTimeMillis: 0,
    totalKeysExamined: 0,
    totalDocsExamined: 0,
    executionStages: {
      stage: 'FETCH',
      nReturned: 0,
      executionTimeMillisEstimate: 0,
      works: 1,
      advanced: 0,
      needTime: 0,
      needYield: 0,
      saveState: 0,
      restoreState: 0,
      isEOF: 1,
      docsExamined: 0,
      alreadyHasObj: 0,
      inputStage: {
        stage: 'IXSCAN',
        nReturned: 0,
        executionTimeMillisEstimate: 0,
        works: 1,
        advanced: 0,
        needTime: 0,
        needYield: 0,
        saveState: 0,
        restoreState: 0,
        isEOF: 1,
        keyPattern: {
          'Annual Income (k$)': 1
        },
        indexName: 'Annual Income (k$)_1',
        isMultiKey: false,
        multiKeyPaths: {
          'Annual Income (k$)': []
        },
        isUnique: false,
        isSparse: false,
        isPartial: false,
        indexVersion: 2,
        direction: 'forward',
        indexBounds: {
          'Annual Income (k$)': [
            '(50, inf.0]'
          ]
        },
        keysExamined: 0,
        seeks: 1,
        dupsTested: 0,
        dupsDropped: 0
      }
    }
  },
  ...,
  ok: 1
}
```  

</details>