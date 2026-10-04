-- Docs: https://docs.mage.ai/guides/sql-blocks
UPDATE control.etl_watermark
SET last_successful_extraction_time =
    '{{ cet_override }}'::TIMESTAMP
WHERE pipeline_name = 'transaction_ingestion';