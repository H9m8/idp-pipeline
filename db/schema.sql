-- enable extensions
create extension if not exists "pgcrypto";
create extension if not exists vector;

-- vendors
create table if not exists vendors (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  tax_id      text,
  created_at  timestamptz not null default now()
);

-- documents
create table if not exists documents (
  id            uuid primary key default gen_random_uuid(),
  vendor_id     uuid references vendors(id),
  status        text not null default 'received',
  file_name     text,
  mime_type     text,
  file_size     integer,
  doc_type      text,
  raw_text      text,
  currency      text,
  invoice_date  date,
  subtotal      numeric(14,2),
  tax           numeric(14,2),
  total         numeric(14,2),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- line_items
create table if not exists line_items (
  id           uuid primary key default gen_random_uuid(),
  document_id  uuid not null references documents(id) on delete cascade,
  description  text,
  quantity     numeric(14,2),
  unit_price   numeric(14,2),
  amount       numeric(14,2)
);

-- extraction_runs
create table if not exists extraction_runs (
  id            uuid primary key default gen_random_uuid(),
  document_id   uuid not null references documents(id) on delete cascade,
  model         text,
  prompt_tokens   integer,
  output_tokens   integer,
  output        jsonb,
  created_at    timestamptz not null default now()
);

-- anomalies
create table if not exists anomalies (
  id           uuid primary key default gen_random_uuid(),
  document_id  uuid not null references documents(id) on delete cascade,
  kind         text not null,
  detail       text,
  severity     text default 'warning',
  created_at   timestamptz not null default now()
);

-- indexes
cat > db/schema.sql << 'EOF'
-- enable extensions
create extension if not exists "pgcrypto";
create extension if not exists vector;

-- vendors
create table if not exists vendors (
  id          uuid primary key default gen_random_uuid(),
  name        text not null,
  tax_id      text,
  created_at  timestamptz not null default now()
);

-- documents
create table if not exists documents (
  id            uuid primary key default gen_random_uuid(),
  vendor_id     uuid references vendors(id),
  status        text not null default 'received',
  file_name     text,
  mime_type     text,
  file_size     integer,
  doc_type      text,
  raw_text      text,
  currency      text,
  invoice_date  date,
  subtotal      numeric(14,2),
  tax           numeric(14,2),
  total         numeric(14,2),
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now()
);

-- line_items
create table if not exists line_items (
  id           uuid primary key default gen_random_uuid(),
  document_id  uuid not null references documents(id) on delete cascade,
  description  text,
  quantity     numeric(14,2),
  unit_price   numeric(14,2),
  amount       numeric(14,2)
);

-- extraction_runs
create table if not exists extraction_runs (
  id            uuid primary key default gen_random_uuid(),
  document_id   uuid not null references documents(id) on delete cascade,
  model         text,
  prompt_tokens   integer,
  output_tokens   integer,
  output        jsonb,
  created_at    timestamptz not null default now()
);

-- anomalies
create table if not exists anomalies (
  id           uuid primary key default gen_random_uuid(),
  document_id  uuid not null references documents(id) on delete cascade,
  kind         text not null,
  detail       text,
  severity     text default 'warning',
  created_at   timestamptz not null default now()
);

-- indexes
create index if not exists idx_documents_status on documents(status);
create index if not exists idx_documents_vendor on documents(vendor_id);
create index if not exists idx_line_items_doc   on line_items(document_id);
