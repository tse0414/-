# 可執行網站：包裹追蹤與計費系統（Flask 版本）

## 如何啟動
```bash
pip install -r requirements.txt
python app.py
```
啟動後開啟： http://127.0.0.1:5000

## 重要路徑
- 靜態頁面：/pages/index.html、/pages/customer.html、/pages/parcel_tracking.html、/pages/billing.html
- API：
  - GET /api/customers            取得所有客戶（僅示意）
  - GET /api/customers/<id>       取得單一客戶
  - POST /api/customers           新增或覆寫客戶（JSON body）
  - GET /api/packages             取得所有包裹
  - GET /api/packages/<trk>       取得單一包裹
  - POST /api/packages            新增或覆寫包裹（JSON body）
  - GET /api/tracking/<trk>       取得某包裹的追蹤事件
  - POST /api/tracking/<trk>      新增事件（JSON body）
  - GET /api/billing              依 customer/period 查詢帳單與示意明細

## 說明
- 目前資料儲存在 `data/*.json`。
- 前端頁面已掛載 `static/main.js`，提供簡易範例的 API 讀取（例如 `billing.html` 的月結報表）。
- 你可以在不改 HTML 的情況下逐步擴增 API，或把頁面搬到模板引擎。
