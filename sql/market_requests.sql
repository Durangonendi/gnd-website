create table if not exists market_requests (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete cascade not null,
  islem_turu text not null check (islem_turu in ('satis', 'alim')),
  ad_soyad text not null,
  telefon text not null,
  baslik text not null,
  durum_bilgisi text,
  fiyat text,
  aciklama text,
  onay_durumu text not null default 'beklemede' check (onay_durumu in ('beklemede', 'yayinda', 'reddedildi')),
  created_at timestamptz default now()
);

alter table market_requests enable row level security;

create policy "Users can view own requests"
  on market_requests for select
  using (auth.uid() = user_id);

create policy "Anyone can view approved requests"
  on market_requests for select
  using (onay_durumu = 'yayinda');

create policy "Users can insert own requests"
  on market_requests for insert
  with check (auth.uid() = user_id);

create policy "Users can update own requests"
  on market_requests for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

create policy "Users can delete own requests"
  on market_requests for delete
  using (auth.uid() = user_id);
