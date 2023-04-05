db.mall.updateMany({}, [{ $set: { "Annual Income (k$)": { $toInt: "$Annual Income (k$)" } } }])
