create table if not exists website_quote_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  ad_soyad text not null,
  firma text,
  iletisim text not null,
  kategori text not null,
  adet integer default 1,
  notlar text,
  created_at timestamptz default now()
);

alter table website_quote_requests enable row level security;

create policy "Users can view own quote requests"
  on website_quote_requests for select
  using (auth.uid() = user_id);

create policy "Users can insert own quote requests"
  on website_quote_requests for insert
  with check (auth.uid() = user_id);
