-- GND Machinery — Admin panel + Pazar fotoğraf/kategori/temel bilgiler güncellemesi
-- Supabase Dashboard > SQL Editor > New query içine yapıştırıp "Run" a bas.
-- Bu script'i birden fazla kez çalıştırman güvenlidir (tekrar çalıştırınca hata vermez).

-- 1) Admin yetkisi
drop policy if exists "admin_select_market_requests" on market_requests;
create policy "admin_select_market_requests"
on market_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

drop policy if exists "admin_update_market_requests" on market_requests;
create policy "admin_update_market_requests"
on market_requests for update
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

drop policy if exists "admin_select_quote_requests" on website_quote_requests;
create policy "admin_select_quote_requests"
on website_quote_requests for select
to authenticated
using (auth.jwt() ->> 'email' = 'kuralsz_drn3444@hotmail.com');

-- 2) Pazar ilanlarına kategori ve çoklu fotoğraf desteği
alter table market_requests add column if not exists kategori text;
alter table market_requests add column if not exists foto_urls text[];

-- 3) Fotoğraf yükleme için depolama alanı (bucket)
insert into storage.buckets (id, name, public)
values ('market-photos', 'market-photos', true)
on conflict (id) do nothing;

drop policy if exists "public_read_market_photos" on storage.objects;
create policy "public_read_market_photos"
on storage.objects for select
to public
using (bucket_id = 'market-photos');

drop policy if exists "authenticated_upload_market_photos" on storage.objects;
create policy "authenticated_upload_market_photos"
on storage.objects for insert
to authenticated
with check (bucket_id = 'market-photos');

-- 4) Mevcut yayındaki ilanları kategorilere ayır (yeni filtreleme çalışsın diye)
update market_requests set kategori = 'atasman' where id in (
  '004568c3-a6db-4561-adb0-d9efd2118473', 'ffa8e62f-3e67-4395-9a9f-5786e21777db',
  '7fcafa2f-a104-4aae-84c1-3c7c5de5c2e8', '1ff6dd86-606d-45c6-a90c-0cf29c000c44',
  'c0154096-4ce0-488a-b4c3-b081d5fac286', '80e128d2-76df-4b73-a31f-3a4f2b86ea62',
  'f31cc56d-19e4-4ca2-a96f-e110eae7e1c3', '21f4a483-6a23-4bf3-8092-c4fb59ed8b62',
  '0d4381bc-d5b5-4266-9621-bc8f5ed04cc1', 'e4c468fb-2e5d-44a8-90d2-0c9f93ef1ec5',
  '85b06855-7b24-4b27-a126-4a081d794cdb'
);
update market_requests set kategori = 'makine' where id in (
  'c4a696f2-495a-4f98-b0e5-1f7aac6587e1'
);
update market_requests set kategori = 'parca' where id in (
  'c15b1b82-7e52-45a6-a79a-394b2944cf80', '66c67a00-d41f-4b70-8c2e-8c6a5a9c860d'
);

-- 5) Müşteriler kendi ilanlarını düzenleyebilsin ("İlanlarım" - Hesabım sayfası)
drop policy if exists "owner_update_own_market_requests" on market_requests;
create policy "owner_update_own_market_requests"
on market_requests for update
to authenticated
using (auth.uid() = user_id)
with check (auth.uid() = user_id);

-- 6) Temel bilgiler: motor saati, model yılı, tonaj, yakıt tipi
alter table market_requests add column if not exists motor_saati text;
alter table market_requests add column if not exists model_yili text;
alter table market_requests add column if not exists tonaj text;
alter table market_requests add column if not exists yakit_tipi text;

-- 7) Alt kategori (mini ekskavatör, dozer, hidrolik gruplar vb.) — kategori sayfalarında
-- ilgili ilanların otomatik listelenmesi için
alter table market_requests add column if not exists alt_kategori text;
