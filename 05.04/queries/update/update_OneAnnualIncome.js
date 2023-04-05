db.mall.updateMany({ Age: { $lt: "30" } }, { $set: { "Annual Income (k$)": 40 } })
