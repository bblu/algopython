//MongoDB 权威指南
//4.1 $lt $lte $gt $gte $ne
db.stuff.find({"age": {"$gt": 18, "$lt": 21}})
db.stuff.find({"age": {"$in": [18,19,20,21]}})
db.stuff.find({"$or": [{"age":18},{"age":19}]})

//4.2.3 $not $mod (id_num mod 5 == 1)
db.stuff.find({"id_num":{"$mod": [5, 1]}})
db.stuff.find({"id_num":{"$not": {"$mod": [5, 1]}}})

//4.3.1 z 存在且为null(很遗憾没有$eq)
db.coord.find({"z": {"$in": [null], "$exists": true}})

//4.3.3 array 匹配任何一个数组成员都可以成功匹配
db.food.insert({"fruit":["apple", "banana", "peach"]})
db.food.find({"fruit": "apple"})
//多重匹配 $all
db.food.find({fruit": {"$all": ["apple", "banana"]}})
//索引匹配 key.index 从零开始
db.food.find({"fruit.1": "banana"})
// array $size
db.food.find({"fruit": {"$size": 3}})
// $silce : -10

// 4.3.4 内嵌文档  . $elementMatch
{
  "name":{
    "first": "Joe",
    "last": "Schmoe"
  },
  "age": 35
}
//第一种查询必须全部匹配子文档，并且顺序相关
db.stuff.find({"name": {"first": "Joe","last": "Schemoe"}})
db.stuff.finde({"name.first": "Joe"})
