# Mage orchestration — hướng dẫn lắp trong Edit pipeline (tự động theo dependencies)

Giữ nguyên các block của Tutorial 02–03, **đổi đường downstream** cho `commit_watermark` để chỉ chạy sau bước kiểm thử:

```mermaid
flowchart TD
  A[get_extraction_window] --> F[filter_incremental]
  B[load_source_files] --> F
  F --> N[standardize_and_validate]
  N --> T[load_stage — Transaction Stage]
  P[load_products_full] --> P2[export_products_full — Product Stage]
  C[load_customers_full] --> C2[export_customers_full — Customer Stage]
  C2 --> S[run_customer_snapshot_t04 — dbt snapshot]
  T --> D[DBT Model block — run +fact_sales_enriched]
  P2 --> D
  S --> D
  D --> Q[test_integrated_dds_t04 — dbt test]
  Q --> W[commit_watermark]
  A --> W
```

Khi chọn DBT Model block: Project `dbt/dbt_project`, target `dev`, **All models**, command `run`, model selection `--select +fact_sales_enriched`.

Cả ba nhánh Stage phải kết thúc trước DBT Model block. Các block chỉ dùng dependency để điều phối; dbt tự đọc dữ liệu trực tiếp từ PostgreSQL qua `source()` / `ref()`.

**Quan trọng:** Từng lần chạy cần cùng bộ `product_file`, `customer_file`, `cet_override` để giữ trạng thái tương ứng của batch.

## Thứ tự mô phỏng bằng terminal khi debug (nếu chưa nối Mage)

Sau khi ba bảng Stage đã được nạp đúng phiên bản:

```bash
docker compose exec mage bash
cd /home/src/lab_project/dbt/dbt_project
dbt snapshot --select customers_snapshot
dbt run --select +fact_sales_enriched
dbt test --select +fact_sales_enriched
```

Trên Mage, **không dùng CLI này thay cho pipeline** khi cần commit watermark; chỉ dùng để kiểm tra riêng từng bước.
